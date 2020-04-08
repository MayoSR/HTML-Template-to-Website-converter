var serverData = null

document.getElementById('file-btn').onchange = function (evt) {
    var tgt = evt.target || window.event.srcElement,
        files = tgt.files;

    // FileReader support
    if (FileReader && files && files.length) {
        var fr = new FileReader();

        fr.onload = function () {
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

document.getElementById("sbt").addEventListener("click", (e) => {

    let formData = new FormData()
    formData.append("uploaded-file", document.getElementById("file-btn").files[0]);
    var xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (this.readyState == "4" && this.status == "200") {
            document.getElementById("rendered-page").src = "http://localhost:5000/generatedpage"
            getCSSFromServer()
        }
    }
    xhr.setRequestHeader = "multipart/form-data"
    xhr.open("POST", "/sendfile", true)
    xhr.send(formData)

}, false)

function getCSSFromServer(){

    console.log("Fetching CSS")
    $.ajax({
        url:"http://localhost:5000/getcss",
        async : true,
        success:function(data){
            serverData = data
            console.log("Server data",serverData)
        },
        error:function(){
            alert("Error occured")
        }
    })
}

document.getElementById("previewframe").addEventListener("click", () => {
    window.open("/generatedpage");
}, false)

function iframeclick() {
    document.getElementById("rendered-page").contentWindow.document.body.onclick = function (event) {

        var ids = [
            "position",
            "left",
            "right",
            "top",
            "bottom",
            "width",
            "height",
            "backgroundColor",
            "color",
        ]
        ids.forEach((ele) => {
            console.log(ele)
            document.getElementById(ele).value = serverData["#"+event.target.id][ele]
        })
    }
}

function modifyValues() {
    var data = {
        "posip" : document.getElementById("pos").value,
        "leftip" : document.getElementById("left").value,
        "rightip" :document.getElementById("right").value,
        "topip" : document.getElementById("top").value,
        "bottomip" : document.getElementById("bottom").value,
        "widthip" : document.getElementById("width").value,
        "heightip" : document.getElementById("height").value,
        "bgip" : document.getElementById("backgroundColor").value,
        "colorip" : document.getElementById("color").value,
    }
    $.ajax({
        url:"http://localhost:5000/",
        contentType : "application/json",
        data : data,
        async : true,
        success:function(data){
            console.log("Modified")
        },
        error:function(){
            alert("Error occured")
        }
    })
}