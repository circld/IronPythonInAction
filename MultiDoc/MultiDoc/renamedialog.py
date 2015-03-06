import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Windows.Forms import (
    Button, DockStyle, DialogResult, Form,
    FormBorderStyle, Padding, Panel, TextBox
)
from System.Drawing import Size


class RenameTabDialog(Form):

    def __init__(self, name, rename):
        title = "Name Tab"
        if rename:
            title = 'Rename Tab'
        self.Text = title
        self.Size = Size(170, 85)
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.ShowInTaskbar = False  # don't want dialog to appear in taskbar
        self.Padding = Padding(5)

        self.initializeTextBox(name)
        self.initializeButtons()

    def initializeTextBox(self, name):
        self.textBox = TextBox()
        self.textBox.Text = name
        self.textBox.Width = 160
        self.Dock = DockStyle.Top

        self.Controls.Add(self.textBox)

    def initializeButtons(self):
        buttonPanel = Panel()
        buttonPanel.Height = 23
        buttonPanel.Dock = DockStyle.Bottom
        buttonPanel.Width = 170

        # define custom buttons
        acceptButton = Button()
        acceptButton.Text = 'OK'
        acceptButton.Width = 75
        acceptButton.Dock = DockStyle.Left
        acceptButton.DialogResult = DialogResult.OK
        self.AcceptButton = acceptButton  # link to form
        buttonPanel.Controls.Add(acceptButton)

        cancelButton = Button()
        cancelButton.Text = 'Cancel'
        cancelButton.Width = 75
        cancelButton.Dock = DockStyle.Right
        cancelButton.DialogResult = DialogResult.Cancel
        self.CancelButton = cancelButton  # link to form
        buttonPanel.Controls.Add(cancelButton)

        self.Controls.Add(buttonPanel)


def ShowDialog(name, rename):
    dialog = RenameTabDialog(name, rename)
    result = dialog.ShowDialog()
    dialog.Close()  # else remains hidden

    if result == DialogResult.OK:
        return dialog.textBox.Text


if __name__ == '__main__':
    print ShowDialog("Something", False)
    print ShowDialog("Something Else", True)
