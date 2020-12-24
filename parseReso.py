from docx2python import docx2python
from Resolution import Resolution

doc = docx2python('Mock Resolution.docx', html = True)
print(doc.text)

reso = Resolution(doc.text)






##import docx
##
##doc = docx.Document("Mock Resolution.docx")
##paras = doc.paragraphs
##
##for p in paras:
##    print("style: " + p.style.name + " | text: " + p.text[:20])
##    print("-----")
##
##print(paras[12].runs[0].text)
##
##def test():
##    print(paras[12].runs[0].text)
#print(paras[12].style)


##import zipfile
##import xml.dom.minidom


##d = zipfile.ZipFile('./Mock Resolution.docx')
##uglyXml = xml.dom.minidom.parseString(d.read('word/numbering.xml')).toprettyxml(indent='  ')
##
##with open('numbering.xml', 'w') as f:
##    f.write(uglyXml)
##
##import xml.etree.ElementTree as ET
##
##tree = ET.parse('document.xml')
##root = tree.getroot()
##w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
##
##for p in root[0].findall(w + 'p'):
##    for ppr in p.findall(w + 'pPr'):
##        for numpr in ppr.findall(w + 'numPr'):
##            print(numpr.find(w + 'ilvl').attrib)
##

    
