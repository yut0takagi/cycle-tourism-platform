import json
import os
from pathlib import Path
from typing import Dict

import torch
import torchvision
from PIL import Image
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from tqdm import tqdm


def log_dataset(dataset_dir: str, log_path: str) -> None:
    """Scan a COCO-format dataset and write simple stats as JSON."""
    ann_file = os.path.join(dataset_dir, "annotations.json")
    if not os.path.exists(ann_file):
        raise FileNotFoundError(f"annotations.json not found in {dataset_dir}")
    dataset = torchvision.datasets.CocoDetection(dataset_dir, ann_file)
    class_counts: Dict[int, int] = {}
    for _, targets in dataset:
        for t in targets:
            cls = t["category_id"]
            class_counts[cls] = class_counts.get(cls, 0) + 1
    stats = {
        "images": len(dataset),
        "annotations": sum(class_counts.values()),
        "class_distribution": class_counts,
    }
    Path(log_path).write_text(json.dumps(stats, indent=2))


def _get_transform():
    def transform(image, target):
        image = F.to_tensor(image)
        return image, target

    return transform


def fine_tune(dataset_dir: str, output_dir: str, epochs: int = 5) -> None:
    """Fine-tune a pre-trained Faster R-CNN model using a COCO-format dataset."""
    ann_file = os.path.join(dataset_dir, "annotations.json")
    dataset = torchvision.datasets.CocoDetection(
        dataset_dir, ann_file, transforms=_get_transform()
    )
    data_loader = torch.utils.data.DataLoader(
        dataset, batch_size=2, shuffle=True, collate_fn=lambda x: tuple(zip(*x))
    )

    model = fasterrcnn_resnet50_fpn(weights="DEFAULT")
    num_classes = max(t["category_id"] for _, targets in dataset for t in targets) + 1
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = (
        torchvision.models.detection.faster_rcnn.FastRCNNPredictor(
            in_features, num_classes
        )
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)

    model.train()
    for epoch in range(epochs):
        for images, targets in tqdm(data_loader, desc=f"epoch {epoch+1}"):
            images = list(img.to(device) for img in images)
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
            loss_dict = model(images, targets)
            losses = sum(loss for loss in loss_dict.values())
            optimizer.zero_grad()
            losses.backward()
            optimizer.step()
    os.makedirs(output_dir, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(output_dir, "model.pt"))


def evaluate(model_path: str, dataset_dir: str) -> float:
    """Evaluate a trained model on a validation dataset. Returns mAP."""
    ann_file = os.path.join(dataset_dir, "annotations.json")
    dataset = torchvision.datasets.CocoDetection(
        dataset_dir, ann_file, transforms=_get_transform()
    )
    data_loader = torch.utils.data.DataLoader(
        dataset, batch_size=2, shuffle=False, collate_fn=lambda x: tuple(zip(*x))
    )

    num_classes = max(t["category_id"] for _, targets in dataset for t in targets) + 1
    model = fasterrcnn_resnet50_fpn(weights=None, num_classes=num_classes)
    state_dict = torch.load(model_path, map_location="cpu")
    model.load_state_dict(state_dict)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    from torchvision.ops import box_iou

    total_iou = 0.0
    count = 0
    with torch.no_grad():
        for images, targets in data_loader:
            images = list(img.to(device) for img in images)
            outputs = model(images)
            for output, target in zip(outputs, targets):
                if len(output["boxes"]) == 0 or len(target["boxes"]) == 0:
                    continue
                iou = box_iou(output["boxes"].cpu(), target["boxes"].cpu()).max().item()
                total_iou += iou
                count += 1
    return total_iou / max(count, 1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Object detection training pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    log_parser = subparsers.add_parser("log", help="Log dataset stats")
    log_parser.add_argument("dataset", help="Path to dataset directory")
    log_parser.add_argument("output", help="Output JSON path")

    train_parser = subparsers.add_parser("train", help="Fine-tune model")
    train_parser.add_argument("dataset", help="Path to dataset directory")
    train_parser.add_argument("output", help="Directory to save model")
    train_parser.add_argument("--epochs", type=int, default=5)

    eval_parser = subparsers.add_parser("eval", help="Evaluate model")
    eval_parser.add_argument("model", help="Path to trained model")
    eval_parser.add_argument("dataset", help="Path to validation dataset")

    args = parser.parse_args()

    if args.command == "log":
        log_dataset(args.dataset, args.output)
    elif args.command == "train":
        fine_tune(args.dataset, args.output, args.epochs)
    elif args.command == "eval":
        score = evaluate(args.model, args.dataset)
        print(f"mAP approximation: {score:.4f}")
