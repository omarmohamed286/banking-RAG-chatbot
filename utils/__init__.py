from yaml import safe_load
from ensure import ensure_annotations
from pathlib import Path
from typing import Dict



@ensure_annotations
def read_yaml(file_path: Path) -> Dict:
    try:
        with open(file_path) as yaml_file:
            file_content = safe_load(yaml_file)
            return file_content
    except Exception as e:
        raise Exception(f'Error occured: {e}')




