from setuptools import setup, find_packages

setup(
    name="bahr-backend",
    version="1.0.0",
    description="BAHR - Arabic Poetry Prosody Analysis Backend",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        # Core dependencies will be installed from requirements.txt
        # This setup.py is primarily for editable installation
    ],
)
