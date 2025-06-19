const { useState } = React;

function App() {
  const [page, setPage] = useState('detect');
  const vantaRef = useVanta();
  return (
    <div ref={vantaRef} className="w-full h-full overflow-auto">
      <div className="max-w-2xl mx-auto bg-black bg-opacity-50 min-h-screen">
        <nav className="flex gap-4 p-4 text-white">
          <button onClick={() => setPage('detect')} className="underline">
            Damage Detector
          </button>
          <button onClick={() => setPage('video')} className="underline">
            Video Extractor
          </button>
        </nav>
        {page === 'detect' ? <DamageDetector /> : <VideoFrameExtractor />}
      </div>
    </div>
  );
}

