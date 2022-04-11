from pathlib import Path
from typing import NamedTuple
import subprocess


class Requirement(NamedTuple):
    name: str
    requirement: str


layer_dir = Path.cwd() / "layer"
subprocess.check_output(["rm", "-rf", str(layer_dir)])
layer_dir.mkdir(exist_ok=True)

# requirements
requirements_txt = Path.cwd() / "requirements.txt"
with requirements_txt.open() as f:
    requirements = [Requirement(x.split("==")[0], x)
                    for x in f.read().split("\n")]

for req in requirements:
    subprocess.check_output(
        ["pip", "install", req.requirement, "-t", str(layer_dir / req.name)])

# font
# git clone https://github.com/fontdasu/ShipporiAntique.git layer/font/
subprocess.check_output(
    ["git", "clone", "https://github.com/fontdasu/ShipporiAntique.git", str(layer_dir / "font")])
