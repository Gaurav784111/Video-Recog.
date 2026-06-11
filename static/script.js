const video = document.getElementById("video");
const nameBox = document.getElementById("name");

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => {
    video.srcObject = stream;
});

// Capture frame every second
setInterval(() => {
    captureAndSend();
}, 1000);

function captureAndSend() {

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    const imageData = canvas.toDataURL("image/jpeg");

    fetch("/recognize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(res => res.json())
    .then(data => {
        nameBox.innerText = data.name;
    });
}
