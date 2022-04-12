#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 02/04/2022
Project: Data analysis of fluid mechanichs lab

File: grapher.py

Abstract: just another graphing script x3

Sources:
'''

from os import mkdir
from os.path import exists, getmtime, join
from math import pi, sqrt, tan
from numpy import linspace
from scipy.stats import linregress
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
import pickle

paths = {
    'rawDataDir': '../00 data',
    'outputPath': 'out',
    'cachedData': 'cached'
}
paths['rawDataFile'] = join(paths['rawDataDir'], 'Lab2.xlsx')

ignoreCache = False

b = 0.03 # Spillway width [m]
theta = pi/2 # Spillway angle [rad]

def flowVSheightPowerCharts():
    ## Dataframes tuple ((title, dataframe, h^x, flow function ideal cond.),x2)
    dataTuple = (
        ('rectangular', 
            pd.read_excel(
                paths['rawDataFile'], 
                sheet_name= u'vertedero', 
                usecols= 'B,C', 
                skiprows= 14, 
                nrows= 7),
            3, # Relation exponent
            lambda fH: 2/3*sqrt(2*9.81)*b*fH # idealFlow func
        ),
        ('triangular', 
            pd.read_excel(
                paths['rawDataFile'], 
                sheet_name= u'vertedero', 
                usecols= 'D,E', 
                skiprows= 14, 
                nrows= 7),
            5, # Relation exponent
            lambda fH: 8/15*tan(theta/2)*sqrt(2*9.81)*fH # idealFlow func
        )
    )
    
    for dataName, dataSet, exponent, idealFlow in dataTuple:
        print(f'Analyzing dataset {dataName.upper()}:')
        # Q vs f(h)
        dtaX = dataSet.iloc[:,0].to_numpy() # f(h)
        dtaY = dataSet.iloc[:,1].to_numpy() # Q

        plt.scatter(
            dtaX,
            dtaY,
            c= 'b',
            marker= 'o',
            label= 'Caudal experimental'
        )

        popt, _ = getLineSlope(dataName, paths['rawDataFile'], lambda x, m: m*x, dtaX, dtaY)
        slope, = popt
        print(f'\tRegression line slope: {slope}')
        
        regLx = [min(dtaX), max(dtaX)]
        regLy = [slope * regLx[0], slope * regLx[-1]]
        plt.plot(
            regLx,
            regLy,
            color= 'b',
            linestyle= 'dashed',
            label= rf'Regresión por origen: $Q={slope:.4f} \cdot h^\frac{exponent}{{2}}$'
        )

        # Ideal discharge line
        idealX = (min(dtaX), max(dtaX))
        idealY = list(map(idealFlow, idealX))
        plt.plot(
            idealX,
            idealY,
            color= 'orange',
            linestyle= 'dashed',
            label= 'Descarga ideal'
        )

        plt.xlabel(rf'$h^\frac{exponent}{2}, [m^\frac{exponent}{2}]$')
        plt.ylabel(r'$Q, [m^3/s]$')
        plt.legend()

        #plt.tight_layout()
        plt.show()
        
        plt.cla()

    return

def CdVShPwChart():
    print('Point 3')
    df = pd.read_excel(
        paths['rawDataFile'], 
        sheet_name= u'vertedero', 
        usecols= 'B:E', 
        skiprows= 34, 
        nrows= 7
    ).drop(index= 4)
    print(df)
    
    dtaX  = df.iloc[:,0].to_numpy() # h/Pw
    dtaY1 = df.iloc[:,2].to_numpy() # Cd
    dtaY2 = df.iloc[:,3].to_numpy() # Cd,corr

    sdtaX = (min(dtaX ), max(dtaX ))
    sdtaY = (min(dtaY2), max(dtaY2))

    plt.scatter(
        dtaX,
        dtaY1,
        c= 'b',
        marker= 'o',
        label= 'Coef. descarga experimental'
    )
    regLine = linregress(dtaX, dtaY1)
    regLx = (min(dtaX), max(dtaX))
    regLy = [regLine.slope * regLx[0] + regLine.intercept, regLine.slope * regLx[-1] + regLine.intercept]
    plt.plot(
        regLx,
        regLy,
        color= 'r',
        linestyle= 'dashed',
        label= rf'Regresión coefs.: $C_d= {regLine.slope:.4f}·\frac{{H}}{{P_w}}+{regLine.intercept:.4f}$'
    )

    plt.plot(
        sdtaX,
        sdtaY,
        c= 'orange',
        linestyle= 'dashed',
        label= r'Línea coef. descarga propuesta: $C_{d,corr}=0.611+0.075\frac{H}{P_w}$'
    )

    plt.xlabel(r'$\frac{H}{P_w}, [adim.]$')
    plt.ylabel(r'$C_d$ y $ C_{d,corr}, [adim.]$')
    plt.legend(loc= 'upper center')
    plt.show()

    return

def isFileNewer(reference, toCompare):
    return getmtime(toCompare) > getmtime(reference)

def getLineSlope(dataSetName, originFile, func2fit, xvalues, yvalues):
    if not exists(paths['cachedData']):
        mkdir(paths['cachedData'])

    cachedFile = join(paths['cachedData'], dataSetName+'.pickle')
    if not exists(cachedFile) or isFileNewer(cachedFile, originFile) or ignoreCache:
        print('Fitting curve and caching...')
        popt, pcov = curve_fit(func2fit, xvalues, yvalues)
        try:
            with open(cachedFile, "wb") as f:
                pickle.dump((popt, pcov), f, protocol=pickle.HIGHEST_PROTOCOL)
            print('\tFile cached succesfully')
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)
        return popt, pcov
    else:
        try:
            print('Reading from cached file...')
            with open(cachedFile, "rb") as f:
                popt, pcov = pickle.load(f)
                print('\tCached file successfully read')
                return popt, pcov
        except Exception as ex:
            print("Error during unpickling object (Possibly unsupported):", ex)


if __name__ == '__main__':
    # Initialize matplotlib styles
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica"]})
    flowVSheightPowerCharts()
    #CdVShPwChart()
    print('Data was analyzed successfully. Have a nice day.')
