# Button icons (C) 2013 Yusuke Kamiyamane. All rights reserved.


import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import Bitmap, Color, Size
from System.Windows.Forms import (
    Application, DockStyle, Form, 
    Keys, MenuStrip, MessageBox, MessageBoxButtons,
    MessageBoxDefaultButton, MessageBoxIcon,
    ScrollBars, TabAlignment, 
    TabControl, TabPage, TextBox,
    ToolStripItemDisplayStyle, ToolStrip,
    ToolStripButton, ToolStripGripStyle,
    ToolStripMenuItem,
)
from System.IO import Directory, Path
# import other from other user-written modules
from savecommands import SaveCommand, SaveAsCommand

executablePath = __file__
if executablePath is None:
    Application.ExecutablePath
executableDirectory = Path.GetDirectoryName(executablePath)

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

        tab = self.tabControl = TabControl()
        self.tabControl.Dock = DockStyle.Fill
        self.tabControl.Alignment = TabAlignment.Bottom
        self.Controls.Add(self.tabControl)

        doc = self.document = Document()
        # all interaction with Document via controller
        self.tabController = TabController(self.tabControl, self.document)

        # initializing form components using class methods
        self.initializeCommands()
        self.initializeToolbar()
        self.initializeMenus()

    def initializeCommands(self):
        tabC = self.tabController
        doc = self.document
        self.saveCommand = SaveCommand(doc, tabC)
        self.saveAsCommand = SaveAsCommand(doc, tabC)

    def initializeToolbar(self):
        self.iconPath = Path.Combine(executableDirectory, 'icons', 'icons')
        self.toolBar = ToolStrip()  # Toolbar (.NET 1.0) is apparently garbage
        self.toolBar.Dock = DockStyle.Top
        self.toolBar.GripStyle = ToolStripGripStyle.Hidden
        
        self.addToolbarItem('Save', 
                            lambda sender, event : self.saveCommand.execute(),
                            'disk-black.png')
        self.Controls.Add(self.toolBar)

    def addToolbarItem(self, name, clickHandler, iconFile):
        button = ToolStripButton()
        button.ToolTipText = name
        button.Image = Bitmap(Path.Combine(self.iconPath, iconFile))
        button.ImageTransparentColor = Color.Magenta
        button.DisplayStyle = ToolStripItemDisplayStyle.Image
        button.Click += clickHandler

        # add button to toolbar
        self.toolBar.Items.Add(button)

    def initializeMenus(self):
        menuStrip = MenuStrip()
        menuStrip.Dock = DockStyle.Top

        fileMenu = self.createMenuItem('&File')

        saveKeys = Keys.Control | Keys.S
        saveMenuItem = self.createMenuItem(
            '&Save...',
            handler = lambda sender, event : self.saveCommand.execute(),
            keys=saveKeys
        )

        saveAsKeys = Keys.Control | Keys.Shift | Keys.S
        saveAsMenuItem = self.createMenuItem(
            'S&ave As...',
            lambda sender, event : self.saveAsCommand.execute(),
            saveAsKeys
        )

        # Add menu items to menu, menu to menus
        fileMenu.DropDownItems.Add(saveMenuItem)
        fileMenu.DropDownItems.Add(saveAsMenuItem)
        menuStrip.Items.Add(fileMenu)

        # Add to form controls
        self.Controls.Add(menuStrip)


    def createMenuItem(self, text, handler=None, keys=None):
        """ 
        Creates both menus (fileMenu) and menu items (saveMenuItem);
        hence the need for default values
        """
        menuItem = ToolStripMenuItem()
        menuItem.Text = text

        # logic for menu dropdown item
        if keys:
            menuItem.ShortcutKeys = keys
        if handler:
            menuItem.Click += handler

        # return rather than add since function is used for both menus & menu
        # items (logic differs from addToolbarItem() above)
        return menuItem


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


Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MyForm()
Application.Run(form)
