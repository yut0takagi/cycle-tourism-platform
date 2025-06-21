# サイクルツーリズム活性化プラットフォーム

## ビジネス要件定義書 兼 システム要件定義書

> **Version**: 0.1
> **作成日**: 2025‑05‑27
> **作成者**: ChatGPT (based on user concept & 散走\_アイデアソン)

---

## 1. 概要・目的

地方の観光資源とサイクルツーリズムを結びつけ、\*\*ローダー（ロードバイク愛好家）\*\*が走行･撮影するデータを AI が自動編集し、地方自治体・旅行者向けに PR 動画と付加価値データを提供する。目的は

1. ローダーの“走る楽しみ”を拡張し配信者化する。
2. 自治体へ SNS 拡散用動画 + 行動データを**低コスト**で提供する。
3. 地方の観光・移住促進 KPI（来訪者数・現地消費額 等）を伸ばす。 

---

## 2. ペルソナ

| #   | ペルソナ                       | ニーズ / 痛点                       |
| --- | -------------------------- | ------------------------------ |
| P‑1 | **旅行プランを模索する Active User** | 穴場スポット・短時間で行程を決めたい／動画で雰囲気を掴みたい |
| P‑2 | **地方公共団体・DMO 担当者**         | PR 予算が限られ動画制作コストが高い／観光データが不足   |
| P‑3 | **サイクリング好きローダー**           | 新ルート探し・走行ログ共有・撮影/配信で収益化したい     |

---

## 3. ビジネスモデル

| ステークホルダ     | 価値提供                         | 収益源             |
| ----------- | ---------------------------- | --------------- |
| ローダー        | 高性能カメラ/バイタル機器レンタル、走行報酬（Coin） | ‑               |
| Active User | PR 動画 & ルート閲覧、宿/飲食店レコメンド     | アフィリエイト手数料      |
| 自治体/企業      | SNS 用ショート動画、来訪 KPI ダッシュボード   | 年額 SaaS ライセンス   |
| プラットフォーム    | データ販売 (道路補修･都市計画)、広告         | B2B/B2G データ API |

**収益試算** (ローダー 6000 万人 × 年 1 回旅 × 3 万円消費 ≒ 1.8 兆円市場の 0.1% を GMV として獲得) → 初年度 GMV 18 億円、手数料 10% で 1.8 億円を目指す。

---

## 4. 市場規模フェルミ推定

* **ローダー向け旅市場**: 6000 万人 × 3 万円/回 × 0.1 回/年 = **1.8 兆円**
* **学生旅行アクティブユーザ**: 3000 万人 × 3 万円 = **9000 億円**
* **地方活性化追加効果**: 合算で約 **3 兆円/年** 規模の消費を活性化し得る。

---

## 5. 成功指標 (KPI)

| 指標           | 目標 (ローンチ +12 か月) |
| ------------ | ---------------- |
| 月間アクティブローダー数 | 20,000           |
| アップロード動画数    | 50,000 本         |
| PR 動画視聴数 / 月 | 1,000 万回         |
| 契約自治体数       | 50               |
| 来訪誘発率 (動画経由) | 3%               |

---

## 6. サービスフロー

1. **参加登録** (メール or SSO)
2. **ツーリングプラン選択**：動画・画像・難易度から AI 推奨ルートを提示
3. **機器受取**：GoPro 4K + Garmin バイタルセンサ (本人確認)
4. **走行 & 撮影**
5. **Wi‑Fi 自動アップロード** (B2Video)
6. **AI ハイライト抽出**：美景ポイント検出モデル
7. **自治体ダッシュボード反映 & 報酬付与**
8. **動画公開 & SNS 拡散** fileciteturn0file0

---

## 7. システム概要

```
[Mobile App] ──▶ [Backend API]
                        │
        ┌──────────┬───────────────┐
        │Video Upload Svc│ Telemetry Ingest │
        ├──────────┼───────────────┤
        │AI Scenic Scorer│ AI Video Editor  │
        └──────────┴───────────────┘
                        │
           [Data Lake & Dashboard]
```

---

## 8. 機能要件

### 8.1 データ取得 (F‑01)

| 要件                                 | 優先度    |
| ---------------------------------- | ------ |
| GoPro/Garmin 連携で 4K 映像・GPS・心拍を同時記録 | High   |
| 盗難防止のためデバイス位置を 5 秒間隔で送信            | Medium |

### 8.2 アップロード & AI 処理 (F‑02)

| 要件                                          | 優先度  |
| ------------------------------------------- | ---- |
| Wi‑Fi 接続時に自動アップロード (途中再接続可)                 | High |
| Vision AI で風景スコアリング (Instagram 高評価画像を教師データ) | High |
| Top‑N ハイライトを 60 秒縦動画へ自動編集 (BGM / テロップ付)     | High |

### 8.3 ダッシュボード (F‑03)

| 要件                           | 優先度    |
| ---------------------------- | ------ |
| 来訪者数、走行ルートヒートマップ、消費推定額を可視化   | High   |
| 道路損傷検知レイヤ (ひび割れ・穴) を GIS で表示 | Medium |

### 8.4 報酬 & コミュニティ (F‑04)

