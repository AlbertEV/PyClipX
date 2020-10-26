#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.0a6 on Sun Oct 25 12:17:20 2020
#

import wx
from time import sleep
import threading
import pyclipx
import pyperclip

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):

    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((487, 596))
        self.SetTitle("PyClipX-0.1")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 4)

        self.button_6 = wx.Button(self.panel_1, wx.ID_ANY, "Start")
        sizer_2.Add(self.button_6, 0, wx.ALL, 2)

        self.button_7 = wx.Button(self.panel_1, wx.ID_ANY, "Copy All")
        sizer_2.Add(self.button_7, 0, wx.ALL, 2)

        self.button_8 = wx.Button(self.panel_1, wx.ID_ANY, "Cut All")
        sizer_2.Add(self.button_8, 0, wx.ALL, 2)

        self.button_9 = wx.Button(self.panel_1, wx.ID_ANY, "Clear")
        sizer_2.Add(self.button_9, 0, wx.ALL, 2)

        self.on = wx.Bitmap("on.png")
        self.off = wx.Bitmap("off.png")

        self.bitmap_1 = wx.StaticBitmap(
            self.panel_1, wx.ID_ANY, wx.Bitmap("./off.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_1.SetMinSize((32, 32))
        sizer_2.Add(self.bitmap_1, 0, wx.LEFT, 23)

        static_line_1 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.EXPAND, 0)

        self.text_ctrl_2 = wx.TextCtrl(
            self.panel_1, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE)
        sizer_1.Add(self.text_ctrl_2, 1, wx.ALL | wx.EXPAND, 0)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.button_strart_stop_switch, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.button_copy_press, self.button_7)
        self.Bind(wx.EVT_BUTTON, self.button_cut_press, self.button_8)
        self.Bind(wx.EVT_BUTTON, self.button_clear_press, self.button_9)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_TEXT, self.change_text_ctr_2, self.text_ctrl_2)
        # end wxGlade
        self.ignore_clipboard = [""]
        self.app = pyclipx.PyClipX()
        self.gui_text = []
        self.is_update = True
        self.x = threading.Thread(target=self.update_text_ctr)
        self.x.start()

    # wxGlade: MyFrame.<event_handler>
    def button_strart_stop_switch(self, event):
        """ wxGlade: MyFrame.<event_handler>"""
        if self.app.is_run:
            self.app.stop_tree()
            # self.gui_text = [""]
            # self.text_ctrl_1.Clear()
            self.button_6.SetLabel("Start")
            self.bitmap_1.SetBitmap(self.off)

        else:
            self.app.start()
            self.button_6.SetLabel("Stop")
            self.bitmap_1.SetBitmap(self.on)

    def button_copy_press(self, event):  # wxGlade: MyFrame.<event_handler>
        # self.app.list_update.clear()
        union = ("\r\n").join(self.gui_text)
        pyperclip.copy(union)
        self.ignore_clipboard.append(union)
        # self.text_ctrl_2.Clear()
        # self.gui_text.clear()

    def button_cut_press(self, event):  # wxGlade: MyFrame.<event_handler>
        self.app.stop_tree()
        sleep(0.5)
        union = "\r\n".join(self.gui_text)
        pyperclip.copy(union)
        print("#####:", union, self.gui_text)
        self.button_6.SetLabel("Start")
        self.bitmap_1.SetBitmap(self.off)
        self.app.list_update.clear()
        self.gui_text.clear()
        self.text_ctrl_2.Clear()

    def button_clear_press(self, event):  # wxGlade: MyFrame.<event_handler>
        pyperclip.copy("")
        self.text_ctrl_2.Clear()
        self.app.list_update.clear()
        self.gui_text.clear()
        self.ignore_clipboard.clear()

    def OnClose(self, event):
        print("cerrado")
        self.is_update = False
        self.app.stop_tree()
        self.Destroy()

    def update_text_ctr(self):
        """Update text ctrl"""
        while self.is_update:
            sleep(0.5)
            for text in self.app.list_update:
                if (text not in self.gui_text) and (text != ""):
                    if text not in self.ignore_clipboard:
                        self.gui_text.append(text)
                        self.text_ctrl_2.AppendText(str(text) + "\n")
                        # print(text)

    def change_text_ctr_2(self, event):
        text_ctrl = len(self.text_ctrl_2.GetValue())
        print(text_ctrl)
        if text_ctrl <= 2:
            pyperclip.copy("")
            self.app.list_update.clear()
            self.gui_text.clear()
            self.ignore_clipboard.clear()
            text_ctrl = 3


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
