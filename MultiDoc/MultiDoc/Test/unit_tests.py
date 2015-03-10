import unittest as ut
from assemblies import *
from App.opencommands import OpenCommand


class Listener(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.returnVal = None
        self.triggered = False
        self.triggerArgs = None
        self.triggerKwargs = None

    def __call__(self, *args, **kwargs):
        self.triggered = True
        self.triggerArgs = args
        self.triggerKwargs = kwargs
        return self.returnVal


class Mock(object):
    pass


class MockDialog(object):

    def __init__(self):
        self.InitialDirectory = None
        self.FileName = None
        self.returnVal = DialogResult.Cancel

    def ShowDialog(self):
        return self.returnVal


class test_OpenFileDialog(ut.TestCase):

    def setUp(self):
        mainform = Mock()
        document = Mock()
        document.fileName = None
        mainform.document = document

        self.command = OpenCommand(mainform)
        self.command.openFileDialog = MockDialog()  # override openFileDialog

    def test_execute_should_set_filename_and_initial_directory_on_dialog(self):
        # user cancels out of dialog
        self.command.execute()
        self.assertIsNone(self.command.openFileDialog.FileName,
                          "FileName incorrectly set (None).")

        # user 'selects' a file
        self.command.mainForm.document.fileName = __file__
        self.command.execute()
        self.assertEquals(self.command.openFileDialog.FileName,
                          __file__,
                          "FileName incorrectly set (not None).")
        self.assertEquals(self.command.openFileDialog.InitialDirectory,
                          Path.GetDirectoryName(__file__),
                          "InitialDirectory incorrectly set.")

    def test_execute_should_not_call_getDocument_for_cancelled_dialog(self):
        # monkey-patching example
        listener = Listener()
        self.command.getDocument = listener  # override getDocument

        self.command.execute()
        self.assertFalse(listener.triggered, 'getDocument called incorrectly')

    def test_execute_should_call_getDocument_for_accepted_dialog(self):
        listener = Listener()
        self.command.getDocument = listener
        
        originalDocument = self.command.mainForm.document
        self.command.mainForm.document.fileName = __file__
        self.command.openFileDialog.returnVal = DialogResult.OK
        self.command.execute()
        self.assertEquals(listener.triggerArgs, (__file__,),
                          'getDocument not called with filename')
        self.assertEquals(self.command.openFileDialog.InitialDirectory,
                          Path.GetDirectoryName(__file__),
                          'InitialDirectory incorrectly set.')
        self.assertEquals(self.command.mainForm.document,
                          originalDocument,
                          'document incorrectly changed.')

    def test_new_document_from_getDocument_should_be_set_on_mainForm(self):
        listener = Listener()
        self.command.getDocument = listener
        
        self.command.mainForm.document.fileName = __file__
        self.command.openFileDialog.returnVal = DialogResult.OK
        newDocument = object()
        listener.returnVal = newDocument
        self.command.execute()
        self.assertEquals(self.command.mainForm.document,
                          newDocument,
                          'document not replaced')


if __name__ == '__main__':
    ut.main()
