from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='remote-log',
    version='1.0.10',
    packages=find_packages(),
    description = 'A simple function to send logging data to a remote server.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'Shubham Gupta',
    author_email = 'shubhastro2@gmail.com',
    install_requires=[
            'psutil',
            'py-cpuinfo',
            'requests',
        ],
)