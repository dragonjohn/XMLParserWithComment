import xml.etree.ElementTree as ET
import io
from HTMLParser import HTMLParser


class PCParser(ET.XMLTreeBuilder):
   def __init__(self):
       ET.XMLTreeBuilder.__init__(self)
       # assumes ElementTree 1.2.X
       self._parser.CommentHandler = self.handle_comment
       self._parser.ProcessingInstructionHandler = self.handle_pi
       self._target.start("document", {})

   def close(self):
       self._target.end("document")
       return ET.XMLTreeBuilder.close(self)

   def handle_comment(self, data):
       self._target.start(ET.Comment, {})
       self._target.data(data)
       self._target.end(ET.Comment)

   def handle_pi(self, target, data):
       self._target.start(ET.PI, {})
       self._target.data(target + " " + data)
       self._target.end(ET.PI)

def whatisthis(s):
    if isinstance(s, str):
        return "ordinary string"
    elif isinstance(s, unicode):
        return "unicode string"
    else:
        return "not a string"

parser = PCParser()
#self.tree = ET.parse(self.templateOut, parser=parser)
with open( 'abc.xml', 'r' ) as f:
    xml = ET.parse( f, parser = parser )
#ET.dump( xml )
xml_root = xml.getroot()
gcl_items = xml_root.findall(".//Item[@type='CompanyList']")
gcl_names = [item.text for item in gcl_items]
#print len(gcl_names)
#print gcl_names

htmlParser = HTMLParser()
idx = 0
gcl_comments = []
with open( 'abc.xml', 'r' ) as f:
    line1 = f.readline().decode('utf-8')
    while(True):
        line2 = f.readline().decode('utf-8')
        target = '<Item type="CompanyList">'+gcl_names[idx]+'</Item>'
        line = htmlParser.unescape(line2.strip())
        print "target: "+target
        print "target encode: "+ whatisthis(target)
        print "line: "+line
        print "line encode: "+ whatisthis(line)
        if target in line:
            if line1.strip().startswith('<!--'):
                print line1.strip().startswith('<!--'), line1.strip()
                gcl_comments = gcl_comments + [(line1.strip().encode('utf-8'))[4:-3]]
            else:
                gcl_comments = gcl_comments + [None]
            idx = idx + 1
        line1 = line2
        if not line2 or len(gcl_names) <= idx:
            break
print len(gcl_names)
print len(gcl_comments)
print gcl_names
print gcl_comments