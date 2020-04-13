import os
import json

style_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static','styles'))
template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
metadata_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'metadata'))
samples_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'samples'))

def reset_header():
    
    fdata = '''<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!-->
<html class="no-js">
<!--<![endif]-->

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title></title>
    <meta http-Equiv="Cache-Control" Content="no-cache" />
    <meta http-Equiv="Pragma" Content="no-cache" />
    <meta http-Equiv="Expires" Content="0" />
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/simplex/bootstrap.min.css" rel="stylesheet" integrity="sha384-cRAmF0wErT4D9dEBc36qB6pVu+KmLh516IoGWD/Gfm6FicBbyDuHgS4jmkQB8u1a" crossorigin="anonymous">
    <style>
        #main-container {
            position: absolute;
            top: 0px;
            left: 0px;
            right: 0px;
            bottom: 0px;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        #cssplaceholder{}

    </style>
</head>

<body>
    <div id="main-container">'''
    
    fp = open(os.path.join(template_path,"header.html"),"w")
    fp.write(fdata)
    fp.close()
    

def server_reset():
    fp = open(os.path.join(template_path, "content.html"), "w")
    fp.close()
    fp = open(os.path.join(style_path, "index.css"), "w")
    fp.close()
    fp = open(os.path.join(metadata_path, "element_structure.json"), "w")
    fp.close()
    fp = open(os.path.join(metadata_path, "metadata.pkl"), "wb")
    fp.close()
    for i in os.listdir(samples_path):
        os.remove(os.path.join(samples_path, i))

def rewrite_css(data):
    fp = open(os.path.join(style_path, "index.css"), "r")
    fp_content = fp.read().replace("}", "} ").split()
    fp.close()
    reppos = -1
    for i in enumerate(fp_content):
        if data["ele"] in i[1]:
            reppos = i[0]
    ele = data["ele"]
    del data["ele"]
    fp_content[reppos] = ele+json.dumps(data).replace(",", ";").replace(
        " ", "").replace('"', '').replace("backgroundColor", "background-color")
    with open(os.path.join(metadata_path, "element_structure.json"), 'r') as f:
        json_css = json.load(f)
        for i in data:
            json_css[ele][i] = data[i]
    with open(os.path.join(metadata_path, "element_structure.json"), 'w') as f:
        json.dump(json_css, f)
    fp = open(os.path.join(style_path, "index.css"), "w")
    fp.write("".join(fp_content))
    fp.close()


def download_file():
    reset_header()
    
    fp = open(os.path.join(template_path,"header.html"),"r")
    files = fp.readlines()
    fp.close()
    
    fp = open(os.path.join(style_path,"index.css"),"r")
    css = fp.read()
    fp.close()
    
    ind = 0
    for i in enumerate(files):
        if "cssplaceholder" in i[1]:
            ind = i[0]
            break
    
    files[ind] = "\t\t"+css.replace("{","{\n\t\t\t").replace(";",";\n\t\t\t").replace("}","}\n\t\t")
    
    fp = open(os.path.join(template_path,"header.html"),"w")
    fp.writelines(files)
    fp.close()