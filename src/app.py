import numpy as np
import PySimpleGUI as sg
from src.config import *


class NpzEditor():
    def __init__(self):
        self.filename: str = None
        self.data = None
        self.create_window()

    def create_window(self) -> sg.Window:
        self.window = sg.Window(
            'NPZ Editor',
            self.layout(),
            # icon=img_to_base64(ICON_IMG_SRC),
            resizable=True,
            use_default_focus=False,
            finalize=True
        )
        self.window.force_focus()
        self.bind_shortcutkeys()

    def __del__(self):
        self.window.close()

    def layout(self):
        menubar = sg.Menubar([['File', ['Open::-OPEN-', 'Save::-SAVE-', 'Save As::-SAVEAS-', 'Exit::-EXIT-']]], key='menubar')
        filename_txt = sg.Text('', key='filename')
        omission_chkbox = sg.Checkbox('Data omission', key='omission', default=False, enable_events=True)
        npz_keys_list = sg.Listbox([], key='npz_keys', enable_events=True, horizontal_scroll=True, expand_x=True, expand_y=True)
        npz_shape_txt = sg.Text('', key='np_shape')
        data_tab_ml = sg.Multiline(size=(80, 25), font=(font_style_console, 12), expand_x=True, expand_y=True, key='dataview', background_color='#FFFFFF', horizontal_scroll=True, disabled=True)
        layouts = [
            [menubar],
            [filename_txt, omission_chkbox],
            [npz_keys_list, sg.Column([[npz_shape_txt], [data_tab_ml]], expand_x=True, expand_y=True)]
        ]
        return layouts

    def bind_shortcutkeys(self):
        self.window.bind('<Control-o>', 'Open::-OPEN-')
        self.window.bind('<Control-S>', 'Save As::-SAVEAS-')
        self.window['npz_keys'].Widget.bind('<Double-Button-1>', self.event_key_list_doubleclick)
        self.window['npz_keys'].Widget.bind('<F2>', self.event_key_list_doubleclick)

    def event_open_npz_file(self):
        filename = sg.popup_get_file(
            'Open NPZ file',
            title='Open NPZ file',
            default_path='.',
            file_types=(('NPZ', '*.npz'),),
            no_window=True,
        )
        if filename is None:
            return
        self.open_npz(filename)

    def event_save_npz_file(self):
        np.savez("vo.npz", **self.data)

    def event_saveas_npz_file(self):
        src = sg.popup_get_file(
            'Open NPZ file',
            title='Open NPZ file',
            default_path='.',
            file_types=(('NPZ', '*.npz'),),
            no_window=True,
            save_as=True
        )
        if src is None:
            return
        np.savez(src, **self.data)
        self.open_npz(src)

    def open_npz(self, src: str):
        self.filename = src
        self.data = dict(np.load(src, allow_pickle=True))
        self.window['filename'].update(src)
        self.listup_keys()

    def listup_keys(self):
        self.data = dict(sorted(self.data.items(), key=lambda x: x[0]))
        self.window['npz_keys'].update(values=self.data.keys())

    def event_npz_keys_changed(self, k: str):
        if len(k) == 0:
            return
        self.window['np_shape'].update(f"Shape: {self.data[k[0]].shape}")
        self.window['dataview'].update(self.data[k[0]])

    def event_omission_ckb(self, is_omit: bool):
        if is_omit:
            np.set_printoptions(threshold=0)
        else:
            np.set_printoptions(threshold=np.inf)

    def event_key_list_doubleclick(self, btn_evt: sg.tk.Event):
        if self.data is None:
            return
        row = btn_evt.widget.curselection()[0]
        self.edit_key_name(row)

    def edit_key_name(self, row):
        edit = False
        data_lists = self.window['npz_keys'].get_list_values()
        old_txt = data_lists[row]

        def callback(evt, row, txt, k):
            global edit
            widget = evt.widget
            if k == 'Return':
                txt = widget.get()
                if old_txt != txt:
                    data_lists[row - 1] = txt

                    self.data[txt] = self.data[old_txt]
                    self.data.pop(old_txt)

                    self.listup_keys()
                    self.window['dataview'].update(self.data[txt])
            widget.destroy()
            widget.master.destroy()
            edit = False

        if edit or row < 0:
            return

        edit = True
        list_box = self.window['npz_keys'].Widget
        x, y, w, h = list_box.bbox(row)

        frame = sg.tk.Frame(list_box)
        frame.place(x=x, y=y, anchor="nw", width=150, height=h)
        text_var = sg.tk.StringVar()
        text_var.set(old_txt)
        entry = sg.tk.Entry(frame, textvariable=text_var, bg="white", width=w)
        entry.pack()
        entry.select_range(0, sg.tk.END)
        entry.icursor(sg.tk.END)
        entry.focus_force()
        entry.bind("<Return>", lambda e, r=row, t=old_txt, k='Return': callback(e, r, t, k))
        entry.bind("<Escape>", lambda e, r=row, t=old_txt, k='Espace': callback(e, r, t, k))
        entry.bind("<Button-1>", lambda e, r=row, t=old_txt, k='Espace': callback(e, r, t, k))
