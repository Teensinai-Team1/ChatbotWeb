let clicker = document.getElementById("button");
let closer = document.querySelector(".close");
let reg = document.getElementById("register");
var pops = document.querySelectorAll(".content-modal");

clicker.addEventListener('click', function(){
    document.querySelector(".bg-modal").style.display = "flex";
    pops[0].style.display = "block";
});

reg.addEventListener('click', function(){
    document.querySelector(".bg-modal").style.display = "flex";
    pops[1].style.display = "block";
})

closer.addEventListener('click', function(){
    document.querySelector(".bg-modal").style.display = "none";
    for (var n=0; n < pops.length; n++){
        pops[n].style.display = "none";
    }
});