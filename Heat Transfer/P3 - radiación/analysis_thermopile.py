#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 13/03/2022
Project: Data analysis of heat transfer lab

File: analysis_thermopile.py

Abstract: Correlation of U(thermopile) with respect to Temperature, depending on the surface

Sources:
'''

from os import mkdir
from os.path import join, exists, getmtime
from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dataPath       = 'data'
rawDataPath    = join(dataPath, 'raw')
parsedDataPath = join(dataPath, 'parsed')
outputDataPath = join(dataPath, 'out')

dataFiles = [
    ('Cara Negra','caraNegra.txt', 'darkturquoise', 'blue'), 
    ('Cara Blanca','caraBlanca.txt', 'gold', 'orangered'), 
    ('Cara Brillante','caraBrillante.txt', 'lime', 'green'), 
    ('Cara Mate','caraMate.txt', 'palevioletred', 'crimson')
]
outputDataFile = join(outputDataPath, 'todasLasCaras.xlsx')

recomputeOverride = False
remakeGraphs      = True

class dataVars:
    C_to_K_const = 273.15
    AmbTemp_C = 18.4
    AmbTemp_K = AmbTemp_C + C_to_K_const

def main():
    # Check that subfolders have been created
    for path in (dataPath, rawDataPath, parsedDataPath, outputDataPath):
        if not exists(path):
            print(f'Path {path} not found. Creating it...')
            mkdir(path)
    for dataName, fileName, _, _ in dataFiles:
        if not exists( join(rawDataPath, fileName) ):
            raise IOError(f'Data file {fileName} not found for dataset {dataName}')

    all_u_vs_temp = []
    with pd.ExcelWriter(outputDataFile) as writer:
        pd.DataFrame().to_excel(writer, sheet_name='Sheet', index=True)
        for dataName, fileName, color, regColor in dataFiles:
            print(f'Working on file {fileName}')
            rawFile    = join(rawDataPath, fileName)
            parsedFile = join(parsedDataPath, fileName+'.csv')
            graphFile  = join(outputDataPath, dataName+'.png')
            if not exists(parsedFile) or isFileNewer(parsedFile, rawFile) or recomputeOverride:
                print('\tRaw data was updated or parsed data not found, reading from raw...')
                readDf = readCustomInput(join(rawDataPath, fileName))
                try:
                    readDf.to_csv(parsedFile)
                    print('\t\tSuccessfully saved DataFrame to CSV file as parsed data.')
                except Exception as e:
                    print('\t\tError while creating parsed data file!')
                    print(e)
            else:
                print('\tFound cached file.')
                readDf = pd.read_csv(parsedFile, dtype= float)
                readDf.drop(readDf.columns[0], axis=1, inplace=True)
            print('\tReading complete.')

            customDf = generateCustomDf(readDf)

            # Merge pandas dataframes into different sheets of one excel sheet
            if isFileNewer(outputDataFile, rawFile) or recomputeOverride:
                print('\tData appended to final file.')
                customDf.to_excel(writer, sheet_name=fileName, index=False)

            # Graphs output
            if isFileNewer(graphFile, rawFile) or remakeGraphs:
                plt.clf()
                plt.suptitle(dataName)

                axs0 = plt.subplot(2,2,1)
                axs1 = plt.subplot(2,2,2)
                axs2 = plt.subplot(2,1,2)
                
                axs0.plot(customDf.iloc[:,0], # Time
                          customDf.iloc[:,2], # Temperature
                          color= color
                )
                axs0.set_title('Temperatura respecto el tiempo')
                axs0.set_xlabel('t (s)')
                axs0.set_ylabel('T (K)')
                axs0.grid(visible=True, which='major', axis='both')

                axs1.plot(customDf.iloc[:,0], # Time
                          customDf.iloc[:,4], # Voltage
                          color= color
                )
                axs1.set_title('Tensión respecto al tiempo')
                axs1.set_xlabel('t (s)')
                axs1.set_ylabel('U (V)')
                axs1.grid(visible=True, which='major', axis='both')

                axs2.plot(customDf.iloc[:,2], # Temperature
                          customDf.iloc[:,4], # Voltage
                          color= color
                )
                axs2.set_title('Tensión respecto temperatura')
                axs2.set_xlabel('T (K)')
                axs2.set_ylabel('U (V)')
                axs2.grid(visible=True, which='major', axis='both')

                plt.tight_layout()
                plt.savefig(graphFile)
                print('\tGraphs saved.')
            else:
                print('No changes from last execution - new graphs haven\'t been generated')
            all_u_vs_temp.append( (
                dataName,
                customDf.iloc[:,3], # Diffs of fourth power of temps
                customDf.iloc[:,4], # Voltage
                color,
                regColor
                )
            )
        # end of For loop
        
        plt.clf()
        outImgUvsTdiffs = join(outputDataPath, 'tempDiffsAndU.png')
        if any(map(isFileNewer, (outImgUvsTdiffs,)*3, [join(rawDataPath,dFile[1]) for dFile in dataFiles])):
            plt.suptitle(u'Relación voltaje vs '+u'T\u2074 - Ta\u2074 (K\u2074)')
            for dataName, x, y, color, regColor in all_u_vs_temp:
                plt.plot(
                    x, 
                    y,
                    color= color,
                    label= dataName
                )
                regLine = linregress(x, y)
                print(
                    f'Line regression of '+dataName,
                    f'  -> Slope: {regLine.slope} ',
                    f'  -> Standard deviation: {regLine.stderr}',
                    sep= '\n'
                )
                regLx = [min(x), max(x)]
                regLy = [
                    regLine.slope * regLx[0]  + regLine.intercept,
                    regLine.slope * regLx[-1] + regLine.intercept
                ]
                plt.plot(
                    regLx,
                    regLy,
                    label= 'Ajuste '+dataName,
                    color= regColor,
                    linestyle= 'dashed'
                )

            
            plt.legend()
            plt.xlabel(u'T\u2074 - Ta\u2074 (K\u2074)')
            plt.ylabel(u'Tensión de la termopila (mV)')
            plt.tight_layout()
            plt.savefig( outImgUvsTdiffs )
            plt.show()
        else:
            print('Last graph was already generated. Skipping...')

def readCustomInput(filePath):
    df = pd.DataFrame( columns=['TIME', 'TEMP', 'VOLT'] )
    with open(filePath, 'r') as file:
        for line in file.readlines():
            if (not line[:1].isdigit()): # Line does not have the data we want (doesn't start with a number), or is empty (:1 accesor trick)
                continue
            splittedLine = line.split('\t')
            df = pd.concat([df,
                            pd.DataFrame({
                                'TIME': [float(splittedLine[0].replace(',','.'))], 
                                'TEMP': [float(splittedLine[1].replace(',','.'))], 
                                'VOLT': [float(splittedLine[3].replace(',','.'))]
                                }, dtype= float)],
                            ignore_index=True)
    return df

def generateCustomDf(dataframe):
    tempKelvin  = dataframe['TEMP'] + dataVars.C_to_K_const
    temp4sDiffs = np.power(tempKelvin, 4) - np.power(dataVars.AmbTemp_K, 4)

    newDf = pd.DataFrame( {
                               u't (s)': dataframe['TIME'],
                           u'T (\xB0C)': dataframe['TEMP'],
                               u'T (K)': tempKelvin,
        u'T\u2074 - Ta\u2074 (K\u2074)': temp4sDiffs,
                              u'U (mV)': dataframe['VOLT']
    }, dtype= float ) # This dtype solves numbers being assigned object type when they are read from raw file
    return newDf

def isFileNewer(reference, toCompare):
    return getmtime(toCompare) > getmtime(reference)

if __name__ == '__main__':
    main()
    print('Data was analyzed successfully. Have a nice day.')
