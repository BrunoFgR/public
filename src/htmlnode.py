class HtmlNode:
    def __init__(self, tag, value, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method is not implemented")

    def props_to_html(self):
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html.strip()

    def  __repr__(self):
        return f"HtmlNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"
