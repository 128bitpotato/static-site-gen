from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITAL = "ital"
    CODE = "code"
    LINK = "link"
    IMAG = "imag"

class TextNode():
    def __init__(text, text_type, url=None):
        self.text = text
        self.text_type = text_type.value
        self.url = url
    
    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (self.text == other.text and
                    self.text_type == other.text_type and
                    self.url == other.url)
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"