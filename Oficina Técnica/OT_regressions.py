#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 05/11/2022
Project: Technical Office graphs

File: OT_regressions.py

Abstract: just another grapher

Sources:
'''

import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk
import SciencePlots # Using my distribution, needs import
from scipy.stats import linregress

def main():
    #plt.clf()
    plt.style.use(['science'])
    fig, ax = plt.subplots()

    # Superior title
    fig.suptitle('Regresiones de la demanda', **{'fontsize': 'x-large'})

    x_months = np.array(['Enero','Febrero','Marzo','Abril','Mayo','Junio',
                         'Julio','Agosto','Septiembre','Octubre','Noviembre',
                         'Diciembre'])

    y_ene_jun = np.array([500, 510, 530, 535, 542, 570])
    y_jul_dic = np.array([950, 970, 1000, 1050, 1075, 1100])

    # Meses menor demanda
    x = np.arange(0,6)
    y = y_ene_jun
    # Barras de demandas
    ax.bar(x_months[:6], y, edgecolor="k",
           label='Demanda: meses de menor demanda')
    # Regresión
    regLine = linregress(x, y)
    regLx = [min(x), max(x)]
    regLy = [regLine.slope * regLx[0] + regLine.intercept, regLine.slope * regLx[-1] + regLine.intercept]
    print(rf'D= {regLine.slope:.4f}·(i_mes)+{regLine.intercept:.4f}')
    plt.plot(
        regLx,
        regLy,
        color= 'mediumorchid',
        linestyle= 'dashed',
        linewidth = '5',
        label= 'Regresión lineal: meses de menor demanda'
    )
    # Previsiones: Baja demanda
    regLy = [regLine.slope * 6 + regLine.intercept, regLine.slope * 11 + regLine.intercept]
    plt.plot(
        regLx,
        regLy,
        color= 'indigo',
        linestyle= 'dashed',
        linewidth = '5',
        label= 'Extrapolación siguiente año: alta demanda'
    )

    # Meses de mayor demanda
    x = np.arange(6,12)
    y = y_jul_dic
    # Barras de demanda
    ax.bar(x_months[6:], y, edgecolor="k",
           label='Demanda: meses de mayor demanda')
    # Regresión
    regLine = linregress(x, y)
    regLx = [min(x), max(x)]
    regLy = [regLine.slope * regLx[0] + regLine.intercept, regLine.slope * regLx[-1] + regLine.intercept]
    print(rf'D= {regLine.slope:.4f}·(i_mes-6)+{regLine.intercept:.4f}')
    plt.plot(
        regLx,
        regLy,
        color= 'crimson',
        linestyle= 'dashed',
        linewidth = '5',
        label= 'Regresión lineal: meses de mayor demanda'
    )
    # Previsiones: Alta demanda
    regLy = [regLine.slope * 12 + regLine.intercept, regLine.slope * 17 + regLine.intercept]
    plt.plot(
        regLx,
        regLy,
        color= 'deeppink',
        linestyle= 'dashed',
        linewidth = '5',
        label= 'Extrapolación siguiente año: alta demanda'
    )


    ax.set_xticks(np.arange(0,12))
    ax.set_xticklabels(x_months)

    plt.xlabel(r'Mes')
    plt.ylabel(r'Demanda')
    plt.grid()
    plt.legend()

    # mplcyberpunk.add_glow_effects()

    plt.tight_layout()
    # plt.savefig('some_title.png')
    plt.show()

if __name__ == '__main__':
    main()
    print('☭Data was analyzed successfully. Have a nice day☭')
