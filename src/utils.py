def tab(text, tabulator='  '):
    return '\n'.join([
                      tabulator + line
                      for line in text.split('\n')
                      ])


class Tag(object):

    def __init__(self, tagName, tagContent='', joiner='\n', doTab=True, **kwargs):
        ''' Kwarg hyphens should be mutilated to quadruple underscores.'''
        self.tagName = tagName
        self.joiner = joiner
        self.doTab = doTab
        kwargsList = []
        for (key, value) in kwargs.items():
            if key is 'cls':
                key = 'class'
            if '____' in key:
                newKey = key.replace('____', '-')
                kwargsList.append('%s="%s"' % (newKey, value))
            else:
                kwargsList.append('%s="%s"' % (key, value))
        self.kwargs = ' '.join(kwargsList)
        if len(self.kwargs) > 0:
            self.kwargs = ' ' + self.kwargs
        self.tagContent = tagContent

    def __call__(self, enclosed):
        if enclosed.strip() == '':
            return '<%s%s />' % (self.tagName, self.kwargs)

        if self.doTab:
            enclosed = tab(enclosed)
        return self.joiner.join([
                '<%s%s>' % (self.tagName, self.kwargs),
                enclosed,
                '</%s>' % self.tagName,
                ]).replace('\n \n', '\n').replace('\n  \n', '\n')
    
    def __str__(self):
        return self(self.tagContent)


class Div(Tag):
    def __init__(self, **kwargs):
        #Tag.__init__(self, 'div', **kwargs)
        super(Div, self).__init__('div', **kwargs)

