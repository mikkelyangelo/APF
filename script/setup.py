from setuptools import setup

APP = ['exe_conventer.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5','time','numpy','random','matplotlib'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)