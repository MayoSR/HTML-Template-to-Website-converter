import os
import abc



class HTMLFactory(object):

    prev_left = None
    prev_top = None
    
    def __init__(self, coords):

        self.x1, self.y1, self.w, self.h = coords
        self.x2 = self.x1+self.w
        self.y2 = self.y1+self.h
        self.top_offset = self.y1
        self.margin = 0
        self.padding = 0
        self.position = "absolute"
        self.left = "auto"
        self.right = "auto"
        self.top = "auto"
        self.bottom = "auto"
        self.width = "auto"
        self.height = "auto"
        self.document = None

    def attach_new_width(self,obj):
        self.w = obj
        
    def attach_new_top(self,obj):
        self.top_offset = obj.top_offset
    
    def attach_new_left(self,obj):
        self.x1 = obj.x1
    
    def view_coordinates(self):
        return "W : %d" % (self.w)
    
    def set_margin(self, margin):
        self.margin = margin
        
    def set_padding(self, padding):
        self.padding = padding
    
    def set_position(self, position):
        self.position = position
    
    def set_left(self, left):
        self.left = left
        
    def set_top(self, top):
        self.top = top
        
    def set_bottom(self, bottom):
        self.bottom = bottom
        
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height
    
    
    @abc.abstractmethod
    def html_template(self):
        pass
    
    @abc.abstractmethod
    def css_template(self):
        pass
    
    def render_HTML_template(self):
        fp = open(os.path.abspath(os.path.join(os.path.dirname(
            __file__), '..', 'templates', 'content.html')), "a+")
        fp.write(self.html_template())
        fp.close()
        fp = open(os.path.abspath(os.path.join(os.path.dirname(
            __file__), '..','static', 'styles',     'index.css')), "a+")
        fp.write(self.css_template())
        fp.close()

    def set_css(self,parent):
        self.width = str(int((int(self.w) / int(parent.w))*100) - 3) + "% !important"
        self.height = str(int(((int(self.h - self.y1) / int(parent.h))*100)) - 2)+ "% !important"
        self.left = str(int((int(self.x1) / (int(parent.w)) )* 100) + 10) + "%"
        self.top = str(int((int(self.top_offset) / int(parent.h)) * 100) + 8) + "%"

class HTMLElementTemplateFactory:

    def __init__(self, coords,id):
        self.id = id
        self.coords = coords
        
    def cast_to_image(self,HTMLid,className):
        return HTMLImage(HTMLid,className,self.coords,self.id)

    def cast_to_input(self,HTMLid,className):
        return HTMLInput(HTMLid,className,self.coords,self.id)
    
    def cast_to_checkbox(self,HTMLid,className):
        return HTMLCheckBox(HTMLid,className,self.coords,self.id)
    
    def cast_to_button(self,HTMLid,className):
        return HTMLButton(HTMLid,className,self.coords,self.id)
    
    def cast_to_video(self,HTMLid,className):
        return HTMLButton(HTMLid,className,self.coords,self.id)
    
    
class HTMLDocument(HTMLFactory):

    def __init__(self, coords, id):
        self.id = id
        self.x1, self.y1, self.w, self.h = coords
        self.x2 = self.x1+self.w
        self.y2 = self.y1+self.h
        HTMLFactory.__init__(self,coords)


class HTMLInput(HTMLFactory):

    def __init__(self,HTMLid,className,coords,id):
        
        self.id = id
        self.HTMLid = HTMLid
        self.className = className
        
        HTMLFactory.__init__(self, coords)
        


    def html_template(self):
        return '''
                <div class="'''+ self.className +'''" >
                    <input type="text"   id="input'''+ self.HTMLid +'''"  class="form-control" placeholder="Default input">
                </div>
                '''
                
    def css_template(self):
        #return "#{}\{ position : {}; left : {}; right : {}; top : {}; bottom : {}; width : {}; height : {}; margin : {}; padding : {} \}".format(self.HTMLid,self.position,self.left,self.right,self.top,self.bottom,self.width,self.height,self.margin,self.padding)
        return f'''#input{self.HTMLid}{{
            position : {self.position};
            left : {self.left};
            right : {self.right};
            top : {self.top};
            bottom : {self.bottom}; 
            width : {self.width};
            height : {self.height};
            margin : {self.margin};
            padding : {self.padding};
        }}\n'''


