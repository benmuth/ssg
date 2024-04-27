class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def toHTML(self):
        raise NotImplementedError

    def propsToHTML(self):
        html_attrs = ""
        if self.props:
            for attr in self.props:
                html_attrs += f'{attr}="{self.props[attr]}" '
            html_attrs = html_attrs[:-1]
        return html_attrs

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(children=None, tag=tag, value=value, props=props)

    def toHTML(self):
        if self.tag:
            if self.props:
                return f"<{self.tag} {self.propsToHTML()}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
        return self.value


class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(children=children, tag=tag, props=props)

    def toHTML(self):
        if not self.tag:
            raise ValueError("No tag provided")
        if not self.children:
            raise ValueError("Parent node has no children")

        html = ""
        if self.props:
            html += f"<{self.tag} {self.propsToHTML()}>"
        else:
            html += f"<{self.tag}>"
        for child in self.children:
            print(child)
            html += child.toHTML()
        html += f"</{self.tag}>"

        return html
