"""
This example follows the ControlsExample in Iron Python In Action 9.2.1 onwards
but implements the visual elements using XAML, retaining only application logic
in Python code.
"""
import wpf
import os

from System import Uri, UriKind
from System.Windows import (
    Application, CornerRadius, HorizontalAlignment, MessageBox,
    SizeToContent, Thickness, Window
)
from System.Windows.Controls import (
    Border, CheckBox, ColumnDefinition, ComboBox, ComboBoxItem, Grid, Image,
    Label, RowDefinition, ToolTip
)
from System.Windows.Media import Brushes
from System.Windows.Input import Cursors
from System.Windows.Media.Imaging import BitmapImage
from System.Windows.Documents import Run


class MyWindow(Window):
    
    def __init__(self):
        wpf.LoadComponent(self, 'GridExample.xaml')
        self.set_grid_child()
        self.init_combobox_vals()
        self.init_handlers()
        self.config_image(self.image, 'image.bmp')

    def set_grid_child(self):
        'Convenience method for setting grid child properties'
        for child in self.main_grid.Children:
            child.Margin = Thickness(15)
            child.Cursor = Cursors.Hand

    def init_combobox_vals(self):
        choices = (
            'Choice 1', 'Choice 2', 'Choice 3'
        )
        [self.combo.Items.Add(ComboBoxItem(Content=ch)) for ch in choices]

    def init_handlers(self):
        toggle_check_lab = toggle_msg(self.check, self.check_lab)
        self.check.Checked += toggle_check_lab
        self.check.Unchecked += toggle_check_lab

        toggle_combo_lab = toggle_msg(self.combo, self.combo_lab)
        self.combo.SelectionChanged += toggle_combo_lab
        
        disp_push_me_msg = display_msg(self.push_me_lab, 'Push Me! button was clicked.')
        self.push_me.Click += disp_push_me_msg

        #disp_hyperlink_msg = display_msg(self.text_box, 'Hyperlink clicked')
        #self.hyperlink.Click += disp_hyperlink_msg
        disp_text_box_append_msg = append_msg(self.text_box, 
                                              ' The hyperlink was clicked.')
        self.hyperlink.Click += disp_text_box_append_msg

    def config_image(self, image, fname):
        bi = BitmapImage()
        bi.BeginInit()
        image_uri = os.path.join(os.path.dirname(__file__), fname)
        bi.UriSource = Uri(image_uri, UriKind.RelativeOrAbsolute)
        bi.EndInit()
        image.Source = bi


def toggle_msg(UI_obj, UI_lab):
    """
    Reusable handler generator for printing messages to labels
    relying on ducktyping
    """
    if hasattr(UI_obj, 'IsChecked'):
        prop = 'IsChecked'
    elif hasattr(UI_obj, 'SelectedIndex'):
        prop = 'SelectedIndex'
    else:
        raise TypeError('%s is not supported in toggle_msg' % type(UI_obj))

    def msg_func(sender, event):
        msg = '%s %s = %s' % (UI_obj.__class__,
                              prop,
                              getattr(UI_obj, prop))
        UI_lab.Content = msg
    return msg_func


def display_msg(UI_lab, msg):
    
    def msg_func(sender, event):
        if hasattr(UI_lab, 'Text'):
            UI_lab.Text = msg
        elif hasattr(UI_lab, 'Content'):
            UI_lab.Content = msg
        else:
            MessageBox.Show(
                '%s has no Text or Content property\r\nMessage: %s' %
                (UI_lab.__class__, msg)
            )

    return msg_func


def append_msg(UI_lab, msg):

    def msg_func(sender, event):
        UI_lab.Inlines.Add(Run(msg))
    return msg_func


if __name__ == '__main__':
    Application().Run(MyWindow())
