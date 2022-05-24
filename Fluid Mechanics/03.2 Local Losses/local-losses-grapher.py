#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 23/05/2022
Project: Data analysis of fluid mechanichs lab

File: local-losses-grapher.py

Abstract: just another graphing script x4 for the local losses practice

Sources:
'''

from os.path import getmtime, join
from turtle import width
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd

paths = {
    'rawDataDir': '../00 data',
    'outputPath': 'out',
    'cachedData': 'cached'
}
paths['rawDataFile'] = join(paths['rawDataDir'], 'Lab3.xlsx')

ignoreCache = False

def lossesCharts(plotEnv):
    df = pd.read_excel(
        paths['rawDataFile'],
        sheet_name= u'DATOS Perdida Carga Local', 
        usecols= 'D:O', 
        skiprows= 28, 
        nrows= 5
    )
    dataTitles = (
        'Ensanchamiento',
        'Estrechamiento',
        'Codo largo',
        'Codo corto',
        'Codo 90°',
        'Inglete'
    )
    for id in range(len(df.columns)//2-1):
        title = dataTitles[id]
        print(title.upper())
        xvals = df.iloc[:,id*2]
        yvals = df.iloc[:,id*2+1]
        p = plotEnv.scatter(
            xvals,
            yvals,
            label= title+': pérdidas con respecto $h_c$',
            zorder= 5 + id
        )
        popt, _ = curve_fit(lambda x,m: m*x, xvals, yvals)
        slope, = popt
        print(f'Slope: {slope}')
        regLx = (0, max(xvals))
        regLy = (0, slope * regLx[1])
        plotEnv.plot(
            regLx,
            regLy,
            label= 'Ajuste '+title,
            color= p.colorbar,
            linestyle= '-.',
            zorder= 5 - id
        )

    plotEnv.suptitle('Pérdidas de carga locales en función de la altura cinética')
    plotEnv.legend()
    plotEnv.xlabel('Altura cinética $h_c\:[m]$')
    plotEnv.ylabel('Diferencia de alturas de presión $\Delta H\:[m]$')
    plotEnv.show()
    return

def valveLosses(plotEnv):
    data = (
        (
            'Poco abierta',
            pd.read_excel(
                paths['rawDataFile'],
                sheet_name= u'DATOS Perdida Carga Local', 
                usecols= 'S:T', 
                skiprows= 28, 
                nrows= 6
            )
        ),
        (
            'Más abierta',
            pd.read_excel(
                paths['rawDataFile'],
                sheet_name= u'DATOS Perdida Carga Local', 
                usecols= 'AA:AB', 
                skiprows= 28, 
                nrows= 6
            )
        )
    )

    for title, df in data:
        print(title.upper())
        xvals = df.iloc[:,0]
        yvals = df.iloc[:,1]
        p = plotEnv.scatter(
            xvals,
            yvals,
            label= 'Válvula '+title.lower()
        )
        popt, _ = curve_fit(lambda x,m: m*x, xvals, yvals)
        slope, = popt
        print(f'Slope: {slope}')
        regLx = (0, max(xvals))
        regLy = (0, slope * regLx[1])
        plotEnv.plot(
            regLx,
            regLy,
            label= 'Ajuste \''+title.lower()+'\'',
            color= p.colorbar,
            linestyle= '-.'
        )
    plotEnv.suptitle('Pérdida de carga local en la válvula', y=0.975)
    plotEnv.title('Respecto de $h_c$', fontsize='medium')
    plotEnv.legend()
    plotEnv.xlabel('Altura cinética $h_c\:[m]$')
    plotEnv.ylabel('Diferencia de alturas de presión $\Delta H\:[m]$')
    plotEnv.show()
    return

if __name__ == '__main__':
    # Initialize matplotlib styles
    plt.style.use(['latex-sans','science','grid','std-colors'])
    plt.rcParams.update({
        'figure.dpi': '125',
        'figure.figsize': '8, 5'
    })
    #lossesCharts(plt)
    valveLosses(plt)
    print('Data was analyzed successfully. Have a nice day.')
