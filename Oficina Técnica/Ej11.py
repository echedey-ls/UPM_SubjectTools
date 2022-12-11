#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 2022-12-11
Project: Technical Office graphs

File: Ej11.py

Abstract: Práctica 11, gráficas y regresiones, lo que toque

Sources:
'''

import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk
import scienceplots
from scipy.stats import linregress

def main():
    #plt.clf()
    plt.style.use(['science', 'dark_background'])
    fig, ax1 = plt.subplots()

    # Superior title
    fig.suptitle('Tiempo unitario vs piezas de pedido',
                 **{'fontsize': 'x-large'})

    # Apartado b
    ax1.set_title('Apartado (b)')
    ax1.set_xlabel(r'Tamaño del pedido [$uds.$]')
    ax1.set_ylabel(r'Tiempo unitario (por pieza) [$min$]')

    x_piezas = np.array([5, 10, 16, 17, 25, 32, 33, 40, 48, 49, 56, 64, 65,
                         73, 80, 81, 89, 96, 97, 105, 112, 113, 121, 128])
    y_tpo_ud = np.array([24.000, 12.000, 7.500, 14.118, 9.600, 7.500, 10.909,
                         9.000, 7.500, 9.796, 8.571, 7.500, 9.231, 8.219,
                         7.500, 8.889, 8.090, 7.500, 8.660, 8.000, 7.500,
                         8.496, 7.934, 7.500])

    ax1.scatter(x_piezas,
                y_tpo_ud,
                marker='2',
                color='yellow',
                label='Tiempo unitario en función del número de piezas')


    ax1.grid()
    ax1.legend()

    plt.show()

if __name__ == '__main__':
    main()
    print('☭Data was analyzed successfully. Have a nice day☭')
