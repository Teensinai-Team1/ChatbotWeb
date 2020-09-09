function talk(){
    window.onload = document.getElementById("narr").play();
}

function userm(){
    var constraints = {
        audio: true,
        video: true
    };

    navigator.mediaDevices.getUserMedia(constraints).then(function(mediaStream){
        var video = document.getElementById("Prev");
        var Vidsave = document.getElementById("Vidsave");
        video.srcObject = mediaStream;
        video.play();
        let start = document.getElementById("Startbtn");
        let stop = document.getElementById("Stopbtn");
        let mediaRecorder = new mediaRecorder(mediaStream);
        let chunks = [];
        start.addEventListener('click', (ev)=>{
            mediaRecorder.start();
            console.log(mediaRecorder.state);
        })
        stop.addEventListener('click', (ev)=>{
            mediaRecorder.stop();
            console.log(mediaRecorder.state);
        })
        mediaRecorder.ondataavailable = function(ev){
            chunks.push(ev.data);
        }
        mediaRecorder.onstop = (ev)=>{
            let blob = new Blob(chunks, { 'type': 'video/mp4'});
            chunks = [];
            let videoURL = window.URL.createObjectURL(blob);
            Vidsave.src = videoURL;
        }
    }).catch(function(err){
        console.log("Somethang went wrong.");
    })
}

userm()