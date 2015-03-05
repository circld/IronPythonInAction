import clr
clr.AddReference('System.Xml')

from System.Xml import (
    XmlException, XmlNodeType, XmlReader, XmlReaderSettings, IXmlLineInfo
)

# to deal with unrecognized elements
MISSING_HANDLERS = (None,) * 3


# to add line number/position methods to XmlReader
# nb. interfaces can be added through normal Python class inheritance
class XmlReader2(IXmlLineInfo, XmlReader):
    pass


class XmlDocumentReader(object):

    def __init__(self, elementHandlers):
        # _elementHandlers is dict mapping elem type -> handler
        # (always tuple of 3: start, contents, end tag)
        self._elementHandlers = elementHandlers

    def read(self, filename):
        settings = XmlReaderSettings()
        settings.IgnoreWhitespace = True
        reader = XmlReader2.Create(filename, settings)

        self._currentElement = None

        nodeTypeHandlers = {
            XmlNodeType.Element: self.onStartElement,
            XmlNodeType.EndElement: self.onEndElement,
            XmlNodeType.Text: self.onText
        }

        try:
            while reader.Read():
                nodeType = reader.NodeType
                handler = nodeTypeHandlers.get(nodeType)
                if handler:
                    handler(reader)
                else:
                    raise XmlException(
                        "invalid data at line %d" %
                        reader.LineNumber
                    )
        finally:
            reader.Close()  # close or file locked until garbage collection

    def onStartElement(self, reader):
        name = reader.Name
        self._currentElement = name

        attributes = {}
        while reader.MoveToNextAttribute():
            attributes[reader.Name] = reader.Value

        # if unknown/unhandled element, default to MISSING_HANDLERS
        startHandler = self._elementHandlers.get(name,
                                                 MISSING_HANDLERS)[0]
        if startHandler:
            startHandler(reader.LineNumber, attributes)
        else:
            raise XmlException(
                'invalid data at line %d' % reader.LineNumber()
            )

    def onText(self, reader):
        # text is not own element (nb. reader.Name = '')
        element = self._currentElement
        textHandler = self._elementHandlers.get(element,
                                                MISSING_HANDLERS)[1]
        if textHandler:
            textHandler(reader.LineNumber, reader.Value)

    def onEndElement(self, reader):
        endHandler = self._elementHandlers.get(reader.Name,
                                               MISSING_HANDLERS)[2]
        if endHandler:
            endHandler(reader.LineNumber)  # pass line # for error msgs
