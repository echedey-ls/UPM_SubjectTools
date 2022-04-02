#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 29/03/2022
Project: Data analysis of fluid mechanichs lab

File: grapher.py

Abstract: just another graph x2

Sources:
'''

from os.path import getmtime, join, exists
from scipy.stats import linregress
from math import sqrt
import matplotlib.pyplot as plt
import pandas as pd

paths = {
    'rawDataDir': '../00 data',
    'outputPath': 'out'
}
paths['rawDataFile'] = paths['rawDataDir'] + '/Lab2.xlsx'

def main():
    # Dataframe with flow and height square root
    df0 = pd.read_excel(
        paths['rawDataFile'], 
        sheet_name= u'orificio', 
        usecols= 'G:H', 
        skiprows= 24, 
        nrows= 8
        )
    # Dataframe with discharge coeff and height
    df1 = pd.read_excel(
        paths['rawDataFile'], 
        sheet_name= u'orificio', 
        usecols= 'F,I', 
        skiprows= 24, 
        nrows= 8
    )

    # Q vs sqrt(h)
    x = df0.iloc[:,1].to_numpy() # sqrt(h)
    y = df0.iloc[:,0].to_numpy() # Q
    plt.scatter(
        x,
        y,
        c= 'b',
        marker= 'o',
        label= 'Caudal respecto raíz de la altura'
    )
    regLine = linregress(x, y)
    regLx = [x[0], x[-1]]
    regLy = [regLine.slope * regLx[0] + regLine.intercept, regLine.slope * regLx[-1] + regLine.intercept]
    plt.plot(
        regLx,
        regLy,
        color= 'b',
        linestyle= 'dashed',
        label= 'Regresión lineal de los puntos'
    )
    plt.text(
        15.5,
        0.000174,
        f'y = {regLine.slope:.8f}x + {regLine.intercept:.8f}\nr² = {regLine.rvalue**2:.5f}'
    )
    print('Lineregress of Q vs sqrt(h):')
    print('\tSlope:     '+str(regLine.slope))
    print('\tIntercept: '+str(regLine.intercept))

    # Ideal discharge line
    idealX = x
    idealY = 0.000132732289614169*sqrt(2*9.81)*idealX/sqrt(1000)
    plt.plot(
        idealX,
        idealY,
        color= 'orange',
        linestyle= 'dashed',
        label= 'Descarga ideal'
    )

    plt.xlabel('Raíz cuadrada de h, [mm^(1/2)]')
    plt.ylabel('Caudales, Q [m³/s]')
    plt.legend()

    plt.tight_layout()
    plt.show()

    # Cd respect to h
    plt.cla()

    x = df1.iloc[:,0].to_numpy() # Cd [1]
    y = df1.iloc[:,1].to_numpy() # h [mm]

    plt.scatter(
        x,
        y,
        c= 'b',
        marker= 'o',
        label= 'Cd'
    )

    regLine = linregress(x, y)
    regLx = [x[0], x[-1]]
    regLy = [regLine.slope * regLx[0] + regLine.intercept, regLine.slope * regLx[-1] + regLine.intercept]
    plt.plot(
        regLx,
        regLy,
        color= 'b',
        linestyle= 'dashed',
        label= 'Regresión lineal de los coeficientes de descarga'
    )

    plt.xlabel('Altura, h [mm]')
    plt.ylabel('Coeficiente de descarga, Cd [1]')
    plt.legend()

    plt.tight_layout()
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
