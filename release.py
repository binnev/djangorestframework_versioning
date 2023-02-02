import shutil
import subprocess
from pathlib import Path

LIBRARY_NAME = "djangorestframework_versioning"


def cleanup():
    for folder in [
        Path(__file__).parent / f"{LIBRARY_NAME}.egg-info",
        Path(__file__).parent / "dist",
        Path(__file__).parent / "site",
    ]:
        if folder.exists():
            shutil.rmtree(folder)


cleanup()
subprocess.run("python -m build".split())
subprocess.run("twine upload dist/*".split())
cleanup()
