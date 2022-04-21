"""
     This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
"""

from os.path import exists
import pandas as pd

class appGlobals:
    dataFilepath     = "Data\\"
    fileOriginalData = dataFilepath + "EnglishSurveyPersonal.csv" # Not the name I'm most proud of
    fileClearedData  = dataFilepath + "EnglishSurveyCleared.csv"

def main():
    if not exists(appGlobals.fileClearedData): # If file without personal and useless data does not exist
        if not exists(appGlobals.fileOriginalData): # Raise an error for inexistent data source file
            raise IOError("Couldn't find file with original data!")
        original = pd.read_csv(appGlobals.fileOriginalData, # Read origin CSV file
            header= 0, 
            names= ["TEMP", "EMAIL", "POSITION", "HEARING", "DISTRACTED", "USAGE"])
        data = original.drop(columns= ["TEMP", "EMAIL"]) # Drop that unused and useless data
        data.to_csv(appGlobals.fileClearedData) # And save so we can read from it again in the future
        print("New CSV file was created! Dropped timestamp and email.")
        print("USING FILE: " + appGlobals.fileOriginalData)

    else:
        print("Using saved data without useless information")
        print("USING FILE: " + appGlobals.fileClearedData)
        data = pd.read_csv(appGlobals.fileClearedData, 
            header= 0, 
            names= ["POSITION", "HEARING", "DISTRACTED", "USAGE"])

    # print(data)

    positionValues = data["POSITION"].unique()
    hearingValues  = data["HEARING"] .unique()
    usageValues    = data["USAGE"]   .unique()

    print("Question 2 answers by position of student:")
    for posVal in positionValues:
        tempData = data[ data["POSITION"] == posVal ]
        print("--> " + str(posVal).upper())
        for hearVal in hearingValues:
            countOf = len(tempData[ tempData["HEARING"] == hearVal])
            print(f"{hearVal}: {countOf}")

    print("Question 4 answers by position of student:")
    for posVal in positionValues:
        tempData = data[ data["POSITION"] == posVal ]
        print("--> " + str(posVal).upper())
        for useVal in usageValues:
            countOf = len(tempData[ tempData["USAGE"] == useVal])
            print(f"{useVal}: {countOf}")
    pass

if __name__ == "__main__":
    main()
