

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        list_of_strings = list(map(lambda item: f'{item[0]}="{item[1]}"', self.props.items()))
        return " " + " ".join(list_of_strings)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return (self.tag == other.tag and
                    self.value == other.value and
                    self.children == other.children and
                    self.props == other.props)
        return False
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("missing value, all LeafNodes must contain value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def __eq__(self, other):
        if isinstance(other, LeafNode):
            return (self.tag == other.tag and
                    self.value == other.value and
                    self.props == other.props)
        return False
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("missing value, all ParentNodes must contain tag")
        if self.children is None:
            raise ValueError("missing value, all ParentNodes must contain children")
        html_string = ""
        for child in self.children:
            html_string += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>'
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
    def __eq__(self, other):
        if isinstance(other, ParentNode):
            return (self.tag == other.tag and
                    self.children == other.children and
                    self.props == other.props)
        return False



    