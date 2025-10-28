const video = document.getElementById("video");

async function startCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;

  setInterval(captureFrame, 3000); // send every 3 seconds
}

async function captureFrame() {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  
  const imgData = canvas.toDataURL("image/jpeg");

  await fetch("http://localhost:5000/api/proctor", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: imgData }),
  });
}

document.getElementById("endExam")?.addEventListener("click", () => {
  alert("Exam Ended. Data saved.");
  window.location.href = "index.html";
});

startCamera();
