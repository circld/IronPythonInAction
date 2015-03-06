from System.Windows.Forms import DockStyle, ScrollBars, TabPage, TextBox

class TabController(object):
    """Connects tabControl and Document"""

    def __init__(self, tabControl):
        self.tabControl = tabControl  # link to view
        self._document = None  # populated by observer method

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, document):
        if self._document is not None:
            self.tabControl.SelectedIndexChanged -= self.maintainIndex

        self._document = document
        self.tabControl.TabPages.Clear()  # clears pages as prep for adding

        [self.addTabPage(page.title, page.text) for page in document]
        self.index = self.tabControl.SelectedIndex
        if self.index == -1:
            self.index = self.tabControl.SelectedIndex = 0
        self.tabControl.SelectedIndexChanged += self.maintainIndex

    @property
    def hasPages(self):
        return self.tabControl.SelectedIndex != -1  # index = -1 if no pages

    @property
    def title(self):
        if self.hasPages:
            index = self.tabControl.SelectedIndex
            return self.document.pages[index].title

    @title.setter
    def title(self, title):
        if self.hasPages:
            index = self.tabControl.SelectedIndex
            page = self.document.pages[index]
            page.title = title
            self.tabControl.SelectedTab.Text = title

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
        if self.hasPages:
            self.updateDocument()  # save currently selected page to model
        self.index = self.tabControl.SelectedIndex

    def updateDocument(self):
        """
        Records text from currently selected tab back into model
        """
        index = self.index
        tabPage = self.tabControl.TabPages[index]
        textBox = tabPage.Controls[0]  # nb. python style subsetting
        self.document[index].text = textBox.Text

    def deletePage(self):
        if self.hasPages:
            index = self.tabControl.SelectedIndex
            del self.document[index]  # remove page from model
            tabPage = self.tabControl.SelectedTab
            self.tabControl.TabPages.Remove(tabPage)  # remove from view
