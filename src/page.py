from utils import Tag


class TagTree(Tag):

    def __init__(self, name=None, **kwargs):
        if name is None:
            baseTag = None
        else:
            baseTag = Tag(name, **kwargs)
        self.baseTag = baseTag
        self.children = []
  
    @property
    def content(self):
        assert hasattr(self, 'children')
        return '\n'.join([str(tree) for tree in self.children])
    
    def __str__(self):
        if self.baseTag is not None:
            return self.baseTag(self.content)
        else:
            return self.content

    def childrenWithName(self, name):
        return [c for c in self.children
                if c.baseTag is not None
                and c.baseTag.tagName == name]

    def child(self, name):
        children = self.childrenWithName(name)
        if len(children) > 0:
            return children[0]
        else:
            return None

    def append(self, child):
        self.children.append(child)
        return self
            

class Head(TagTree):

    def __init__(self):
        super(Head, self).__init__('head')
        self.children.append(Tag('link',
            rel="stylesheet",
            href="https://fonts.googleapis.com/icon?family=Material+Icons",
        ))
        self.children.append(Tag('link',
            rel="stylesheet",
            href="https://code.getmdl.io/1.2.1/material.blue-yellow.min.css",
        ))
        self.children.append(Tag('script defer',
            src="https://code.getmdl.io/1.2.1/material.min.js"
        ))
        self.children.append(Tag('meta',
            name='viewport', content="width=device-width, initial-scale=1.0"
        ))


class Html(TagTree):
    def __init__(self):
        super(Html, self).__init__('html')
        self.children.append(Head())
        self.children.append(TagTree('body'))

if __name__ == '__main__':
    page = Html()
    from components import button
    print page.children
    page.child('html').child('body').append(button('test button'))
    print str(page)
