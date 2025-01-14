let audio;

document.getElementById("audio_upload").addEventListener("change", upload_audio);

function upload_audio(){
    console.log(document.getElementById("audio_upload"))
    audio = document.getElementById("audio_upload").files[0];
}


