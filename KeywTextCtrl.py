""" modified TextCtrl class.
Provides spellchecking while typing functionality"""

__version__ = '10.01.2023'
__author__ = 'Serhiy Kobyakov'


import wx
import enchant



class MyTarget(wx.TextDropTarget):
    def __init__(self, obj):
        wx.TextDropTarget.__init__(self)
        self.object = obj

    def OnDropText(self, x, y, data):
        # print(f"OnDropText have text: -{data}-")
        # add a space before the dropped word to ensure it would not attached directly to the previous one
        self.object.AppendText(" ")
        return True


class KeywTextCtrl(wx.TextCtrl):
    """TextCtrl with spellcheck"""
    def __init__(self, parent, the_id, **kwargs):
        default_kwargs = {'wrap': False, 'allowComma': False, 'name': ''}
        kwargs = default_kwargs | kwargs
        self.allow_comma = kwargs['allowComma']
        self.need_spell_check_while_type = False
        wx.TextCtrl.__init__(self, parent=parent, id=the_id, style=wx.TE_MULTILINE, name=kwargs['name'])
        if kwargs['wrap']:
            self.SetWindowStyle(wx.TE_MULTILINE | wx.TE_WORDWRAP)

        self.SetDropTarget(MyTarget(self))
        self.Bind(wx.EVT_TEXT, lambda event: self.do_spellcheck_while_type(event))
        self.Bind(wx.EVT_CHAR, lambda event: self.filter_keys_while_type(event))

        self.the_dict = enchant.Dict("en_US")

    def filter_keys_while_type(self, event):
        # filter out characters which are not allowed in the keywords
        # or not used in cursor positioning
        key_code = event.GetKeyCode()
        # print('KEY:', key_code)
        if key_code == 1 or key_code == 8 or key_code == 22 or key_code == 127 or key_code == 9:
            # select all, backspace, paste, delete, tab
            event.Skip()
        elif key_code == 3 or key_code == 22:
            # Ctrl+C, Ctrl+V
            event.Skip()
        elif key_code == 44 and self.allow_comma:
            # comma
            event.Skip()
        elif 314 <= key_code <= 317:
            # left and right, up and down arrows
            event.Skip()
        elif key_code == 13:
            # Enter
            self.on_enter()
            # event.Skip() <- comment it to avoid GTK problems
        elif self.valid_char(key_code):
            self.need_spell_check_while_type = True
            event.Skip()
        else:
            # block out everything else
            pass

    def on_enter(self):
        if self.Name == 'search_edit':
            pass
            # print("GO Search!!!")
            # evt = Search_keyw_DB(id=wx.ID_ANY)
            # wx.PostEvent(evt)

    def valid_char(self, key_code: int) -> bool:
        # function returns True if the key_code is a valid character code
        return chr(key_code) in ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def do_spellcheck_while_type(self, event):
        # do spellcheck while type if necessary
        if len(self.GetLineText(0)) == self.GetInsertionPoint() and self.need_spell_check_while_type:
            last_word = self.GetLineText(0).split(' ')[-1]
            if len(last_word) > 1:
                the_end = len(self.GetLineText(0))
                the_start = len(self.GetLineText(0)) - len(last_word)
                # print('  text range in the line:', the_start, the_end)
                if self.the_dict.check(last_word):
                    self.SetStyle(the_start, the_start + 1, self.GetDefaultStyle())
                    self.SetStyle(the_start, the_end, wx.TextAttr(wx.BLACK))
                else:
                    self.SetStyle(the_start, the_end, wx.TextAttr(wx.RED))
                print("spellcheck:", last_word, self.the_dict.check(last_word))
            self.need_spell_check_while_type = False
