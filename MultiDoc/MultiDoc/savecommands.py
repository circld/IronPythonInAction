from System.Windows.Forms import SaveFileDialog, DialogResult
from System.IO import Directory, Path
from documentwriter import DocumentWriter


filter = 'Text files (*.txt)|*.txt|All files (*.*)|*.*'

class SaveCommand(object):

    title = 'Save Document'

    def __init__(self, tabController):
        self.document = None
        self.tabController = tabController
        self.saveDialog = SaveFileDialog()
        self.saveDialog.Filter = filter
        self.saveDialog.Title = self.title

    def execute(self):
        fileName = self.document.fileName
        text = self.getUpdatedDocument()

        directory = Path.GetDirectoryName(fileName)
        directoryExists = Directory.Exists(directory)
        if fileName is None or not directoryExists:
            self.promptAndSave(text)
        else:
            self.saveFile(fileName, text)

    def getUpdatedDocument(self):
        self.tabController.updateDocument()
        return self.document

    def promptAndSave(self, text):
        saveDialog = self.saveDialog
        if saveDialog.ShowDialog() == DialogResult.OK:
            fileName = saveDialog.FileName
            if self.saveFile(fileName, text):
                self.document.fileName = fileName

    def saveFile(self, fileName, text):
        try:
            writer = DocumentWriter(fileName)
            writer.write(text)
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
        text = self.getUpdatedDocument()
        ' If fileName exists, set initial dialog directory to fileName directory'
        if fileName is not None:
            name = Path.GetFileName(fileName)
            directory = Path.GetDirectoryName(fileName)
            self.saveDialog.InitialDirectory = directory
        self.promptAndSave(text)

