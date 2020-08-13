window.onload = function(){

    var constraints = {
        audio: true,
        video: true
    };

    navigator.mediaDevices.getUserMedia(constraints).then(function(mediaStream)
        var video = document.querySelector('video')
        video.srcObject = mediaStream;
        video.play()
    }).catch(function(err) {
        console.log("Yikes an error!")
    })
}