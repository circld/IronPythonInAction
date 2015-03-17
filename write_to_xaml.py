# need wpf for XamlWriter to be accessible in System.Windows.Markup
import wpf
from System.IO import File
from System.Windows import Window, SizeToContent, Application
from System.Windows.Markup import XamlWriter
from System.Windows.Controls import Button, WrapPanel


class ControlsExample(Window):

    def __init__(self):
        self.SizeToContent = SizeToContent.WidthAndHeight
        self.button = self.init_button()
        self.Content = WrapPanel()
        self.Content.AddChild(self.button)
        
    def init_button(self): 
        button = Button()
        button.Content = 'Push me please'
        button.Height = 20
        button.Width = 120
        return button


if __name__ == '__main__':
    #Application().Run(ControlsExample())
    window = ControlsExample()
    # cannot save subclass, so drop down a level to contents
    text = XamlWriter.Save(window.Content)
    File.WriteAllText('out.xaml', text)
