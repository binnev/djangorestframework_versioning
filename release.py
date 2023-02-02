import shutil
import subprocess
from pathlib import Path
import drf_versioning
import glob

version = drf_versioning.__version__


def cleanup():
    paths = ["dist", "site", ".pytest_cache"]
    paths += glob.glob("*.egg-info")
    paths += glob.glob("*.pytest_cache")
    for path in paths:
        path = Path(__file__).parent / path
        if path.exists():
            shutil.rmtree(path)


def check(question: str):
    response = input(question + "\n")
    if response.lower() not in ["y", "yes"]:
        raise Exception(f"Action required")


def shell(cmd: str):
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    print(f"Releasing version {version}")
    cleanup()
    check(f"Did you create / update the Version changelog for version {version}?")

    print("Building package")
    shell("python -m build")
    shell("twine check dist/*")

    print("PyPI test run")
    shell("twine upload -r pypitest dist/*")
    check(f"Does the testpypi output look OK?")

    # print("PyPI deploy")
    # shell("twine upload dist/*", she)

    print("Building docs")
    shell(f"mike deploy {version}")
    shell(f"mike alias {version} latest --update-aliases")
    try:
        process = shell("mike serve")
    except KeyboardInterrupt:
        pass
    check("Do the docs look OK?")
    shell("mike list")
    check("Does the list of docs versions look OK?")

    print("Deploying docs")
    shell(f"mike set-default latest --push")
    cleanup()

    print("Done!")
