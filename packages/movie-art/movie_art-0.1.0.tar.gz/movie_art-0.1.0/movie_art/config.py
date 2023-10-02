'''
config.py
'''

import dataclasses
import pathlib


@dataclasses.dataclass
class Config:
    '''
    Config
    '''

    input: pathlib.Path
    output: pathlib.Path = pathlib.Path('output.jpg')
    width: int = 512
    height: int = 128
