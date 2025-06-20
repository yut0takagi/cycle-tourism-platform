const { useState } = React;

function DamageDetector() {
  const [image, setImage] = useState(null);
  const [boxes, setBoxes] = useState([]);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => setImage(ev.target.result.split(',')[1]);
    reader.readAsDataURL(file);
  };

  const handleSubmit = async () => {
    if (!image) return;
    try {
      const res = await fetch('/detect_road_damage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image }),
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
        {boxes.map((b, i) => (
          <div key={i}>Box: {b.join(', ')}</div>
        ))}
      </div>
    </div>
  );
}
