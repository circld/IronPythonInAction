import clr
clr.AddReference('System.Xml')

from System.Xml import XmlWriter, XmlWriterSettings


class DocumentWriter(object):

    def __init__(self, fileName):
        self.fileName = fileName

    def write(self, document):
        settings = XmlWriterSettings()  # configs XML settings
        settings.Indent = True
        settings.IndentChars = '    '
        settings.OmitXmlDeclaration = True
        # pass filename to XmlWriter.Create to create & write to file
        writer = XmlWriter.Create(self.fileName, settings)

        def writePage(page):
            # refer to model in MultiDoc.py for Page properties
            writer.WriteStartElement('page')
            writer.WriteAttributeString('title', page.title)
            writer.WriteString(page.text)
            writer.WriteEndElement()

        writer.WriteStartDocument()
        writer.WriteStartElement('document')

        [writePage(page) for page in document]

        writer.WriteEndElement()
        writer.WriteEndDocument()
        writer.Flush()  # write existing contents of buffer (w/o closing)
        writer.Close()
