function onResults(results) {

  if (!results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) {
    sendMetrics(false, 0, 0, 0);
    return;
  }

  const lm = results.multiFaceLandmarks[0];

  function distance(a, b) {
    return Math.hypot(a.x - b.x, a.y - b.y);
  }

  const leftEAR =
    (distance(lm[160], lm[144]) + distance(lm[158], lm[153])) /
    (2 * distance(lm[33], lm[133]));

  const rightEAR =
    (distance(lm[385], lm[380]) + distance(lm[387], lm[373])) /
    (2 * distance(lm[362], lm[263]));

  const ear = (leftEAR + rightEAR) / 2;

  const mar = distance(lm[13], lm[14]) / distance(lm[78], lm[308]);

  const noseX = lm[1].x;
  const faceWidth = Math.abs(lm[234].x - lm[454].x);
  const headTurn = Math.abs(
    noseX - (lm[234].x + lm[454].x) / 2
  ) / faceWidth;

  sendMetrics(true, ear, mar, headTurn);
}

const faceMesh = new FaceMesh({
  locateFile: (file) =>
    `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
});

faceMesh.setOptions({
  maxNumFaces: 1,
  refineLandmarks: true,
  minDetectionConfidence: 0.6,
  minTrackingConfidence: 0.6
});

faceMesh.onResults(onResults);

const video = document.getElementById("video");
let mpCamera = null;
let videoStream = null;

async function startCamera(){
  try{
    videoStream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480 },
      audio: false
    });

    video.srcObject = videoStream;
    await video.play();

    mpCamera = new Camera(video, {
      onFrame: async () => {
        await faceMesh.send({ image: video });
      },
      width: 640,
      height: 480
    });

    mpCamera.start();
    console.log("✅ Camera started");
  }catch(err){
    alert("❌ Camera access denied");
    console.error(err);
  }
}

function stopCamera(){
  if(videoStream){
    videoStream.getTracks().forEach(track => track.stop());
    video.srcObject = null;
    videoStream = null;
  }

  if(mpCamera){
    mpCamera.stop();
    mpCamera = null;
  }

  console.log("🛑 Camera stopped");
}
