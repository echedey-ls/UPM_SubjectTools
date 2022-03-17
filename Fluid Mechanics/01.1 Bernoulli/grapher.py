#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 15/03/2022
Project: Data analysis of fluid mechanichs lab

File: grapher.py

Abstract: just another graph

Sources:
'''

from os import mkdir
from os.path import getmtime, join, exists
from scipy.stats import linregress
import matplotlib.pyplot as plt
import pandas as pd

dataPath   = '..\\00 data'
outputPath = 'out'

dataFile   = join(dataPath, 'Lab1.xlsx')

def main():
    dfs = (
        # Label/title, pandas dataframe, reverse x
        ('convergente', pd.read_excel(dataFile, sheet_name= u'Práctica 1', usecols= 'L:U', skiprows= 3,  nrows= 7), False),
        ('divergente' , pd.read_excel(dataFile, sheet_name= u'Práctica 1', usecols= 'L:U', skiprows= 12, nrows= 7), True)
    )

    # Graph generator
    for df in dfs:
        plt.clf()
        # Superior title
        suptitle = u'Flujo '+df[0]
        plt.suptitle(suptitle, y=0.975)
        # Subtitle
        plt.title(u'Alturas características en función del diámetro del tubo', **{'fontsize': 'medium'})
        
        plt.xlabel(u'Diámetro del tubo de Venturi (d) [mm]')
        plt.ylabel(u'Alturas (h\u2096) [mm]')
        plt.grid(which='major', axis='both')

        legend = []

        # Altura presión (medida)
        legend.append(u'Altura presión (medida)')
        plt.plot(
            df[1].iloc[:,0],
            df[1].iloc[:,5],
            c= 'tomato'
        )

        # Altura cinética (calculada)
        legend.append(u'Altura cinética (calculada)')
        plt.plot(
            df[1].iloc[:,0],
            df[1].iloc[:,4],
            c= 'hotpink'
        )

        # Altura de Pitot (medida)
        legend.append(u'Altura de Pitot (medida)')
        plt.plot(
            df[1].iloc[:,0],
            df[1].iloc[:,7],
            c= 'crimson'
        )

        # Altura promedio de carga (calculada)
        legend.append(u'Altura promedio de carga (calculada)')
        plt.plot(
            df[1].iloc[:,0],
            df[1].iloc[:,6],
            c= 'mediumspringgreen'
        )

        # Reverse x axis and draw arrow
        arrowStyle = {
            'width'      : 2.5,
            'head_width' : 10,
            'head_length': 2,
            'color'      : 'turquoise',
        }
        legend.append('Flujo hidráulico')
        if df[2]:
            plt.gca().invert_xaxis()
            plt.arrow(25, -5, -13, 0, **arrowStyle)
        else:
            plt.arrow(10, -5, +13, 0, **arrowStyle)

        plt.legend(legend)

        if not exists(outputPath):
            mkdir(outputPath)
            
        plt.savefig(join(outputPath, 'Graph_'+df[0]+'.png'))
        plt.show()

    return

# def isFileNewer(reference, toCompare):
#     if getmtime(toCompare) > getmtime(reference):
#         return True
#     else:
#         return False

if __name__ == '__main__':
    main()
    print('Data was analyzed successfully. Have a nice day.')
