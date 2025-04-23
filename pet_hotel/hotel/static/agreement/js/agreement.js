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
