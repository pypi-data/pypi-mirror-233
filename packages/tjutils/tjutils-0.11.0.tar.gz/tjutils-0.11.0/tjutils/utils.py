# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/00-utils.ipynb.

# %% auto 0
__all__ = ["copy_template", "copy_directory", "merge_yaml"]

# %% ../notebooks/00-utils.ipynb 1
import yaml
import shutil
import importlib.resources as pkg_resources
from pathlib import Path

# %% ../notebooks/00-utils.ipynb 3
def copy_template(tmp: str, file: str, append: bool = False):
    "Copies a template from the templates directory"
    filepath = Path(file)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    content = pkg_resources.files("tjutils").joinpath(f"templates/{tmp}").read_text()
    with open(file, "a" if append else "w") as f:
        f.write(content)
    return None


# %% ../notebooks/00-utils.ipynb 4
def copy_directory(template_dir: str, destination_dir: str):
    "Copies a directory from the template directory"
    src = str(pkg_resources.files("tjutils").joinpath(f"templates/{template_dir}"))
    dst = destination_dir
    shutil.copytree(src, dst, dirs_exist_ok=True)
    return None


# %% ../notebooks/00-utils.ipynb 5
def merge_yaml(template_yaml: str, destination_yaml: str):
    "Merges in a YAML file into another yaml"
    src = pkg_resources.files("tjutils").joinpath(f"templates/{template_yaml}")
    dst = Path(destination_yaml)
    with src.open("r") as f:
        src_data = yaml.safe_load(f)
    if dst.is_file():
        with dst.open("r") as f:
            dst_data = yaml.safe_load(f)
        new_data = dst_data | src_data
    else:
        new_data = src_data
    with dst.open("w") as f:
        yaml.dump(new_data, f)
    return None
