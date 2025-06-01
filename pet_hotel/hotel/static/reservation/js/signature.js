const canvas = document.getElementById("signature-pad");
const signaturePad = new SignaturePad(canvas);

document.querySelector("form").addEventListener("submit", (e) => {
  if (signaturePad.isEmpty()) {
    e.preventDefault();
    alert("서명 후 제출해주세요 🐾");
    return;
  }

  const dataURL = signaturePad.toDataURL();
  document.getElementById("signature-field").value = dataURL;
});

function resizeCanvas() {
  const ratio = Math.max(window.devicePixelRatio || 1, 1);
  canvas.width = canvas.offsetWidth * ratio;
  canvas.height = canvas.offsetHeight * ratio;
  canvas.getContext("2d").scale(ratio, ratio);
  signaturePad.clear(); // 사이즈 바뀌면 초기화됨
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
