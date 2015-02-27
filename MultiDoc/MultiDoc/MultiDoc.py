import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import Size
from System.Windows.Forms import (
    Application, DockStyle, Form, ScrollBars,
    TabAlignment, TabControl, TabPage, TextBox,
    SaveFileDialog, MessageBox, MessageBoxButtons,
    MessageBoxIcon
)
from System.IO import Directory, Path, StreamWriter

# Model
class Document(object):

    def __init__(self, fileName=None):
        self.fileName = fileName
        self.pages = list()
        self.addPage()

    def addPage(self, title='New Page'):
        page = Page(title)
        self.pages.append(page)

    def __getitem__(self, index):
        # nb. get __iter__ for free
        return self.pages[index]

    def __setitem__(self, index, page):
        self.pages[index] = page

    def __delitem__(self, index):
        del self.pages[index]


class Page(object):

    def __init__(self, title):
        self.title = title
        self.text = ''


# View
class MyForm(Form):

    def __init__(self):
        self.Text = 'MultiDoc Editor'
        self.MinimumSize = Size(150, 150)

        self.tabControl = TabControl()
        self.tabControl.Dock = DockStyle.Fill
        self.tabControl.Alignment = TabAlignment.Bottom
        self.Controls.Add(self.tabControl)

        self.document = Document()
        # all interaction with Document via controller
        self.tabController = TabController(self.tabControl, self.document)


# Controller
class TabController(object):
    """Connects tabControl and Document"""

    def __init__(self, tabControl, document):
        self.tabControl = tabControl  # link to view
        self.document = document  # link to model

        [self.addTabPage(page.title, page.text) for page in self.document]
        
        self.index = self.tabControl.SelectedIndex
        # selects first index (before form shown, index = -1 & 
        # SelectedIndexChanged event not fired)
        if self.index == -1:
            self.index = self.tabControl.SelectedIndex = 0  
        self.tabControl.SelectedIndexChanged += self.maintainIndex

    def addTabPage(self, label, text):
        """Adds a tabbed page"""
        tabPage = TabPage()
        tabPage.Text = label

        textBox = TextBox()
        textBox.Multiline = True
        textBox.Dock = DockStyle.Fill
        textBox.ScrollBars = ScrollBars.Vertical
        textBox.AcceptsReturn = True
        textBox.AcceptsTab = True
        textBox.WordWrap = True
        textBox.Text = text

        tabPage.Controls.Add(textBox)  # add textbox to tabPage control
        self.tabControl.TabPages.Add(tabPage)  # add tabPage to tabControl.TabPages

    def maintainIndex(self, sender, event):
        self.updateDocument()
        self.index = self.tabControl.SelectedIndex

    def updateDocument(self):
        """
        Records text from currently selected tab back into model
        """
        index = self.index
        tabPage = self.tabControl.TabPages[index]
        textBox = tabPage.Controls[0]  # nb. python style subsetting
        self.document[index].text = textBox.Text

# Commands
filter = 'Text files (*.txt)|*.txt|All files (*.*)|*.*'
class SaveCommand(object):

    title = 'Save Document'

    def __init__(self, document, tabController):
        self.document = document
        self.tabController = tabController
        self.saveDialog = SaveFileDialog()
        self.saveDialog.Filter = filter
        self.saveDialog.Title = self.title

    def execute(self):
        fileName = self.document.fileName
        text = self.getText()

        directory = Path.GetDirectoryName(fileName)
        directoryExists = Directory.Exists(directory)
        if fileName is None or not directoryExists:
            self.promptAndSave(text)
        else:
            self.saveFile(fileName, text)

    def getText(self):
        self.tabController.updateDocument()
        return self.document[0].text

    def promptAndSave(self, text):
        saveDialog = self.saveDialog
        if saveDialog.ShowDialog() == DialogResult.OK:
            fileName = saveDialog.FileName
            if self.saveFile(fileName, text):
                self.document.fileName = filename

    def saveFile(self, fileName, text):
        try:
            writer = StreamWriter(fileName)
            writer.Write(text)
            writer.Close()
            return True
        except IOError, e:
            name = Path.GetFileName(fileName)
            MessageBox.Show(
                'Could not write file %s\r\nThe error was:\r\n%s' %
                (name, e),
                'Error Saving File',
                MessageBoxButtons.OK,
                MessageBoxIcon.Error
            )
            return False


class SaveAsCommand(SaveCommand):

    title = "Save Document As"

    def execute(self):
        fileName = self.document.fileName
        text = self.getText()
        ' If fileName exists, set initial dialog directory to fileName directory'
        if fileName is not None:
            name = Path.GetFileName(fileName)
            directory = Path.GetDirectoryName(fileName)
            self.saveDialog.InitialDirectory = directory
        self.promptAndSave(text)


Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MyForm()
Application.Run(form)
