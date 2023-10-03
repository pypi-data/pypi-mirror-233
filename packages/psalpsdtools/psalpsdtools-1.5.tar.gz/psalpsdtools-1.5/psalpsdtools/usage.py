#from psalpsdtools import Edrw
from Edrw import Edrw

# SET REGION TO PROCESS
regName = "Central Visayas"
# SET QUARTER, ALSO USED IN READING THE S-D FILE
qtr = "Q2"
# SET FOLDER OF SOURCES/FINAL FILES INCLUDING S-D FILE
baseFolder = "C:/EDRW/Q2"
# SET S-D FILE NAME
sdFile = 'Duck_SD Q2 2023.xlsm'
# COMMODITY 08=chicken, 09=duck, etc.
commcode = '09'
# Year
yr = '23'

myedrw = Edrw()
myedrw.update_sources(regName,qtr,baseFolder,sdFile,commcode,yr)