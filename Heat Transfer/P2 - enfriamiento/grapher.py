#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 16/03/2022
Project: Data analysis of heat transfer lab

File: grapher.py

Abstract: Temperature evolution of a hot metal rod

Sources:
'''

from os import mkdir
from os.path import join, exists, getmtime
from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

outputDataPath = 'out'

dataFiles = (
    ('Cilindro Claro' , 'cilindroClaro.csv' ),
    ('Cilindro Oscuro', 'cilindroOscuro.csv')
)

class dataVars:
    C2K_const = 273.15
    AmbTemp_C = 18.4
    AmbTemp_K = AmbTemp_C + C2K_const

def main():
    if not exists(outputDataPath):
        print('Output data filepath not found. Creating one...')
        mkdir(outputDataPath)

    for (setName, dataFile) in dataFiles:
        print('Working on dataset '+setName)

        df = pd.read_csv(dataFile, sep=';', decimal=',', skiprows=4, names=['t', 'T'])
        df.insert(2, u'T₀', dataVars.AmbTemp_C)
        df.insert(3, u'ΔT', df['T'] - df['T₀'])
        df.insert(4, u'lnΔT', np.log(df[u'ΔT']))

        df.to_csv(join(outputDataPath, 'Data'+setName.replace(' ', '')+'.csv'))
        print('Data CSV created successfully.')

        plt.clf()
        # Superior title
        plt.suptitle(setName, **{'fontsize': 'x-large'})
        # Subtitle

        plt.grid(which='major', axis='both')

        ax0 = plt.subplot(2,1,1)
        ax0.set_title(u'Evolución de la temperatura con el tiempo')
        ax0.plot(
            df['t'],
            df[u'ΔT'],
            label= 'Diferencia de temperatura cilindro-ambiente'
        )
        ax0.set_xlabel(u'Tiempo (t) [s]')
        ax0.set_ylabel(u'Temperatura (T) [\xB0C]')
        ax0.legend()

        ax1 = plt.subplot(2,1,2)
        ax1.set_title(u'Evolución del logaritmo natural de dicha diferencia')
        x = df['t'].to_numpy()
        y = df[u'lnΔT'].to_numpy()
        ax1.plot(
            x,
            y,
            label= 'ln(T - T₀)'
        )
        # Regression calc, print and plot
        regLine = linregress(x, y)
        print(
            f'Line regression of ln(ΔT):',
            f'  -> Slope: {regLine.slope} ',
            f'  -> Standard deviation: {regLine.stderr}',
            sep= '\n'
        )
        regLx = [x[0], x[-1]]
        regLy = [
            regLine.slope * regLx[0]  + regLine.intercept,
            regLine.slope * regLx[-1] + regLine.intercept
        ]
        ax1.plot(
            regLx,
            regLy,
            label= 'Ajuste lineal de la curva',
            color= 'mediumblue',
            linestyle= 'dashed'
        )
        ax1.set_xlabel(u'Tiempo (t) [s]')
        ax1.set_ylabel(u'Temperatura (T) [°C]')
        ax1.legend()

        plt.tight_layout()
        plt.savefig(join(outputDataPath, 'Graph'+setName.replace(' ', '')+'.png'))
    return

if __name__ == '__main__':
    main()
    print('☭Data was analyzed successfully. Have a nice day☭')
