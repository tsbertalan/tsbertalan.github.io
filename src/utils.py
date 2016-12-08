# import xml.etree.ElementTree as ET
from lxml import etree

def tab(text, tabulator='  '):
    return '\n'.join([
                      tabulator + line
                      for line in text.split('\n')
                      ])


def getMatchingChildren(element, tag):
    for child in element:
        if child.tag == tag:
            yield child
 
def child(element, tag):
    for child in getMatchingChildren(element, tag):
        return child 
            
def tostring(element):
    return etree.tostring(element, method='html', pretty_print=True)

def Tag(*args, **kwargs):
    attribToAdd = {}
    
    if 'tagText' in kwargs:
        tagText = kwargs.pop('tagText')
    else:
        tagText = None
    
    for k, v in kwargs.items():
        if k == 'cls':
            attribToAdd['class'] = kwargs.pop(k)
        if '____' in k:
            newKey = k.replace('____', '-')
            attribToAdd[newKey] = kwargs.pop(k) 
    tag = etree.Element(*args, **kwargs)
    tag.attrib.update(attribToAdd)
    
    if tagText is not None:
        parsed = etree.HTML(tagText)
        p = child(child(parsed, 'body'), 'p')
        tag.text = p.text
        for contents in p:
            tag.append(contents) 
        
    return tag

        
def Div(**kwargs):
    return Tag('div', **kwargs)

def displayHtml(html, fname='/tmp/test.html', browser='google-chrome'):
    f = open(fname, 'w')
    f.write(tostring(html))
    f.close()
    if browser is not None:
        from os import system
        system('%s "%s"' % (browser, fname))
    
