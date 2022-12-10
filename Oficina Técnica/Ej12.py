#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 2022-12-10
Project: Technical Office graphs

File: Ej12.py

Abstract: Práctica 12, gráficas y regresiones, lo que toque

Sources:
'''

import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk
import scienceplots
from scipy.stats import linregress

def main():
    #plt.clf()
    plt.style.use(['science'])
    fig, ax1 = plt.subplots()

    # Superior title
    fig.suptitle('Ánalisis de coste y beneficios', **{'fontsize': 'x-large'})

    C_TA_lin = lambda uds: 10080 + 24.032*uds
    C_TA_fun = lambda uds: 5880 + 28.836*uds

    # Apartado b
    ax1.set_title('Apartado (b)')
    ax1.set_xlabel(r'uds.')
    ax1.set_ylabel(r'€')

    x = np.linspace(0, 2000, 10)

    Bi_lin = lambda uds: 30*uds - C_TA_lin(uds)
    Bi_fun = lambda uds: 30*uds - C_TA_fun(uds)

    ax1.plot(x, C_TA_lin(x), label='Coste dist. en línea')
    ax1.plot(x, C_TA_fun(x), label='Coste dist. funcional')
    ax1.plot(x, Bi_lin(x), label='Beneficio dist. en línea')
    ax1.plot(x, Bi_fun(x), label='Beneficio dist. funcional')

    ax1.grid()
    ax1.legend()

    plt.show()
    plt.clf()
    
    # Apartado f
    fig, ax2 = plt.subplots()
    ax2.set_title('Apartado (f)')
    ax2.set_xlabel(r'uds.')
    ax2.set_ylabel(r'€')

    Bi_lin2 = lambda uds: 34.11*uds - C_TA_lin(uds)
    Bi_fun2 = lambda uds: 34.72*uds - C_TA_fun(uds)

    ax2.plot(x, Bi_lin2(x), label='Beneficio dist. lin. - PV ajustado')
    ax2.plot(x, Bi_fun2(x), label='Beneficio dist. fun. - PV ajustado')

    ax2.grid()
    ax2.legend()

    # mplcyberpunk.add_glow_effects()

    plt.tight_layout()
    # plt.savefig('some_title.png')
    plt.show()

if __name__ == '__main__':
    main()
    print('☭Data was analyzed successfully. Have a nice day☭')
