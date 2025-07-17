import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource for PyInstaller onefile mode """
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this at runtime
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
def get_task_list_path():
    """ Return a writable path for saving task list, works in EXE and script """

    filename = 'to_do_list.csv'

    # Running as EXE: save to user's AppData\Roaming\PomoToDo folder
    if getattr(sys, 'frozen', False):
        appdata = os.getenv('APPDATA')
        app_folder = os.path.join(appdata, 'PomoToDo')
        os.makedirs(app_folder, exist_ok=True)
        full_path = os.path.join(app_folder, filename)
    
    # Running as script: save in current directory
    else:
        full_path = os.path.join(os.path.abspath("."), filename)

    # Create file with header if it doesn't exist
    if not os.path.exists(full_path):
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write("task\n")  # write header line

    return full_path