import os
from pathlib import Path
from datetime import datetime, timedelta
import shutil

NORMAL = 30
EXTENSION = 12

current_date:datetime = datetime.now()

def get_label(folder:Path):
    folder_name = folder.name

    label = folder_name[folder_name.find("[")+1:folder_name.find("]")] # Ewww...

    if label in ["T", "FINISHED", "EXTEND"]:
        return label
    return None

def check_creation(folder):
    return datetime.fromtimestamp(os.stat(folder).st_birthtime)

def calc_deadline(folder, label):
    deadline = check_creation(folder) + timedelta(days=NORMAL)
    if label == "EXTEND":
        deadline += timedelta(days=EXTENSION)
    return deadline


def send_graveyard(root, folder:Path):
    graveyard = Path(f"{root}/[T]GRAVEYARD")
    if not graveyard.exists():
        os.mkdir(graveyard)
    
    shutil.move(folder, graveyard)

def checker(root, folder:Path):
    label = get_label(folder)
    if not label in ["T", "FINISHED"]:
        for directory in folder.iterdir():
            directory = Path(directory)
            
            label = get_label(directory)
            deadline = calc_deadline(directory, label)

            print(label)
            
            if directory.is_dir():    
                if label == "T":
                    checker(root, directory)
                elif current_date < deadline and not label in ["T", "FINISHED"]:
                    send_graveyard(root, directory)
    return


if __name__ == "__main__":
    root = Path(f"{Path.cwd()}/Test")
    if not root.exists():
        os.mkdir(root)
    checker(root, root)