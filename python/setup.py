# -*- coding: utf-8 -*- 
from distutils.core import setup
import py2exe

# 打包程序
options = {'py2exe': { 'dist_dir': "../benben_dist/" }}

setup(console=['main.py'], options=options)