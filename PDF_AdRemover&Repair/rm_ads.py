#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 2023-10-27
Project: Ads Remover and PDF Repairer

File: rm_ads.py

Abstract: remove ads with gulagcleaner and repair PDFs so they can be opened
with SumatraPDF.

Use: python3 -m rm_ads.py [glob pattern, directory, default='.'] [ghostcript_path]
'''

from pdfplumber import repair
from gulagcleaner.extract import clean_pdf

import sys
from pathlib import Path
from itertools import zip_longest


OBF_NAME1 = ['w', 'o', 'a', '-', 'r', 'e']
OBF_NAME2 = ['u', 'l', 'h', 'f', 'e']
OBF_NAME = ''.join(''.join(tup) for tup in zip_longest(OBF_NAME1, OBF_NAME2, fillvalue=''))


def output_path_from_original(path):
    if not isinstance(path, Path):
        path = Path(path)
    new_pdf_stem = path.stem.removeprefix(OBF_NAME).strip('-').rstrip('-')
    new_pdf_path = path.with_stem(new_pdf_stem)
    return new_pdf_path


def rm_ads_and_repair(path, ghostscript_path=None):
    if not isinstance(path, Path):
        path = Path(path)
    new_pdf_path = output_path_from_original(path)
    # Clean PDF
    clean_pdf(pdf_path=path.__str__(), output_path=new_pdf_path)
    # Repair PDF
    repair(path_or_fp=new_pdf_path, outfile=new_pdf_path, gs_path=ghostscript_path)


def main(path, ghostscript_path):
    if not isinstance(path, Path):
        path = Path(path)
    if path.is_dir():
        for pdf in path.glob('**/*.pdf'):
            rm_ads_and_repair(pdf, ghostscript_path)
    elif path.is_file():
        rm_ads_and_repair(path, ghostscript_path)


if __name__ == '__main__':
    len_sys = len(sys.argv)
    path = sys.argv[1] if len_sys >= 2 else None
    if not path:
        path = Path('.')
    gs_path = sys.argv[2] if len_sys >= 3 else None
    main(path, gs_path)
