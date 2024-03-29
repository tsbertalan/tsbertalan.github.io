# import xml.etree.ElementTree as ET
from lxml import etree, html as lxml_html
from os.path import dirname, join, basename
from shutil import copy

def tab(text, tabulator='  '):
    return '\n'.join([
                      tabulator + line
                      for line in text.split('\n')
                      ])


def getMatchingChildren(element, tag):
    assert element is not None, 'Was an empty document used?'
    for child in element:
        if child.tag == tag:
            yield child
 
 
def child(element, tag):
    for child in getMatchingChildren(element, tag):
        return child 
     
            
def tostring(element):
    return etree.tostring(element, method='html', pretty_print=True).decode('utf-8').replace('##AMPERSAND##', '&')


def parseAnonymousHTML(toparse, disp=False, keepEnclosingP=False):
    parsed = etree.HTML(toparse)
    out = child(parsed, 'body')
    if not keepEnclosingP and len(out) == 1 and out[0].tag == 'p':
        out = out[0]
    outTup = out.text, [c for c in out], out.tail
    if disp:
        print('Returning', outTup[0], '[')
        for c in outTup[1]:
            print(tostring(c))
            print(',')
        print(']', outTup[2])
    return outTup


def add_mathjax(head):

    # MathJax needs special help to do inline mode??
    head.append(Tag('script',
                    tagText='''
  MathJax = {
    tex: {
      inlineMath: [['$', '$']],
      processEscapes: true,
    }
  }
  ''', parseTagText=False))
    head.append(Tag('script', type="text/javascript", id="MathJax-script", async_=None, src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"))


def Tag(*args, **kwargs):
    attribToAdd = {}
    
    tagText = None
    if 'tagText' in kwargs:
        tagText = kwargs.pop('tagText')

    parseTagText = False        
    if 'parseTagText' in kwargs:
        parseTagText = kwargs.pop('parseTagText')
    
    toAppend = []
    if 'toAppend' in kwargs:
        toAppend = kwargs.pop('toAppend')
        
    disp = False
    if 'disp' in kwargs:
        disp = kwargs.pop('disp')

    boolean_elems = []
    
    for k, v in list(kwargs.items()):
        if k == 'cls':
            attribToAdd['class'] = kwargs.pop(k)
        if k == 'for_':
            attribToAdd['for'] = kwargs.pop(k)
        if k == 'async_':
            attribToAdd['async'] = kwargs.pop(k)
        if '____' in k:
            newKey = k.replace('____', '-')
            attribToAdd[newKey] = kwargs.pop(k) 
    tag = lxml_html.Element(*args, **kwargs)
    for k, v in attribToAdd.items():
        tag.set(k, v)
    
    if tagText is not None:
        if not parseTagText:
            tag.text = tagText
        else:
            parsedText, parsedChildren, parsedTail = parseAnonymousHTML(tagText, disp=disp)
            tag.text = parsedText
            parsedChildren[-1].tail += parsedTail
            tag.extend(parsedChildren)
            
    tag.extend(toAppend)
        
    return tag

        
def Div(**kwargs):
    return Tag('div', **kwargs)


def sanitize(s, lower=True, upper=True, nums=True, extra=''):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    allowed = ''
    if lower: allowed += alpha.lower()
    if upper: allowed += alpha.upper()
    if nums:  allowed += '1234567890'
    allowed += extra
    return ''.join(
        c for c in s if c in allowed
    )


def writePage(html, files, fname, fromPath, DEBUG=False):
    if DEBUG:
        print('Writing', html, 'to', fname, '...', end=' ')
    f = open(fname, 'w')
    f.write('<!DOCTYPE html>\n')
    f.write(tostring(html))
    f.close()
    if DEBUG:
        print('done.')

    dn = dirname(fname)        
    if DEBUG:
        print('Saving %d files from %s to %s.' % (len(files), fromPath, dn))
        
    for relpath in files:
        fr = join(fromPath, relpath)
        bn = basename(fr)
        to = join(dn, bn)
        if DEBUG:
            print('    Copying from %s to %s.' % (fr, to))
        copy(fr, to)
        

def showPage(fname, browser='google-chrome'):    
    from os import system
    system('%s "%s"' % (browser, fname))
    
    
def displayHtml(html, fname='/tmp/test.html', browser='google-chrome'):
    writePage(html, fname)
    if browser is not None:
        showPage(fname, browser)
       
        
def first(l):
    if len(l) > 0:
        return l[0]
    else:
        return None


def textField(name, label):
    field = Div(cls='mdl-textfield mdl-js-textfield mdl-textfield--floating-label')
    field.append(Tag('input', cls='mdl-textfield__input', type='text',
                     name=name,
                     id=name + '.id'))
    field.append(Tag('label', cls='mdl-textfield__label', for_=name + '.id', tagText=label))
    return field


def textArea(name, label, rows='3', **kwargs):
    rows = str(rows).strip()
    field = Div(cls='mdl-textfield mdl-js-textfield', style='width: 100%;')
    field.append(Tag('textarea', cls='mdl-textfield__input', type='text', rows=rows,
                     name=name,
                     id=name + '.id', **kwargs))
    field.append(Tag('label', cls='mdl-textfield__label', for_=name + '.id', tagText=label))
    return field
    