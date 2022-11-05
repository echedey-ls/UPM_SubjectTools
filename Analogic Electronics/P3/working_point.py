#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 24/10/2022
Project: Plotter for DC and AC load lines on a transistor

File: working_point.py

Abstract: just another grapher

Sources:
'''

import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk
import SciencePlots # Using my distribution, needs import

def main():
    plt.clf()
    plt.style.use(['science'])
    # Superior title
    plt.suptitle('Rectas de carga', **{'fontsize': 'x-large'})

    # Pto trabajo
    I_Cq, V_CEq = (0.941597628282497, 8.05181101254995)
    plt.scatter(x=V_CEq, y=I_Cq, color='black', marker='o', label='Punto de trabajo')

    # Corriente Ic
    plt.plot([0.2, 15.6], [0.941597628282497, 0.941597628282497],
        linestyle=(0, (3, 5, 1, 5)), # dashdotted linestyle. See https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
        color='b'
    )
    
    # Carga en DC
    plt.plot(
        [0, 15.6],
        [1.94601950555682, 0],
        label='Recta de carga en DC'
    )

    # Carga en AC
    coeff = -0.177194245462753
    deltaX = I_Cq / coeff
    ac_load_line_x = np.array([V_CEq - deltaX, V_CEq + deltaX])
    ac_load_line_y = (ac_load_line_x-V_CEq)*coeff + I_Cq

    plt.plot(
        ac_load_line_x,
        ac_load_line_y,
        color='r',
        linestyle=(0, (5, 5)), # custom dashed linestyle. See https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
        label='Recta de carga en AC'
    )

    plt.xlabel(r'$V_{CE} [V]$')
    plt.ylabel(r'$I_{C} [mA]$')
    plt.grid()
    plt.legend()

    # mplcyberpunk.add_glow_effects()

    # plt.tight_layout()
    # plt.savefig('some_title.png')
    plt.show()

if __name__ == '__main__':
    main()
    print('☭Data was analyzed successfully. Have a nice day☭')
