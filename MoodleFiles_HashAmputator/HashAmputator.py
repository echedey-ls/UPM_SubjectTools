#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: Echedey Luis Álvarez
Date: 08/03/2022
Project: Moodle files hash amputator

File: HashAmputator.py

Abstract: Deletes file hash from the end of its filename

Sources:
"""

from os import listdir, rename
from os.path import splitext, isdir, isfile, exists, join
import re

hashMatcher = re.compile(r"^(?P<baseName>.*)_[a-fA-F0-9]{32}$")
## Match example
"""example_06955cc0d1aec70fd5aa8e6682a76159"""

def main():
    selectedDir = input("Select the directory which has the files: ")
    while not exists(selectedDir):
        selectedDir = input("Select the directory which has the files: ")
    renN = renameDeletingHash(selectedDir)
    print(f"Total number of renamed files: {renN}")
    return

def renameDeletingHash(dir) -> int:
    nRenamed = 0
    for entry in listdir(dir):
        fullEntry = join(dir, entry)
        if isdir(fullEntry):
            print(f"Currenty directory: {fullEntry}")
            nRenamed = nRenamed + renameDeletingHash(fullEntry)
        elif isfile(fullEntry):
            f_name, f_ext = splitext(entry)
            match = hashMatcher.fullmatch(f_name)
            if match:
                newFilename = match['baseName'] + f_ext
                print(f'"{entry}" --> "{newFilename}"')
                rename(fullEntry, join(dir, newFilename))
                nRenamed = nRenamed + 1
    return nRenamed

if __name__ == "__main__":
    main()
