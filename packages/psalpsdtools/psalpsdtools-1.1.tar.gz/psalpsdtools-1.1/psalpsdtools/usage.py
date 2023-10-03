from psalpsdtools import Edrw

# SET REGION TO PROCESS
regName = "Central Luzon"
# SET QUARTER, ALSO USED IN READING THE S-D FILE
qtr = "Q2"
# SET FOLDER OF SOURCES/FINAL FILES INCLUDING S-D FILE
baseFolder = "D:/EDRW/Q2"
# SET S-D FILE NAME ex. Chicken_SD Q1 2023.xlsm
sdFile = 'Duck_SD Q2 2023.xlsm'
# COMMODITY 08=chicken, 09=duck, etc.
commcode = '09'
# Year
yr = '23'

myedrw = Edrw()
myedrw.update_sources(regName,qtr,baseFolder,sdFile,commcode,yr)