import PySimpleGUI as sg
from src.app import NpzEditor

if __name__ == "__main__":
    npz_editor = NpzEditor()

    while True:
        main_evt, main_vals = npz_editor.window.read(timeout=1)
        # if main_evt != "__TIMEOUT__":
        #     print(main_evt, main_vals)

        if main_evt == sg.WIN_CLOSED or main_evt == 'Exit::-EXIT-':
            break
        elif main_evt == 'Open::-OPEN-':
            npz_editor.event_open_npz_file()
        elif main_evt == 'Save::-SAVE-':
            npz_editor.event_save_npz_file()
        elif main_evt == 'Save As::-SAVEAS-':
            npz_editor.event_saveas_npz_file()
        elif main_evt == 'npz_elems':
            npz_editor.event_npz_elems_changed(main_vals['npz_elems'])
        elif main_evt == 'omission':
            npz_editor.event_omission_ckb(not main_vals['omission'])
