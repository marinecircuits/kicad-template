# get name of PCB file, the one with .kicad_pcb extension
import os
import re

def get_new_revision(only_major_if_released=False) -> str:
    # get git commit descrpition
    commit_desc = os.popen("git describe --tags --abbrev=4").read().strip()
    if only_major_if_released:
        if re.fullmatch(r'\d+\.\d+\.\d+', commit_desc):
            return commit_desc.split('.')[0]
    return commit_desc


def get_pcb_file_name() -> str:
    for file in os.listdir("."):
        if file.endswith(".kicad_pcb"):
            return file
    raise FileNotFoundError("No .kicad_pcb file found in the current directory.") 

def get_schematic_file_name() -> str:
    # get pcb file name, but with .kicad_sch extension
    pcb_file = get_pcb_file_name()
    return pcb_file.replace(".kicad_pcb", ".kicad_sch")

pcb_file = get_pcb_file_name()
print(f"PCB file: {pcb_file}")
# Read the file
with open(pcb_file, "r") as f:
    content = f.read()
# Replace the revision string inside (rev "...")
content = re.sub(r'\(rev\s*"[^"]*"\)', f'(rev "{get_new_revision(True)}")', content)

with open(pcb_file, "w") as f:
    f.write(content)

sch_file = get_schematic_file_name()
print(f"Schematic file: {sch_file}")
# Read the file
with open(sch_file, "r") as f:
    content = f.read()
# Replace the revision string inside (rev "...")
content = re.sub(r'\(rev\s*"[^"]*"\)', f'(rev "{get_new_revision()}")', content)

with open(sch_file, "w") as f:
    f.write(content)