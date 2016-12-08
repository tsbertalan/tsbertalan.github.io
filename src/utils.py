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

def parseAnonymousHTML(toparse, disp=False):
    parsed = etree.HTML(toparse)
    if disp:
        print 'parsed is', tostring(parsed)
    body = child(parsed, 'body')
    if len(body) == 1:
        return body[0]
    else:
        return body

def Tag(*args, **kwargs):
    attribToAdd = {}
    
    if 'tagText' in kwargs:
        tagText = kwargs.pop('tagText')
    else:
        tagText = None
        
    if 'toAppend' in kwargs:
        toAppend = kwargs.pop('toAppend')
    else:
        toAppend = []
    
    for k, v in kwargs.items():
        if k == 'cls':
            attribToAdd['class'] = kwargs.pop(k)
        if '____' in k:
            newKey = k.replace('____', '-')
            attribToAdd[newKey] = kwargs.pop(k) 
    tag = etree.Element(*args, **kwargs)
    tag.attrib.update(attribToAdd)
    
    if tagText is not None:
        p = parseAnonymousHTML(tagText)
        tag.text = p.text
        for contents in p:
            tag.append(contents)
            
    tag.extend(toAppend)
        
    return tag

        
def Div(**kwargs):
    return Tag('div', **kwargs)


def writePage(html, fname):
    print 'Opening', fname
    f = open(fname, 'w')
    f.write(tostring(html))
    f.close()
    print 'Saved', fname


def showPage(fname, browser='google-chrome'):    
    from os import system
    system('%s "%s"' % (browser, fname))
    
    
def displayHtml(html, fname='/tmp/test.html', browser='google-chrome'):
    writePage(html, fname)
    if browser is not None:
        showPage(fname, browser)
    
    
