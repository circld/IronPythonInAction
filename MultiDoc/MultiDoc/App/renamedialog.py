from os import getcwd
from os.path import join

import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
# apparently doesn't check __file__ directory for DLL's
clr.AddReferenceToFileAndPath(join(getcwd(), 'RenameTabDialog.dll'))

from RenameTabDialog import RenameTabDialogBase
from System.Windows.Forms import (
    Button, DockStyle, DialogResult, Form,
    FormBorderStyle, Padding, Panel, TextBox
)
from System.Drawing import Size


class RenameTabDialog(RenameTabDialogBase):

    def __init__(self, name, rename):
        RenameTabDialogBase.__init__(self)

        title = "Name tab"
        if rename:
            title = "Rename Tab"
        self.Text = title
        self.textBox.Text = name


def ShowDialog(name, rename):
    dialog = RenameTabDialog(name, rename)
    result = dialog.ShowDialog()
    dialog.Close()  # else remains hidden

    if result == DialogResult.OK:
        return dialog.textBox.Text


if __name__ == '__main__':
    print ShowDialog("Something", False)
    print ShowDialog("Something Else", True)
