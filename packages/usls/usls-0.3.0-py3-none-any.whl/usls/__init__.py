#!/usr/bin/env python
# -*- coding:utf-8 -*- 

__version__ = '0.3.0'
_logo = '''
	
'''

from usls.cli import cli
from usls.src.utils import (
	smart_path, TIMER, Palette
)



__all__ = [
	'__version__', 
	'cli',
	'smart_path',
	'TIMER',
	'Palette'
]