class HTMLImage(HTMLFactory):

    def __init__(self,HTMLid,className,coords,id):
        self.id = id
        self.HTMLid = HTMLid
        self.className = className
        
        HTMLFactory.__init__(self, coords)
        
        

    def html_template(self):
        return '''
                <div class="container">
                    <img class="'''+ self.className +'''" src={{ url_for('static', filename = 'images/placeholder.png') }} id="image'''+ self.HTMLid +'''" >
                </div>
                '''

    def css_template(self):
        #return '''#{}{ position : {}; left : {}; right : {}; top : {}; bottom : {}; width : {}; height : {}; margin : {}; padding : {} }'''.format(self.HTMLid,self.position,self.left,self.right,self.top,self.bottom,self.width,self.height,self.margin,self.padding)
        return f'''#image{self.HTMLid}{{
            position : {self.position};
            left : {self.left};
            right : {self.right};
            top : {self.top};
            bottom : {self.bottom};
            width : {self.width};
            height : {self.height};
            margin : {self.margin};
            padding : {self.padding};
        }}\n'''
        
class HTMLCheckBox(HTMLFactory):

    def __init__(self,HTMLid,className,coords,id):
        
        self.id = id
        self.HTMLid = HTMLid
        self.className = className
        
        HTMLFactory.__init__(self, coords)
        


    def html_template(self):
        return '''
                <div class="'''+ self.className +'''" >
                    <input type="checkbox"   id="input'''+ self.HTMLid +'''" placeholder="Default input">
                </div>
                '''
                
    def css_template(self):
        #return "#{}\{ position : {}; left : {}; right : {}; top : {}; bottom : {}; width : {}; height : {}; margin : {}; padding : {} \}".format(self.HTMLid,self.position,self.left,self.right,self.top,self.bottom,self.width,self.height,self.margin,self.padding)
        return f'''#input{self.HTMLid}{{
            position : {self.position};
            left : {self.left};
            right : {self.right};
            top : {self.top};
            bottom : {self.bottom}; 
            width : {self.width};
            height : {self.height};
            margin : {self.margin};
            padding : {self.padding};
        }}\n'''

class HTMLButton(HTMLFactory):

    def __init__(self,HTMLid,className,coords,id):
        
        self.id = id
        self.HTMLid = HTMLid
        self.className = className
        
        HTMLFactory.__init__(self, coords)
        


    def html_template(self):
        return '''
                <div class="'''+ self.className +'''" >
                    <input type="button"   id="input'''+ self.HTMLid +'''"  class="btn btn-primary" value="Button">
                </div>
                '''
                
    def css_template(self):
        #return "#{}\{ position : {}; left : {}; right : {}; top : {}; bottom : {}; width : {}; height : {}; margin : {}; padding : {} \}".format(self.HTMLid,self.position,self.left,self.right,self.top,self.bottom,self.width,self.height,self.margin,self.padding)
        return f'''#input{self.HTMLid}{{
            position : {self.position};
            left : {self.left};
            right : {self.right};
            top : {self.top};
            bottom : {self.bottom}; 
            width : {self.width};
            height : {self.height};
            margin : {self.margin};
            padding : {self.padding};
        }}\n'''

class HTMLVideo(HTMLFactory):

    def __init__(self,HTMLid,className,coords,id):
        
        self.id = id
        self.HTMLid = HTMLid
        self.className = className
        
        HTMLFactory.__init__(self, coords)
        


    def html_template(self):
        return '''
                <div class="'''+ self.className +'''" >
                    <iframe
                        src="https://www.youtube.com/embed/tgbNymZ7vqY?playlist=tgbNymZ7vqY&loop=1">
                    </iframe>
                </div>
                '''
                
    def css_template(self):
        #return "#{}\{ position : {}; left : {}; right : {}; top : {}; bottom : {}; width : {}; height : {}; margin : {}; padding : {} \}".format(self.HTMLid,self.position,self.left,self.right,self.top,self.bottom,self.width,self.height,self.margin,self.padding)
        return f'''#input{self.HTMLid}{{
            position : {self.position};
            left : {self.left};
            right : {self.right};
            top : {self.top};
            bottom : {self.bottom}; 
            width : {self.width};
            height : {self.height};
            margin : {self.margin};
            padding : {self.padding};
        }}\n'''


def build_elements(element,cast):
    
    if element == "Input":
        return cast.cast_to_input(cast.id,"form-group")
    elif element == "Image":
        return cast.cast_to_image(cast.id,"")
    elif element == "Checkbox":
        return cast.cast_to_checkbox(cast.id,"")
    elif element == "Button":
        return cast.cast_to_button(cast.id,"")
    elif element == "Video":
        return cast.cast_to_video(cast.id,"")
