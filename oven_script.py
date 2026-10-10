import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

NORMAL = 30
EXTENSION = 12

current_date = datetime.now()

def get_label(folder):
    folder_name = folder.name
    label = folder_name[folder_name.find("[")+1:folder_name.find("]")] # Ewww...

    return label

def get_creation(folder):
    return datetime.fromtimestamp(os.stat(folder).st_birthtime)

def get_deadline(folder, label):
    deadline = get_creation(folder) + timedelta(days=NORMAL)
    if label == "EXTEND":
        deadline += timedelta(days=EXTENSION)
    return deadline


def send_to_graveyard(root, folder):
    graveyard = Path(f"{root}/[T]GRAVEYARD")
    if not graveyard.exists():
        os.mkdir(graveyard)

    shutil.move(folder, graveyard)

def checker(root, folder:Path):
    label = get_label(folder)
    if not label == "T": 
        for directory in folder.iterdir():
            directory = Path(directory)
            
            label = get_label(directory)
            deadline = get_deadline(directory, label)
            
            if directory.is_dir():    
                if label == "F":
                    checker(root, directory)
                elif current_date >= deadline and label not in ["FINISHED"]:
                    send_to_graveyard(root, directory)


if __name__ == "__main__":
    root = Path(f"{Path.cwd()}/Test")
    if not root.exists():
        os.mkdir(root)
    checker(root, root)