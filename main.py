import PySimpleGUI as sg
from src.app import NpzEditor

if __name__ == "__main__":
    npz_editor = NpzEditor()
    # src = "vo_result_poses.npz"
    # npz_editor.open_npz(src)

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
        elif main_evt == 'npz_keys':
            npz_editor.event_npz_keys_selected(main_vals['npz_keys'][0])
        elif main_evt == 'omission':
            npz_editor.event_omission_ckb(not main_vals['omission'])
        elif main_evt == '-SELECT_KEY_UP-':
            if len(npz_editor.window['npz_keys'].Widget.curselection()) == 0:
                continue
            npz_editor.event_npz_keys_change(npz_editor.window['npz_keys'].Widget.curselection()[0] - 1)
        elif main_evt == '-SELECT_KEY_DOWN-':
            if len(npz_editor.window['npz_keys'].Widget.curselection()) == 0:
                continue
            npz_editor.event_npz_keys_change(npz_editor.window['npz_keys'].Widget.curselection()[0] + 1)
        elif main_evt == '-EDIT_NPZ_KEY-':
            npz_editor.event_key_list_doubleclick()
