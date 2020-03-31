document.getElementById('file-btn').onchange = function(evt) {
    var tgt = evt.target || window.event.srcElement,
        files = tgt.files;

    // FileReader support
    if (FileReader && files && files.length) {
        var fr = new FileReader();

        fr.onload = function() {
            document.getElementById("preview").src = fr.result;
            $("#cf").text("File selected!").removeClass("btn-primary").addClass("btn-success")
        }
        fr.readAsDataURL(files[0]);
    }

    // Not supported
    else {
        // fallback -- perhaps submit the input to an iframe and temporarily store
        // them on the server until the user's session ends.
    }
}

document.getElementById("sbt").addEventListener("click",(e)=>{

    let formData = new FormData()
    formData.append("uploaded-file", document.getElementById("file-btn").files[0]);
    var xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function(){
        if(this.readyState == "4" && this.status == "200"){
            alert("Uploaded")
            window.location.href = "http://localhost:5000/generatedpage"
        }
    }
    xhr.setRequestHeader="multipart/form-data"
    xhr.open("POST","/sendfile",true)
    xhr.send(formData)
    
},false)

document.getElementById("previewframe").addEventListener("click",()=>{
    window.open("/generatedpage");
},false)