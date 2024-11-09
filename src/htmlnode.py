

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
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("missing value, all LeafNodes must contain value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self, index_so_far=0, string=""):
        if self.tag is None:
            raise ValueError("missing value, all ParentNodes must contain tag")
        if self.children is None:
            raise ValueError("missing value, all ParentNodes must contain children")
        if len(self.children) > 1:
            return string = self.children[index_so_far:].to_html() + self.to_html(index_so_far + 1)
        return f'<{self.tag}{self.props_to_html()}>{string}</{self.tag}>'

    