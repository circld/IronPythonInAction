import wpf

from System.Windows import Application, SizeToContent, Thickness, Window
from System.Windows.Controls import Button, Label, StackPanel
from System.Windows.Media.Effects import DropShadowBitmapEffect


class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'HelloWorld.xaml')
        self.button.Click += self.greet

    def greet(self, sender, event):
        message = Label()
        message.FontSize = 36
        message.Content = 'Welcome to IronPython!'
        self.Content.AddChild(message)


## The code below is same as above w/o reliance on XAML
#class MyWindow(Window):
#    def __init__(self):
#        # wpf.LoadComponent(self, 'HelloWorld.xaml')
#        self.Title = 'Welcome to IronPython'
#        self.SizeToContent = SizeToContent.Height
#        self.Width = 450

#        # initialize other components
#        self.__init_stack_panel()
#        self.__init_button()

#    def __init_stack_panel(self):
#        stack = StackPanel()
#        stack.Margin = Thickness(15)
#        self.Content = stack

#    def __init_button(self):
#        button = Button()
#        button.Content = 'Push Me'
#        button.FontSize = 24
#        button.BitmapEffect = DropShadowBitmapEffect()  # add the 3D shadow
#        button.Click += self.greet
#        self.Content.AddChild(button)

#    def greet(self, sender, event):
#        message = Label()
#        message.FontSize = 36
#        message.Content = 'Welcome to IronPython!'
#        self.Content.AddChild(message)

    
if __name__ == '__main__':
    Application().Run(MyWindow())
