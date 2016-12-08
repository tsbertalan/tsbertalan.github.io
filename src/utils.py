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
    for k, v in kwargs.items():
        if k == 'cls':
            attribToAdd['class'] = kwargs.pop(k)
        if '____' in k:
            newKey = k.replace('____', '-')
            attribToAdd[newKey] = kwargs.pop(k) 
    tag = etree.Element(*args, **kwargs)
    tag.attrib.update(attribToAdd)
    return tag

        
def Div(**kwargs):
    return Tag('div', **kwargs)
