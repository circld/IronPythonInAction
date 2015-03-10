import unittest as ut
from assemblies import *
from App.opencommands import OpenCommand


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
        self.command.openFileDialog = MockDialog()

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


if __name__ == '__main__':
    ut.main()
