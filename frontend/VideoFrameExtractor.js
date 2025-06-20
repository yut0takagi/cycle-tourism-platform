const { useState, useRef } = React;

function VideoFrameExtractor() {
  const [videoURL, setVideoURL] = useState(null);
  const [frames, setFrames] = useState([]);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const handleFile = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setVideoURL(URL.createObjectURL(file));
  };

  const captureFrame = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const url = canvas.toDataURL('image/png');
    setFrames((f) => [...f, url]);
  };

  return (
    <div className="p-4 text-white">
      <h1 className="text-2xl font-bold mb-4">Video Frame Extractor</h1>
      <input type="file" accept="video/*" onChange={handleFile} className="mb-2" />
      {videoURL && (
        <div>
          <video src={videoURL} controls ref={videoRef} className="w-full max-w-md mb-2" />
          <button onClick={captureFrame} className="bg-green-500 px-4 py-2 rounded">Capture Frame</button>
          <canvas ref={canvasRef} className="hidden" />
        </div>
      )}
      <div className="flex flex-wrap mt-4 gap-2">
        {frames.map((f, i) => (
          <img key={i} src={f} alt={`frame-${i}`} className="w-32 h-32 object-cover" />
        ))}
      </div>
    </div>
  );
}

