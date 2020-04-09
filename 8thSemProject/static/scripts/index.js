var serverData = null
var selectedElement = null

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
        selectedElement = event.target.id
        ids.forEach((ele) => {
            document.getElementById(ele).value = serverData["#"+event.target.id][ele]
        })
    }
}

function modifyValues() {
    var data = {
        "ele": "#"+selectedElement,
        "position" : document.getElementById("position").value,
        "left" : document.getElementById("left").value,
        "right" :document.getElementById("right").value,
        "top" : document.getElementById("top").value,
        "bottom" : document.getElementById("bottom").value,
        "width" : document.getElementById("width").value,
        "height" : document.getElementById("height").value,
        "backgroundColor" : document.getElementById("backgroundColor").value,
        "color" : document.getElementById("color").value,
    }
    console.log(selectedElement)
    document.getElementById("rendered-page").contentWindow.document.getElementById(selectedElement).style.position = document.getElementById("position").value,
    document.getElementById("rendered-page").contentWindow.document.getElementById(selectedElement).style.left = document.getElementById("left").value,
    document.getElementById("rendered-page").contentWindow.document.getElementById(selectedElement).style.right = document.getElementById("right").value,
    document.getElementById("rendered-page").contentWindow.document.getElementById(selectedElement).style.top = document.getElementById("top").value,
    document.getElementById("rendered-page").contentWindow.document.getElementById(selectedElement).style.bottom = document.getElementById("bottom").value,
    document.getElementById("rendered-page").contentWindow.document.getElementById(selectedElement).style.width = document.getElementById("width").value,
    document.getElementById("rendered-page").contentWindow.document.getElementById(selectedElement).style.height = document.getElementById("height").value,
    document.getElementById("rendered-page").contentWindow.document.getElementById(selectedElement).style.backgroundColor = document.getElementById("backgroundColor").value,
    document.getElementById("rendered-page").contentWindow.document.getElementById(selectedElement).style.color = document.getElementById("color").value,
    $.ajax({
        url:"http://localhost:5000/modify",
        data : JSON.stringify(data),
        contentType : "application/json",
        async : true,
        method:"POST",
        success:function(data){
            console.log("Modified")
            document.getElementById("rendered-page").contentWindow.reload(true)
        },
        error:function(){
            alert("Error occured")
        }
    })
}