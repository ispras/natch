#!/usr/bin/env python3

import os
import sys
import fileinput

script_dir, filename = os.path.split(os.path.abspath(__file__))
path = os.path.join(script_dir, '../docs')

manuals = []

def replace(file):
    for line in fileinput.input(os.path.join(path, file), inplace=1):
        for file in manuals:
            if file in line:
                line = line.replace(file, '')
                break
        sys.stdout.write(line)


for filename in os.listdir(path):
    if filename[0].isnumeric() or filename.startswith('app'):
        manuals.append(filename)

for file in manuals:
    replace(file)

