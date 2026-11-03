from pathlib import Path
from setuptools import find_packages, setup

ROOT = Path(__file__).parent


def read_requirements():
    requirements_file = ROOT / "requirements.txt"
    if not requirements_file.exists():
        return []
    return [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#") and line.strip() != "-e ."
    ]


setup(
    name="loan-approval-prediction",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    python_requires=">=3.9",
)
