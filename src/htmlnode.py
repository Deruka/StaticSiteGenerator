class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        HTMLString = ""
        if self.props is not None:
            for key, value in self.props.items():
                HTMLString += " " + key + '="' + value + '"'
        return HTMLString
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag == "img":
            props_string = self.props_to_html()
            return f"<{self.tag}{props_string}/>"            
        if not self.value:
            raise ValueError("Leaf Node has no Value")
        if not self.tag:
            return str(self.value)
        props_string = self.props_to_html()
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
    
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.props == other.props)

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent Node has no Tag")
        if not self.children:
            raise ValueError("Parent Node is missing a child parameter")
        HTML_String = ""
        props_string = self.props_to_html()
        for child in self.children:
            HTML_String += child.to_html()
        return f"<{self.tag}{props_string}>{HTML_String}</{self.tag}>"