| 要件                           | 優先度    |
| ---------------------------- | ------ |
| Scenic スコア & 再生回数に応じ Coin 付与 | High   |
| Coin は宿・レンタサイクル・地元 EC に使用可能  | Medium |
| フォロー・コメント・ルート共有機能            | Medium |

---

## 9. 非機能要件

| 区分      | 要件                                            |
| ------- | --------------------------------------------- |
| パフォーマンス | ハイライト自動生成 ≤5 分 / 30 分映像                       |
| 可用性     | 99.5% SLA (AWS S3 + CloudFront, RDS Multi‑AZ) |
| セキュリティ  | OAuth2, JWT、機器紛失時の遠隔ワイプ                       |
| プライバシー  | GDPR & 個人情報保護法準拠、顔ぼかし自動処理                     |

---

## 10. データモデル (論理)

```
User(id, role, coin, ...)
Ride(id, user_id, route_geojson, distance, elev_gain, ...)
Media(id, ride_id, type, url, scenic_score, ...)
HighlightVideo(id, ride_id, url, publish_status, views)
Municipality(id, name, contract_level, ...)
DashboardMetric(id, municipality_id, date, visits, spend_est)
Transaction(id, user_id, coin, type, ref_id)
```

---

## 11. 技術スタック

| レイヤ        | 技術候補                                        |
| ---------- | ------------------------------------------- |
| デバイス       | GoPro HERO12, Garmin Edge with ANT+ sensors |
| モバイル       | React Native + Expo / iOS ネイティブ SDK         |
| Backend    | FastAPI + Celery、gRPC マイクロサービス              |
| AI Vision  | AWS Rekognition + Fine‑tuned CLIP           |
| Video Edit | RunwayML Gen‑2 API / FFmpeg pipeline        |
| Storage    | AWS S3, Glacier アーカイブ                       |
| Analytics  | AWS Athena + QuickSight、Superset            |
| CI/CD      | GitHub Actions, Terraform IaC, EKS          |

---

## 12. リスク & 対策

| リスク     | 影響         | 対策                              |
| ------- | ---------- | ------------------------------- |
| 機器紛失・盗難 | データ流出・コスト増 | 位置追跡 + 保険 + デポジット               |
| 低品質映像多数 | PR 効果低下    | Scenic スコア閾値未満は非公開、スコア向上Tips 提供 |
| 個人情報流出  | 法令違反       | 自動顔ぼかし + 撮影禁止区域フィルタ             |

---

## 13. ロードマップ

| フェーズ | 期間       | 主要マイルストーン                 |
| ---- | -------- | ------------------------- |
| POC  | 0‑2 ヶ月   | デバイス連携 & AI Scenic 判定 MVP |
| β版   | 3‑5 ヶ月   | 自治体ダッシュボード, Coin 報酬システム   |
| 正式版  | 6‑9 ヶ月   | コミュニティ & 路面診断機能、広告／アフィ連携  |
| 拡張   | 10‑12 ヶ月 | 海外自治体展開、多言語音声ガイド          |

---

> **備考**: 本要件定義は初版ドラフトであり、ステークホルダーとのレビューを経て優先度や KPI を更新します。

## バックエンド API (Flask)

簡易的なバックエンドAPIをFlaskで構築しました。
現在はBlueprintを用いて`backend/routes`と`backend/services`に機能を分割し、
スケールしやすい構成になっています。
以下の手順で開発サーバを起動できます。

```bash
pip install -r requirements.txt
python backend/app.py
```

バックエンドのコードは以下のようにモジュールごとに分割されています。

```
backend/
    app.py          # エントリーポイント
    __init__.py     # Flask アプリ生成
    routes/         # 各エンドポイントの Blueprint
    services/       # 画像処理などのサービス層
```

`/`路線でAPIの結果がJSONで返ります。`/health`路線はヘルスチェック用です。

## フロントエンド (React)

`frontend` ディレクトリには Tailwind CSS と Vanta.js を利用した簡易 React アプリを配置しています。React コンポーネントは `useVanta.js`、`DamageDetector.js`、`VideoFrameExtractor.js`、`App.js` と複数のファイルに分割され、`index.js` から `ReactDOM.render` を呼び出しています。画像をアップロードして道路損傷検知結果を表示するページと、動画からフレームを抜き出すページを切り替えて利用できます。

### 起動方法

以下のように静的サーバを立ち上げてアクセスしてください。

```bash
cd frontend
python -m http.server 8000
```

ブラウザで `http://localhost:8000` を開くとアプリが表示されます。

## 物体検知ファインチューニングパイプライン

`backend/object_detection_pipeline.py` には、COCO 形式データセットの統計記録、Faster R-CNN のファインチューニング、学習済みモデルの簡易検証を行うスクリプトを追加しました。

### 使い方

```bash
# データセットの統計をJSONに出力
python backend/object_detection_pipeline.py log /path/to/dataset stats.json

# モデルのファインチューニング
python backend/object_detection_pipeline.py train /path/to/dataset output_dir --epochs 10

# 検証 (平均IoUを表示)
python backend/object_detection_pipeline.py eval output_dir/model.pt /path/to/val_dataset
```


## テストの実行

ユニットテストは `pytest` で実行できます。

```bash
pip install -r requirements.txt
pytest
```
