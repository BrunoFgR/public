class HTMLNode:
    def __init__(self, tag=None, value=None, children=[], props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method is not implemented")

    def props_to_html(self):
        props_html = ""
        if self.props:
            for key, value in self.props.items():
                props_html += f' {key}="{value}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag='{self.tag}', value='{self.value}', props={self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be None")
        if self.children is None:
            raise ValueError("Children cannot be None")

        inner_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag='{self.tag}', children={self.children}, props={self.props})"
