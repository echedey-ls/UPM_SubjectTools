#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 13/03/2022
Project: Data analysis of fluid mechanichs lab

File: grapher.py

Abstract: just another graph script

Sources:
'''

from os.path import getmtime, join, exists
from scipy.stats import linregress
import matplotlib.pyplot as plt
import pandas as pd

dataPath   = '..\\00 data'
outputPath = 'out'

dataFile   = join(dataPath, 'Lab1.xlsx')
figureFile = join(outputPath, 'Figure_1.png')

def main():
    df0 = pd.read_excel(dataFile, sheet_name= u'Práctica 2', usecols= 'B:F', skiprows= 10, nrows= 5)
    df1 = pd.read_excel(dataFile, sheet_name= u'Práctica 2', usecols= 'B:F', skiprows= 20, nrows= 5)
    df2 = pd.read_excel(dataFile, sheet_name= u'Práctica 2', usecols= 'B:F', skiprows= 30, nrows= 5)

    plt.suptitle(u'Fuerzas medidas y estimadas en función del caudal y del ángulo de deflexión')

    # Alpha = 90
    x = df0.iloc[:,1].to_numpy() # Q
    y = df0.iloc[:,0].to_numpy() # G
    
    # G vs Q
    plt.scatter(
        x,
        y,
        c= 'r',
        marker= 'o'
    )
    # G regression line
    regLine = linregress(x, y)
    regLx = [x[0], x[-1]]
    regLy = [regLine.slope * regLx[0] + regLine.intercept, regLine.slope * regLx[-1] + regLine.intercept]
    plt.plot(
        regLx,
        regLy,
        color= 'r',
        linestyle= 'dashed'
    )
    # F vs Q
    plt.plot(
        df0.iloc[:,1], # Q
        df0.iloc[:,3], # F
        color= 'r',
        linestyle= 'solid'
    )
    
    # Alpha = 120
    x = df1.iloc[:,1].to_numpy() # Q
    y = df1.iloc[:,0].to_numpy() # G
    # G vs Q
    plt.scatter(
        x,
        y,
        c= 'g',
        marker= 'o'
    )
    # G regression line
    regLine = linregress(x, y)
    regLx = [x[0], x[-1]]
    regLy = [regLine.slope * regLx[0] + regLine.intercept, regLine.slope * regLx[-1] + regLine.intercept]
    plt.plot(
        regLx,
        regLy,
        color= 'g',
        linestyle= 'dashed'
    )
    # F vs Q
    plt.plot(
        df1.iloc[:,1], # Q
        df1.iloc[:,3], # F
        color= 'g',
        linestyle= 'solid'
    )

    # Alpha = 180
    x = df2.iloc[:,1].to_numpy() # Q
    y = df2.iloc[:,0].to_numpy() # G
    # G vs Q
    plt.scatter(
        x,
        y,
        c= 'b',
        marker= 'o'
    )
    # G regression line
    regLine = linregress(x, y)
    regLx = [x[0], x[-1]]
    regLy = [regLine.slope * regLx[0] + regLine.intercept, regLine.slope * regLx[-1] + regLine.intercept]
    plt.plot(
        regLx,
        regLy,
        color= 'b',
        linestyle= 'dashed'
    )
    # F vs Q
    plt.plot(
        df2.iloc[:,1], # Q
        df2.iloc[:,3], # F
        color= 'b',
        linestyle= 'solid'
    )

    plt.grid(visible=True, which='major', axis='both')
    plt.legend([
        u'Fuerza medida (G) α=90°',
        u'Tendencia fuerza medida (G) α=90°',
        u'Fuerza estimada (F) α=90°',
        u'Fuerza medida (G) α=120°',
        u'Tendencia fuerza medida (G) α=120°',
        u'Fuerza estimada (F) α=120°',
        u'Fuerza medida (G) α=180°',
        u'Tendencia fuerza medida (G) α=180°',
        u'Fuerza estimada (F) α=180°'
    ])
    plt.xlabel(u'Caudal, Q [m³/s]')
    plt.ylabel(u'Fuerzas, (F, G) [N]')

    #plt.tight_layout()
    #plt.savefig(figureFile)
    plt.show()

    pass

def isFileNewer(reference, toCompare):
    if getmtime(toCompare) > getmtime(reference):
        return True
    else:
        return False

if __name__ == '__main__':
    main()
    print('Data was analyzed successfully. Have a nice day.')
