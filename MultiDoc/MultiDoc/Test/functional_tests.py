import clr
clr.AddReference('IronPython')

import unittest as ut
from assemblies import Application, Directory, Form, Path, MessageBox
from System.Threading import (
    ApartmentState, ManualResetEvent, Thread, ThreadStart, Timeout
)
from IronPython.Compiler import CallTarget0
from MultiDoc.App.MultiDoc import MyForm


# launches invoke from third thread to avoid blocking while waiting
# for Invoke to return.
class AsyncExecutor(object):

    def __init__(self, function):
        self.result = None
        startEvent = ManualResetEvent(False)

        def StartFunction():
            startEvent.Set()
            self.result = function()

        self._thread = Thread(ThreadStart(StartFunction))
        self._thread.Start()
        startEvent.WaitOne()
    
    def join(self, timeout=Timeout.Infinite):
        return self._thread.Join(timeout)


class FunctionalTest(ut.TestCase):

    def setUp(self):
        self.mainForm = None
        self._thread = Thread(ThreadStart(self.startMultiDoc))        
        self._thread.SetApartmentState(ApartmentState.STA)
        self._thread.Start()

        while self.mainForm is None:
            Thread.CurrentThread.Join(100)

    def startMultiDoc(self):
        fileDir = Path.GetDirectoryName(__file__)
        executableDir = Directory.GetParent(fileDir).FullName

        self.mainForm = MyForm()
        Application.Run(self.mainForm)

    def tearDown(self):
        self.invoke_on_gui_thread(lambda : self.mainForm.Close())

    def invoke_on_gui_thread(self, function):
        return self.mainForm.Invoke(CallTarget0(function))

    def executeAsynchronously(self, function):
        def AsyncFunction():
            return self.invoke_on_gui_thread(function)
        executor = AsyncExecutor(AsyncFunction)
        return executor


class NewPageTest(FunctionalTest):

    def clickNewPageButton(self):
        button = self.mainForm.toolBar.Items[1]
        executor = self.executeAsynchronously(
            lambda : button.PerformClick()
        )
        Thread.CurrentThread.Join(200)  # delay for dialog to appear
        return executor

    def test_new_page_dialog(self):
        # * Harold opens MultiDoc
        # * He clicks on the 'New Page' toolbar button
        executor = self.clickNewPageButton()

        #* A dialog called 'Name Tab' appears
        dialog = self.invoke_on_gui_thread(
            lambda : Form.ActiveForm
        )
        title = self.invoke_on_gui_thread(
            lambda : dialog.Text
        )
        self.assertEquals(title, "Name tab",
                          "Incorrect dialog name.")

        #* Harold changes his mind, so he selects cancel
        self.invoke_on_gui_thread(
            lambda : dialog.CancelButton.PerformClick()
        )
        executor.join()


if __name__ == '__main__':
    ut.main()