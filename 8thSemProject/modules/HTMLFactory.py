import os
import abc

class HTMLFactory(object):

    def __init__(self, coords):

        self.x1, self.y1, self.w, self.h = coords
        self.x2 = self.x1+self.w
        self.y2 = self.y1+self.h
        self.margin = 0
        self.padding = 0
        self.position = "absolute"
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.width = 0
        self.height = 0

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
    
    def render_HTML_template(self):
        fp = open(os.path.abspath(os.path.join(os.path.dirname(
            __file__), '..', 'templates', 'content.html')), "a+")
        fp.write(self.html_template())
        fp.close()
        fp = open(os.path.abspath(os.path.join(os.path.dirname(
            __file__), '..','static', 'styles', 'index.css')), "a+")
        fp.write(self.css_template())
        fp.close()


class HTMLElementTemplateFactory:

    def __init__(self, coords,id):
        self.id = id
        self.coords = coords

    def cast_to_image(self,HTMLid,className,parent):
        return HTMLInput(HTMLid,className,self.coords,self.id,parent)

    def cast_to_input(self,HTMLid,className,parent):
        return HTMLImage(HTMLid,className,self.coords,self.id,parent)
    
    


class HTMLDocument(HTMLFactory):

    parent_height = None
    parent_width = None

    def __init__(self, coords, id):

        self.id = id
        HTMLFactory.__init__(self,coords)


class HTMLInput(HTMLFactory):

    def __init__(self,HTMLid,className,coords,id,parent):
        
        self.id = id
        self.HTMLid = HTMLid
        self.className = className
        self.document = parent
        
        HTMLFactory.__init__(self, coords)

    def html_template(self):
        return '''
                <div class="'''+ self.className +'''">
                    <label class="col-form-label" for="inputDefault">Default input</label>
                    <input type="text"  id="'''+ self.HTMLid +'''"   class="form-control" placeholder="Default input">
                </div>
                '''.format(self.className,self.id)
                
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

    def __init__(self,HTMLid,className,coords,id,parent):
        self.id = id
        self.HTMLid = HTMLid
        self.className = className
        self.document = parent
        
        HTMLFactory.__init__(self, coords)

    def html_template(self):
        return '''
                <div class="container">
                    <img class="'''+ self.className +'''" src={{ url_for('static', filename = 'images/placeholder.png') }} id="'''+ self.HTMLid +'''" >
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

def build_elements(element,cast,parent):
    if element == "Input":
        htmlElement = cast.cast_to_input(cast.id,"form-group",parent)
        htmlElement.render_HTML_template()
    elif element == "Image":
        htmlElement = cast.cast_to_image(cast.id,"",parent)
        htmlElement.render_HTML_template()
