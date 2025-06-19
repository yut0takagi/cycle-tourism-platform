const { useEffect, useRef } = React;

function useVanta() {
  const vantaRef = useRef(null);
  useEffect(() => {
    let effect = window.VANTA.NET({
      el: vantaRef.current,
      mouseControls: true,
      touchControls: true,
      color: 0xff3f81,
      backgroundColor: 0x0a0a0a,
    });
    return () => {
      if (effect) effect.destroy();
    };
  }, []);
  return vantaRef;
}
