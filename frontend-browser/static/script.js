let audio;

document.getElementById("audio_upload").addEventListener("change", upload);

function upload(){
    console.log(document.getElementById("audio_upload"))
    audio = document.getElementById("audio_upload").files[0];
    console.log("received");
    console.log(audio);
}
