#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 19/10/2022
Project: Plotter for two excel sheets

File: analysis_thermopile.py

Abstract: just another grapher

Sources:
'''

import matplotlib.pyplot as plt
import pandas as pd
import mplcyberpunk
import scienceplots

dataFiles = (
    ('TTL' , 'data-TTL.csv'),
    ('CMOS', 'data-CMOS.csv')
)

def main():
    plt.style.use(['latex-sans', 'cyberpunk'])
    for title, csv_file in dataFiles:
        df = pd.read_csv(csv_file, sep=',', decimal='.', skiprows=1, names=['V_in', 'V_out'], usecols= [0, 1])

        plt.clf()
        # Superior title
        plt.suptitle(title, **{'fontsize': 'x-large'})
        # Subtitle

        plt.plot(df['V_in'], df['V_out'], marker='o')
        plt.xlabel(r'$V_{in} [V]$')
        plt.ylabel(r'$V_{out} [V]$')

        mplcyberpunk.add_glow_effects()

        #plt.tight_layout()
        plt.savefig(title+'.png')
        plt.show()
    return

if __name__ == '__main__':
    main()
    print('☭Data was analyzed successfully. Have a nice day☭')
