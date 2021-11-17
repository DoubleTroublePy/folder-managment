from pathClear import PathClear
import PySimpleGUI as sg
import os 

pc = PathClear()


def popup(message: str, bt1: str = 'ok', bt2: str = 'cancel') -> None:
    layout = [
        [sg.Text(message)],
        [sg.Button(bt1), sg.Button(bt2)]
    ]
    window = sg.Window('Download Manager', layout)
    window.read()
    window.close()


def draw_edit(t1: str = '', t2: str = ''):
    layout = [
        [sg.Text('Enter the name of the file you want to rename')],
        [sg.Text('Estensione'), sg.InputText(t1, key='-key-'), sg.Text('Cartella'), sg.InputText(t2, key='-value-')],
        [sg.Button('Confirm'), sg.Button('Cancel')]
    ]
    window = sg.Window('edit', layout)
    
    while True:
        event, values = window.read()
        if event == 'Confirm':
            pc.add_file_type(values['-key-'], values['-value-'])
            window.close()
            return True
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            window.close()
            return False
    

def draw_options():
    def show(): return [(key, ':', pc.paths[key]) for key in pc.paths]
    layout = [
        [sg.Text('Options')],
        [sg.Text('Choose an option:')],
        [sg.Listbox(values=show(), size=(25,10),change_submits=True,
                                        bind_return_key=True,
                                        auto_size_text=True,
                                        key='_list_', enable_events=True)],
        
        [sg.Button('edit'), sg.Button('New'), sg.Button('Delete') ,sg.Button('Exit')]
    ]
    window = sg.Window('Download Manager', layout)
    while True:
        event, values = window.read()

        if event == 'New':
            draw_edit()
            window.Element('_list_').update(values=show())
        if event == 'edit':
            l = window.Element('_list_').Widget.curselection()
            d = pc.paths.keys()
            if len(l) > 0:
                value = pc.paths.get(list(d)[l[0]])
                keys_list = list(pc.paths)
                key = keys_list[l[0]]
                if draw_edit(key, value):
                    pc.del_file_type(key)
            window.Element('_list_').update(values=show())
        if event == 'Delete':
            l = window.Element('_list_').Widget.curselection()
            if len(l) > 0:
                d = pc.paths.keys()
                pc.del_file_type(list(d)[l[0]])
                window.Element('_list_').update(values=show())

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
    window.close()


def draw_window():
    layout = [
        [sg.Text('folder manger')],
        [sg.Text('Folder:', size=(10, 1)), sg.InputText(key='-folder-', size=(60, 1)), sg.FolderBrowse('path', key='-path-')],
        [sg.Button('Clear'), sg.Button('Exit'), sg.Button('Settings')],
    ]
    
    window = sg.Window('folder manger', layout)
    while True:
        event, values = window.read()
        if event == 'path':
            window.hide()
        if event == 'Clear':
            val = values['-folder-']
            if os.path.isdir(val):
                pc.val_path = val
                pc.path_clear()
            else:
                popup('the path is invalid')
                window.find_element('-folder-').update('')
        if event == 'Settings':
            draw_options()

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    draw_window()
    
    # path = input('Enter path >>> ')
    # pc = pathClear(path)

    # pc.pathClear()