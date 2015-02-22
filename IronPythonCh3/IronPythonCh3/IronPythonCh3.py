import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *
from System import Array, Random


class MyForm(Form):
    def __init__(self):
        self.rand_gen = Random()
        # Create child controls and initialize form
        self.labels = [Label(), Label()]
        bounds = ((5, 5, 200, 20), (5, 30, 200, 20))
        self.__config_labels(bounds)
        self.Text = 'Wowie Zowie'

        # add controls to form
        # list != Array (array can only contain obj of one type)
        self.Controls.AddRange(Array[Label](self.labels))  # AddRange vs Add

    def __config_labels(self, BoundList):
        # create font
        self.font_style = Font("Verdana", 11, FontStyle.Bold | FontStyle.Strikeout)

        for lab, bounds in zip(self.labels, BoundList):
            lab.SetBounds(*bounds)  # bounds = tuple, so unpack
            lab.Text = 'Hi there, Earth' 
            lab.ForeColor = Color.Crimson
            lab.BackColor = Color.AliceBlue
            lab.BorderStyle = BorderStyle.Fixed3D
            lab.Font = self.font_style
            lab.MouseEnter += self.__mouse_enter
            lab.MouseLeave += self.__mouse_leave

    def __mouse_enter(self, sender, event):
        rand_colors = [self.rand_gen.Next(0, 255) for i in xrange(6)]
        sender.ForeColor = Color.FromArgb(*rand_colors[:3])
        sender.BackColor = Color.FromArgb(*rand_colors[3:])
        sender.Font = Font('Verdana', 11, FontStyle.Bold)

    def __mouse_leave(self, sender, event):
        sender.ForeColor = Color.Crimson
        sender.BackColor = Color.AliceBlue
        sender.Font = self.font_style

Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MyForm()

Application.Run(form)
