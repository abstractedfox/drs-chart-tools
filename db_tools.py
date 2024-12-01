import database_xml_interface
import xml.etree.ElementTree

class Database:
    def __init__(self, xml:xml.etree.ElementTree.Element = None):
        self.xml = xml
    #incomplete!
