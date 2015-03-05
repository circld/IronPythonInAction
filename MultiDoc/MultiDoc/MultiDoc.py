# Button icons (C) 2013 Yusuke Kamiyamane. All rights reserved.

import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import Bitmap, Color, Size
from System.IO import Path
from System.Windows.Forms import (
    Application, DockStyle, Form, 
    Keys, MenuStrip, TabAlignment, TabControl, 
    ToolStripItemDisplayStyle, ToolStrip,
    ToolStripButton, ToolStripGripStyle,
    ToolStripMenuItem,
)

# import other from other user-written modules
from model import Document
from opencommands import OpenCommand
from savecommands import SaveCommand, SaveAsCommand
from tabcontroller import TabController


executablePath = __file__  # this file's path
if executablePath is None:
    executablePath = Application.ExecutablePath
executableDirectory = Path.GetDirectoryName(executablePath)


class MyForm(Form):

    def __init__(self):
        self.Text = 'MultiDoc Editor'
        self.MinimumSize = Size(150, 150)

        tab = self.tabControl = TabControl()
        self.tabControl.Dock = DockStyle.Fill
        self.tabControl.Alignment = TabAlignment.Bottom
        self.Controls.Add(self.tabControl)

        # all interaction with Document via controller
        self.tabController = TabController(tab)

        # initializing form components using class methods
        self.initializeCommands()
        self.initializeToolbar()
        self.initializeMenus()
        self.initializeObservers()
        self.document = Document()

    def initializeCommands(self):
        tabC = self.tabController
        self.saveCommand = SaveCommand(tabC)
        self.saveAsCommand = SaveAsCommand(tabC)
        self.openCommand = OpenCommand(self)

    def initializeToolbar(self):
        self.iconPath = Path.Combine(executableDirectory, 'icons', 'icons')
        self.toolBar = ToolStrip()  # Toolbar (.NET 1.0) is apparently garbage
        self.toolBar.Dock = DockStyle.Top
        self.toolBar.GripStyle = ToolStripGripStyle.Hidden
        
        self.addToolbarItem('Open', 
                            lambda sender, event : self.openCommand.execute(),
                            'folder-open.png')
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

        openKeys = Keys.Control | Keys.O
        openMenuItem = self.createMenuItem(
            '&Open...',
            handler=lambda sender, event : self.openCommand.execute(),
            keys=openKeys
        )

        saveKeys = Keys.Control | Keys.S
        saveMenuItem = self.createMenuItem(
            '&Save...',
            handler=lambda sender, event : self.saveCommand.execute(),
            keys=saveKeys
        )

        saveAsKeys = Keys.Control | Keys.Shift | Keys.S
        saveAsMenuItem = self.createMenuItem(
            'S&ave As...',
            handler=lambda sender, event : self.saveAsCommand.execute(),
            keys=saveAsKeys
        )

        # Add menu items to menu, menu to menus
        fileMenu.DropDownItems.Add(openMenuItem)
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

    def initializeObservers(self):
        self.observers = [
            self.saveCommand,
            self.saveAsCommand,
            self.tabController
        ]

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, document):
        self._document = document
        for observer in self.observers:
            observer.document = document


Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MyForm()
Application.Run(form)
