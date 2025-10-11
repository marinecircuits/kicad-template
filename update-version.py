# get name of PCB file, the one with .kicad_pcb extension
import os
import re

def get_new_revision() -> str:
    # get git commit descrpition
    commit_desc = os.popen("git describe --tags --abbrev=4").read().strip()
    return commit_desc


def get_pcb_file_name() -> str:
    for file in os.listdir("."):
        if file.endswith(".kicad_pcb"):
            return file
    raise FileNotFoundError("No .kicad_pcb file found in the current directory.") 

pcb_file = get_pcb_file_name()
print(f"PCB file: {pcb_file}")
# Read the file
with open(pcb_file, "r") as f:
    content = f.read()
# Replace the revision string inside (rev "...")
content = re.sub(r'\(rev\s*"[^"]*"\)', f'(rev "{get_new_revision()}")', content)

with open(pcb_file, "w") as f:
    f.write(content)