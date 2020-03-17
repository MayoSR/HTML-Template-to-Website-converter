import os

class HTMLFactory(object):

    def __init__(self, x, y, w, h):

        self.x1 = x
        self.y1 = y
        self.x2 = x+w
        self.y2 = y+h
        self.w = w
        self.h = h


class HTMLInput(HTMLFactory):

    parent_height = None
    parent_width = None

    def __init__(self, x, y, w, h):
        HTMLFactory.__init__(self, x, y, w, h)

    def return_aspect_ratio(self):
        return None

    def html_template(self):
        return '''
                <div class="form-group">
                    <label class="col-form-label" for="inputDefault">Default input</label>
                    <input type="text" class="form-control" placeholder="Default input">
                </div>
                '''

    def render_HTML_template(self):
        fp = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates', 'content.html')), "a+")
        fp.write(self.html_template())
        fp.close()


class HTMLImage(HTMLFactory):

    parent_height = None
    parent_width = None

    def __init__(self, x, y, w, h):
        HTMLFactory.__init__(self, x, y, w, h)

    def return_aspect_ratio(self):
        return None

    def html_template(self):
        return '''
                <div class="container">
                    <img src={{ url_for('static', filename = 'images/placeholder.png') }} width="20%" height="20%">
                </div>
                '''

    def render_HTML_template(self):
        fp = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates', 'content.html')), "a+")
        fp.write(self.html_template())
        fp.close()


def build_elements(element):
    print(element)
    if element == "Input":
        htmlElement = HTMLInput(0, 0, 0, 0)
        htmlElement.render_HTML_template()
    elif element == "Image":
        htmlElement = HTMLImage(0, 0, 0, 0)
        htmlElement.render_HTML_template()
