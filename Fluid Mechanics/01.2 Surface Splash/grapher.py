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

from os.path import getmtime, join
from numpy import poly1d, linspace, polyfit
import matplotlib.pyplot as plt
import pandas as pd

dataPath   = '..\\00 data'
outputPath = 'out'

dataFile   = join(dataPath, 'Lab1.xlsx')
figureFile = join(outputPath, 'Figure_1.png')

quadEc = lambda x, a, b, c: a+x**2 + b*x + c

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
        marker= 'o',
        label= u'Fuerza medida (G) α=90°'
    )
    # Regression G vs Q
    model = poly1d(polyfit(x, y, 2))
    regLx = linspace(min(x), max(x), 50)
    regLy = model(regLx)
    plt.plot(
        regLx,
        regLy,
        c= 'r',
        linestyle= 'dashed',
        label= u'Tendencia fuerza medida (G) α=90°'
    )

    # F vs Q
    plt.plot(
        df0.iloc[:,1], # Q
        df0.iloc[:,3], # F
        color= 'r',
        linestyle= 'solid',
        label= u'Fuerza estimada (F) α=90°'
    )
    
    # Alpha = 120
    x = df1.iloc[:,1].to_numpy() # Q
    y = df1.iloc[:,0].to_numpy() # G
    # G vs Q
    plt.scatter(
        x,
        y,
        c= 'g',
        marker= 'o',
        label= u'Fuerza medida (G) α=120°'
    )
    # Regression G vs Q
    model = poly1d(polyfit(x, y, 2))
    regLx = linspace(min(x), max(x), 50)
    regLy = model(regLx)
    plt.plot(
        regLx,
        regLy,
        c= 'g',
        linestyle= 'dashed',
        label= u'Tendencia fuerza medida (G) α=120°'
    )

    # F vs Q
    plt.plot(
        df1.iloc[:,1], # Q
        df1.iloc[:,3], # F
        color= 'g',
        linestyle= 'solid',
        label= u'Fuerza estimada (F) α=120°'
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
    # Regression G vs Q
    model = poly1d(polyfit(x, y, 2))
    regLx = linspace(min(x), max(x), 50)
    regLy = model(regLx)
    plt.plot(
        regLx,
        regLy,
        c= 'b',
        linestyle= 'dashed',
        label= u'Tendencia fuerza medida (G) α=180°'
    )

    # F vs Q
    plt.plot(
        df2.iloc[:,1], # Q
        df2.iloc[:,3], # F
        color= 'b',
        linestyle= 'solid',
        label= u'Fuerza medida (G) α=180°'
    )

    plt.grid(visible=True, which='major', axis='both')
    plt.legend()
    plt.xlabel(u'Caudal, Q [m³/s]')
    plt.ylabel(u'Fuerzas, (F, G) [N]')

    #plt.tight_layout()
    #plt.savefig(figureFile)
    plt.show()

    pass

if __name__ == '__main__':
    main()
    print('Data was analyzed successfully. Have a nice day.')
