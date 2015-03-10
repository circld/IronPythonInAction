import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython')

from System.Windows.Forms import Application, Form
from System.Threading import ApartmentState, Thread, ThreadStart
from IronPython.Compiler import CallTarget0


class Something(object):
    started = False
    form = None

something = Something()

def StartEventLoop():
    f = Form()
    f.Text = 'A Windows Forms Form'
    f.Show()
    something.form = f  # stores reference to form
    something.started = True
    Application.Run(f)

thread = Thread(ThreadStart(StartEventLoop))
thread.SetApartmentState(ApartmentState.STA)  # Single Threaded Apartment
thread.Start()

# time for form to appear
while not something.started:
    Thread.CurrentThread.Join(100)  # what does Join do?

def GetFormTitle():
    title = something.form.Text
    return title

title = something.form.Invoke(CallTarget0(GetFormTitle))
print title

# CallTarget0(something.form.Close) doesn't work
# apparently does not work when method has void return signature
# http://lists.ironpython.com/pipermail/users-ironpython.com/2009-June/025456.html
Thread.Sleep(3000)
delegate = CallTarget0(lambda : something.form.Close())
something.form.Invoke(delegate)