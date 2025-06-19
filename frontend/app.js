const { useState, useEffect, useRef } = React;

function useVanta() {
  const vantaRef = useRef(null);
  useEffect(() => {
    let effect = window.VANTA.NET({
      el: vantaRef.current,
      mouseControls: true,
      touchControls: true,
      color: 0xff3f81,
      backgroundColor: 0x0a0a0a
    });
    return () => {
      if (effect) effect.destroy();
    };
  }, []);
  return vantaRef;
}

function DamageDetector() {
  const [image, setImage] = useState(null);
  const [boxes, setBoxes] = useState([]);
  const [error, setError] = useState(null);

  const handleChange = e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => setImage(ev.target.result.split(',')[1]);
    reader.readAsDataURL(file);
  };

  const handleSubmit = async () => {
    if (!image) return;
    try {
      const res = await fetch('/detect_road_damage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Error');
      setBoxes(data.boxes);
      setError(null);
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="p-4 text-white">
      <h1 className="text-2xl font-bold mb-4">Road Damage Detection</h1>
      <input type="file" accept="image/*" onChange={handleChange} className="mb-2" />
      <button onClick={handleSubmit} className="bg-blue-500 text-white px-4 py-2 rounded">Send</button>
      {error && <p className="text-red-400 mt-2">{error}</p>}
      <div className="mt-4">
        {boxes.map((b,i)=>(<div key={i}>Box: {b.join(', ')}</div>))}
      </div>
    </div>
  );
}

function VideoFrameExtractor() {
  const [videoURL, setVideoURL] = useState(null);
  const [frames, setFrames] = useState([]);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const handleFile = e => {
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
    setFrames(f => [...f, url]);
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
        {frames.map((f,i)=>(<img key={i} src={f} alt={`frame-${i}`} className="w-32 h-32 object-cover"/>))}
      </div>
    </div>
  );
}

function App() {
  const [page, setPage] = useState('detect');
  const vantaRef = useVanta();
  return (
    <div ref={vantaRef} className="w-full h-full overflow-auto">
      <div className="max-w-2xl mx-auto bg-black bg-opacity-50 min-h-screen">
        <nav className="flex gap-4 p-4 text-white">
          <button onClick={()=>setPage('detect')} className="underline">Damage Detector</button>
          <button onClick={()=>setPage('video')} className="underline">Video Extractor</button>
        </nav>
        {page==='detect'?<DamageDetector/>:<VideoFrameExtractor/>}
      </div>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
