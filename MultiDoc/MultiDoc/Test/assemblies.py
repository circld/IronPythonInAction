import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import Bitmap, Color, Icon, Size
from System.IO import Path, Directory
from System.Windows.Forms import (
    Application, Button, DialogResult, DockStyle, 
    Form, FormBorderStyle, Keys, MenuStrip, 
    Padding, Panel, ScrollBars, TabAlignment,
    TabPage, TabControl, TextBox,
    ToolStripItemDisplayStyle, ToolStrip,
    ToolStripButton, ToolStripGripStyle,
    ToolStripMenuItem,
)