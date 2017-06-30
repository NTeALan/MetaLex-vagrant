#! usr/bin/env python
# coding: utf8

"""
    Implémentation de détection de composants  des articles.
 
    
    Usage:
    >>> from MetaLex.dicOcrText import *
    >>> composeArticle()
"""

# ----Internal Modules------------------------------------------------------

import MetaLex
from   composeArticle import *

# ----External Modules------------------------------------------------------

import re, sys, codecs, os
from bs4    import BeautifulSoup
from random import sample
from shutil import copyfile

# -----Exported Functions-----------------------------------------------------

__all__ = ['xmlised', 'dicoHtml']

# -----Global Variables-----------------------------------------------------

components = {
                u'xml'  :   {
                              u'metadata'       : [u'projectname', u'author', u'date', u'comment', u'contributors'],
                              u'identification' : [u'article', u'entry', u'flexion', u'category', u'gender', u'rection', u'phonetic'], 
                              u'treatment'      : [u'definition', u'contextualisation', u'figured', u'contrary']
                            },
                u'tei'  :   {
                              u'metadata'       : [],
                              u'identification' : [], 
                              u'treatment'      : []
                            },
                u'lmf'  :   {
                              u'metadata'       : [],
                              u'identification' : [], 
                              u'treatment'      : []
                            },
                u'dtd'  :   [u'ELEMENT', u'ATTRIBUTE', u'PCDATA', u'CDATA', u'REQUIRED', u'IMPLIED'],
                u'xsd'  :   [],
                u'forms':   {
                             u'allfs'  : [u'.', u',', u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.', u'm.', u'f.', u'Fig.', u'tr.', u'intr.', u'interj.', u'art.', u'Firm.'],
                             u'cats'   : [u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.', u'interj.', u'art.', u'Firm.'],
                             u'genres' : [u'm.', u'f.', u'Fig.', u'tr.', u'intr.'],
                             u'flexs'  : [u'tr.', u'intr.']
                            },
                u'codif':   {
                             u'text'   : [u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.', u'm.', u'f.', u'Fig.', u'tr.', u'intr.', u'interj.', u'art.'],
                             u'graph'  : [u'.', u',', u':', u'-', u';'],
                             u'symb'   : [u'||', u'&#9830;', u'-', u'1.',u'2.',u'3.',u'4.',u'5.',u'6.',u'7.',u'8.',u'9.',u'a)',u'b)',u'c)',u'd)',u'e)',u'f)',u'g)',u'a.'],
                             u'typo'   : [u'I', u'G', u'B', u'P', u'']
                            }
             }

article = []
#Cauthor, Cname, Cdate, Ccomment = "", "", "",""

# ----------------------------------------------------------


def dataArticles(typ=u'pickle'):
    MetaLex.dicProject.createtemp()
    contentdir = os.listdir('.')
    filepickle = u''
    filetext   = u''
    for fil in contentdir :
        if fil.split('.')[1]   == u'pickle' :
            filepickle = fil 
        elif fil.split('.')[1] == u'art'    :
            filetext = fil
    if typ :
        datapickle = MetaLex.dicProject.fileUnpickle(filepickle)
        return datapickle
    if typ == u'text' :
        datatext = MetaLex.dicProject.fileGettext(filetext)
        return datatext



def xmlised(typ=u'xml', save=False) :
    metadata   = xmlMetadata()
    content    = xmlContent()
    if typ == u'xml' :
        if save :
            MetaLex.dicProject.createtemp()
            name = u'MetaLex-'+MetaLex.projectName+u'.xml'
            metalexxml = balise(metadata+content, u'MetaLexProject', typ=u'')
            if MetaLex.dicProject.inDir(name) :
                with codecs.open(name, 'w', 'utf-8') as fle :
                    fle.write(metalexxml)
                message = u"'"+name+u"'  is created and contain all dictionary articles formated in xml standard format > Saved in dicTemp folder"
                MetaLex.dicLog.manageLog.writelog(message)
            else:
                message = u"'"+name+u"'  is created and contain all dictionary articles formated in xml standard format > Saved in dicTemp folder"
                print message
                #MetaLex.dicLog.manageLog.writelog(message)
        else :
            metalexxml = balise(metadata+content, u'MetaLexProject', typ=u'')
            return metalexxml
        
    

def xmlMetadata(typ=u'xml'):
    MetaLex.dicProject.createtemp()
    if typ == u'xml' :
        projectconf = MetaLex.dicProject.readConf()
        author      = balise(projectconf['Author'], u'mtl:author', typ=u'')
        name        = balise(projectconf['Projectname'], u'mtl:projectname', typ=u'')
        date        = balise(projectconf['Creationdate'], u'mtl:date', typ=u'')
        comment     = balise(projectconf['Comment'], u'mtl:comment', typ=u'')
        contribtab  = projectconf['Contributors'].split(u',') if projectconf['Contributors'].find(u',') else projectconf['Contributors']
        contrib = ''
        if len(contribtab) > 1 :
            for data in contribtab :
                contrib += balise(data, u'mtl:pers', typ=u'') 
        else :
            contrib = balise(''.join(contribtab), u'mtl:pers ', typ=u'') 
        contrib = balise(contrib, u'mtl:contributors', typ=u'')
        cont    = name+author+date+comment+contrib
        content = balise(cont, u'mtl:metadata', typ=u'') 
        return content
        
        
def xmlContent(typ=u'xml'): 
    data    = dataArticles()
    content = u''
    result  = u''
    if typ == u'xml' :
        for dicart in data :
            for art in dicart.keys() :
                art = balise(dicart[art], u'mtl:article', typ=u'', art=True)
                content += art
        result = balise(content, u'mtl:content', typ=u'', art=True)
        return result

    
      
def buildStructure(data, typ=u'dtd'):
    return False


def dicoHtml(save=False) :
    MetaLex.dicPlugins
    filepath     = sys.path[-1]+u'/MetaLex-template.html'
    MetaLex.dicProject.createtemp()
    if MetaLex.dicProject.inDir('CopyMetaLexTemplate.html') :
        copyfile(filepath, 'CopyMetaLexTemplate.html')
        souphtl = htmlInject('CopyMetaLexTemplate.html')
        if save : 
            with codecs.open('MetaLexViewerEditor.html', 'w') as htmlresult :
                htmlresult.write(souphtl)
            os.remove('CopyMetaLexTemplate.html')
            message = u"'MetaLexViewerEditor.html' has correctly been generated > Saved in dicTemp folder" 
            MetaLex.dicLog.manageLog.writelog(message)
    else :
        souphtl = htmlInject('CopyMetaLexTemplate.html')
        if save : 
            with codecs.open('MetaLexViewerEditor.html', 'w') as htmlresult :
                htmlresult.write(souphtl)
            os.remove('CopyMetaLexTemplate.html')
            message = u"'MetaLexViewerEditor.html' has correctly been generated > Saved in dicTemp folder" 
            MetaLex.dicLog.manageLog.writelog(message)
    
    
def htmlInject(template):
    MetaLex.dicProject.createtemp()
    contentxml     = xmlised(typ=u'xml', save=False)
    projectconf    = MetaLex.dicProject.readConf()
    Hauthor, Hname, Hdate, Hcomment, Hcontrib = projectconf['Author'], projectconf['Projectname'], projectconf['Creationdate'], projectconf['Comment'], projectconf['Contributors']
    filetemplate   = codecs.open(template, 'r', 'utf-8')
    souphtml       = BeautifulSoup(filetemplate, "html5lib")
    content        = souphtml.find(u'div', attrs={'id': u'all-articles'}) 
    author         = content.find(u'h3', attrs={'id': u'author'})
    author.string  = 'main : '+Hauthor
    date           = content.find(u'h5', attrs={'id': u'date'})
    date.string    = Hdate
    descipt        = content.find(u'p', attrs={'id': u'description'})
    descipt.string = Hcomment
    contrib        = content.find(u'h4', attrs={'id': u'contributors'})
    contrib.string = 'contributors : '+Hcontrib
    project        = content.find(u'h4', attrs={'id': u'projetname'})
    project.string = Hname
    
    soupxml        = BeautifulSoup(contentxml, "html5lib")
    articlesxml    = soupxml.findAll(u'mtl:article')
    articleshtml   = souphtml.find(u'div', attrs={'id': u'mtl:articles'})
    for x in articlesxml : articleshtml.append(x)
    listlemme      = souphtml.find(u'ul', attrs={'id': u'list-articles'})
    for x in articlesxml :
        art     = x.get_text()
        id      = x.get('id')
        lem     = ' '.join(re.split(ur'(\s)',art)[0:3]) 
        lemme   = BeautifulSoup('<li class="w3-hover-light-grey" ><span class="lemme" onclick="changeImage('+"'"+id+"'"+')">'+lem+'</span><span class="fa fa-plus w3-closebtn" onclick="add('+"'"+id+"'"+')"/></li>', 'html5lib')
        listlemme.append(lemme)
        
    filetemplate.close()
    html = souphtml.prettify("utf-8")
    return html
    
        
        
def balise(element, markup, typ=u'xml', art=False):
    if type :
        if markup in components[u'xml'][u'identification'] \
        or components[u'xml'][u'treatment'] :
            if art :
                element = chevron(markup, art=True)+element+chevron(markup, False)
                return element
            else:
                element = chevron(markup)+element+chevron(markup, False)
                return element
    elif typ == u'tei' :
        if markup in components[u'tei'][u'identification'] \
        or components[u'xml'][u'treatment'] :
            if art :
                element = chevron(markup, art=True)+element+chevron(markup, False)
                return element
            else:
                element = chevron(markup)+element+chevron(markup, False)
                return element
    elif typ == u'lmf' :
        if markup in components[u'lmf'][u'identification'] \
        or components[u'xml'][u'treatment'] :
            if art :
                element = chevron(markup, art=True)+element+chevron(markup, False)
                return element
            else:
                element = chevron(markup)+element+chevron(markup, False)
                return element
    else :
        if art :
            element = chevron(markup, art=True)+element+chevron(markup, False)
            return element
        else:
            element = chevron(markup)+element+chevron(markup, False)
            return element
    

    
def generateMetadata():
    return False


    
def chevron(el, openchev=True, art=False):
    idart = generateID()
    if art :
        if openchev     : return u"<"+el+u" id='"+idart+u"' class='data-article'"+u">"
        if not openchev : return u"</"+el+u">"
    else :
        if openchev     : return u"<"+el+u">"
        if not openchev : return u"</"+el+u">"
    
    
def generateID():
    idart = sample([u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0',u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h',u'i',u'j',u'k',u'l',u'm',u'n',u'o',u'p',u'q',u'r',u's',u't',u'v',u'w',u'y',u'z'], k=5)
    return u''.join(idart)
    
    
    
    