import shutil
from pathlib import Path
from datetime import datetime, timedelta

NORMAL = 30
EXTENSION = 12

CURRENT_DATE = datetime.now()

def get_folder_label(folder):
    folder_name:str = folder.name

    if "[" in folder_name and "]" in folder_name:
        folder_label = folder_name[folder_name.find("[")+1:folder_name.find("]")] # Ewww...
    else:
        return None

    return folder_label


def get_creation(folder):
    return datetime.fromtimestamp(folder.stat().st_birthtime)


def calc_deadline(folder, folder_label):
    deadline = get_creation(folder) + timedelta(days=NORMAL)
    
    if folder_label == "EXTEND":
        deadline += timedelta(days=EXTENSION)
    return deadline


def send_to_graveyard(root, folder):
    GRAVEYARD = root / "[T]GRAVEYARD"
    
    if not GRAVEYARD.exists():
        GRAVEYARD.mkdir()

    shutil.move(folder, GRAVEYARD)


def checker(root, folder:Path):
    for directory in folder.iterdir():
        if directory.name.startswith("[T]") or "GRAVEYARD" in directory.name:
            continue

        directory = Path(directory)

        folder_label = get_folder_label(directory)
        deadline = calc_deadline(directory, folder_label)
        
        if directory.is_dir():
            if folder_label == "F": 
                checker(root, directory)
            elif CURRENT_DATE < deadline and not folder_label == "FINISHED":
                send_to_graveyard(root, directory)



if __name__ == "__main__":
    root = Path("[OVEN]")

    if not root.exists():
        root.mkdir()
    
    checker(root, root)