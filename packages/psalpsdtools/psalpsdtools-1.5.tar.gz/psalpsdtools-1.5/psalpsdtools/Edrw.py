from .PhRegPrv import PhRegPrv
from openpyxl import load_workbook
import os
#import xlrd
class Edrw:
    def __init__(self):
        pass
    def update_sources(self, regName, qtr, baseFolder, sdFile, commcode, yr):
        philippines = PhRegPrv()
        selected_regions = philippines.get_regions()
        print(selected_regions)
        for regName in selected_regions:
            selected_provinces = philippines.get_provinces(regName)
            src = load_workbook(filename = baseFolder + "/" + sdFile, keep_vba=True, keep_links=True, rich_text=True)
            if regName == "Ilocos Region":
                regCode = "01"
            elif regName == "Cagayan Valley":
                regCode = "02"
            elif regName == "Central Luzon":
                regCode = "03"
            elif regName == "CALABARZON":
                regCode = "04"
            elif regName == "Bicol Region":
                regCode = "05"
            elif regName == "Western Visayas":
                regCode = "06"
            elif regName == "Central Visayas":
                regCode = "07"
            elif regName == "Eastern Visayas":
                regCode = "08"
            elif regName == "Zamboanga Peninsula":
                regCode = "09"
            elif regName == "Northern Mindanao":
                regCode = "10"
            elif regName == "Davao Region":
                regCode = "11"
            elif regName == "SOCCSKSARGEN":
                regCode = "12"
            elif regName == "NCR":
                regCode = "13"
            elif regName == "CAR":
                regCode = "14"
            elif regName == "BARMM":
                regCode = "15"
            elif regName == "Caraga":
                regCode = "16"
            elif regName == "MIMAROPA Region":
                regCode = "17"

            if commcode == '08':
                src_active = src["native B"] # Get Province Names from this worksheet
                comm_arr = ["native","gamefowl","broiler","layer"]
                srv_arr = [" B"," C","_T"]
                if selected_provinces:
                    for province in selected_provinces:
                        srcFile = str(commcode) + ' ' + str(province) + '_' + str(yr)
                        fileExt = '.xlsm'
                        fpath = str(baseFolder) + '/Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt)
                        if os.path.isfile(fpath) == True:
                            for row in src_active.iter_rows(min_row=17, min_col=1, max_row=135, max_col=1):
                                for cell in row:
                                    if cell.value == province:
                                        #print(f"{province} {cell.row}")
                                        rNumSrc = cell.row

                                        dst = load_workbook(filename=str(baseFolder) + '/Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt))
                                        #dst = xlrd.open_workbook('Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt))
                                        q1_dst_ws = dst[qtr]
                                        #q1_dst_ws = dst.sheet_by_name(qtr)

                                        if os.path.isfile(fpath) == True:
                                            for comm in comm_arr:
                                                for srv in srv_arr:
                                                    if comm == "native":
                                                        if srv == " B":
                                                            rNumDst = 22
                                                        elif srv == " C":
                                                            rNumDst = 28
                                                        elif srv == "_T":
                                                            rNumDst = 34
                                                    elif comm == "gamefowl":
                                                        if srv == " B":
                                                            rNumDst = 40
                                                        elif srv == " C":
                                                            rNumDst = 46
                                                        elif srv == "_T":
                                                            rNumDst = 52
                                                    elif comm == "broiler":
                                                        if srv == " B":
                                                            rNumDst = 58
                                                        elif srv == " C":
                                                            rNumDst = 64
                                                        elif srv == "_T":
                                                            rNumDst = 70
                                                    elif comm == "layer":
                                                        if srv == " B":
                                                            rNumDst = 76
                                                        elif srv == " C":
                                                            rNumDst = 82
                                                        elif srv == "_T":
                                                            rNumDst = 88

                                                    sheetNameSrc = str(comm) + str(srv)
                                                    qtr_src_ws = src[sheetNameSrc]
                                                    print(f"PSA-LPSD (EDRW): Loading source -> {province} - {comm} - {srv}")

                                                    if srv != "_T":
                                                        #print(f"Copying Source B{rNumSrc} to E{rNumDst}")
                                                        q1_dst_ws['E' + str(rNumDst)].value = qtr_src_ws['B' + str(rNumSrc)].value
                                                        q1_dst_ws['F' + str(rNumDst)].value = qtr_src_ws['C' + str(rNumSrc)].value
                                                        q1_dst_ws['H' + str(rNumDst)].value = qtr_src_ws['E' + str(rNumSrc)].value
                                                        q1_dst_ws['I' + str(rNumDst)].value = qtr_src_ws['F' + str(rNumSrc)].value
                                                        q1_dst_ws['J' + str(rNumDst)].value = qtr_src_ws['G' + str(rNumSrc)].value
                                                        q1_dst_ws['M' + str(rNumDst)].value = qtr_src_ws['J' + str(rNumSrc)].value
                                                        q1_dst_ws['N' + str(rNumDst)].value = qtr_src_ws['K' + str(rNumSrc)].value
                                                        q1_dst_ws['Q' + str(rNumDst)].value = qtr_src_ws['N' + str(rNumSrc)].value
                                                        q1_dst_ws['R' + str(rNumDst)].value = qtr_src_ws['U' + str(rNumSrc)].value
                                                        q1_dst_ws['S' + str(rNumDst)].value = qtr_src_ws['V' + str(rNumSrc)].value
                                                        q1_dst_ws['V' + str(rNumDst)].value = qtr_src_ws['Y' + str(rNumSrc)].value
                                                        q1_dst_ws['X' + str(rNumDst)].value = qtr_src_ws['AA' + str(rNumSrc)].value
                                                    elif srv == "_T":
                                                        if comm == "native" or comm == "broiler" or comm == "layer":
                                                            q1_dst_ws['AA' + str(rNumDst)].value = qtr_src_ws['AD' + str(rNumSrc)].value
                                                        if comm == "broiler" or comm == "layer":
                                                            q1_dst_ws['AC' + str(rNumDst)].value = qtr_src_ws['AF' + str(rNumSrc)].value
                                                    print(f"PSA-LPSD (EDRW): Copied to destination -> {province} - {comm} - {srv} at row {rNumSrc}")

                                            fpath = str(baseFolder) + '/Final/' + str(regName)
                                            if os.path.isdir(fpath) == False:
                                                os.mkdir(fpath)
                                            finalFile = str(baseFolder) + '/Final/' + str(regName) + '/' + str(commcode) + ' ' + str(province) + '_' + str(yr) + '.xlsx'
                                            print(f"PSA-LPSD (EDRW): Saving to file -> {finalFile}")
                                            dst.save(finalFile)
                                        else:
                                            print(f"File {srcFile}{fileExt} Not Found.")
                        else:
                            print(f"File {srcFile}{fileExt} Not Found.")
                else:
                    print("Region not found or has no provinces.")
            # Duck
            if commcode == '09':
                src_active = src["Backyard"] # Get Province Names from this worksheet
                # comm_arr = ["native","gamefowl","broiler","layer"]
                srv_arr = ["Backyard","Commercial","Total"]
                if selected_provinces:
                    for province in selected_provinces:
                        srcFile = str(commcode) + ' ' + str(province) + '_' + str(yr) # template files
                        fileExt = '.xlsx' # orig .xlsm
                        fpath = str(baseFolder) + '/Sources/' + str(regCode) + ' ' + str(regName) + '/' + str(regCode) + ' ' + str(province) + '/' + str(srcFile) + str(fileExt)
                        if os.path.isfile(fpath) == True:
                            for row in src_active.iter_rows(min_row=18, min_col=2, max_row=118, max_col=2):
                                for cell in row:
                                    if cell.value == province:
                                        #print(f"{province} {cell.row}")
                                        rNumSrc = cell.row

                                        #dst = load_workbook(filename=str(baseFolder) + '/Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt))
                                        dst = load_workbook(filename=fpath)
                                        #dst = xlrd.open_workbook('Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt))
                                        qtr_dst_ws = dst[qtr]
                                        currqtr = qtr[:-1] + str(int(qtr[-1])+1) # current quarter +1
                                        currqtr_dst_ws = dst[currqtr]
                                        #q1_dst_ws = dst.sheet_by_name(qtr)

                                        if os.path.isfile(fpath) == True:
                                            # for comm in comm_arr:
                                            for srv in srv_arr:
                                                if srv == "Backyard": # row number of destinations of copied values from SD
                                                    rNumDst = 22
                                                elif srv == "Commercial":
                                                    rNumDst = 28
                                                elif srv == "Total":
                                                    rNumDst = 32

                                                # sheetNameSrc = str(comm) + str(srv)
                                                qtr_src_ws = src[srv]
                                                print(f"PSA-LPSD (EDRW): Loading source -> {province} - {srv}")

                                                if srv != "Total":
                                                    #print(f"Copying Source B{rNumSrc} to E{rNumDst}")
                                                    qtr_dst_ws['H' + str(rNumDst)].value = qtr_src_ws['F' + str(rNumSrc)].value # Hatched live
                                                    qtr_dst_ws['J' + str(rNumDst)].value = qtr_src_ws['H' + str(rNumSrc)].value # Laying flock
                                                    qtr_dst_ws['K' + str(rNumDst)].value = qtr_src_ws['I' + str(rNumSrc)].value # MALE BREEDER
                                                    qtr_dst_ws['N' + str(rNumDst)].value = qtr_src_ws['L' + str(rNumSrc)].value # AVIAN INF
                                                    qtr_dst_ws['O' + str(rNumDst)].value = qtr_src_ws['M' + str(rNumSrc)].value # OTHER DISEASE
                                                    qtr_dst_ws['R' + str(rNumDst)].value = qtr_src_ws['P' + str(rNumSrc)].value # DRESSED ON FARM
                                                    qtr_dst_ws['S' + str(rNumDst)].value = qtr_src_ws['T' + str(rNumSrc)].value # Total E.I. (v Current Q)
                                                    qtr_dst_ws['T' + str(rNumDst)].value = qtr_src_ws['U' + str(rNumSrc)].value # Laying flock (v Current Q)
                                                    currqtr_dst_ws['E' + str(rNumDst)].value = qtr_src_ws['T' + str(rNumSrc)].value # Total E.I. (v Next Q) TO B.I. of next Q
                                                    currqtr_dst_ws['F' + str(rNumDst)].value = qtr_src_ws['U' + str(rNumSrc)].value # Laying flock (v Next Q) TO B.I. of next Q
                                                    qtr_dst_ws['W' + str(rNumDst)].value = qtr_src_ws['X' + str(rNumSrc)].value # SOLD LIVE FOR OTHER PURPOSE
                                                    qtr_dst_ws['Y' + str(rNumDst)].value = qtr_src_ws['Z' + str(rNumSrc)].value # AVG LOCAL LIVEWEIGHT
                                                elif srv == "Total":
                                                    qtr_dst_ws['AB' + str(rNumDst)].value = qtr_src_ws['AC' + str(rNumSrc)].value # INFLOW FROM OTHER PRV
                                                    qtr_dst_ws['AD' + str(rNumDst)].value = qtr_src_ws['AE' + str(rNumSrc)].value # SHIPPED-OUT TO OTHER PRV
                                                print(f"PSA-LPSD (EDRW): Copied to destination -> {province} - {srv} at row {rNumSrc}")
                                            fpath_reg = str(baseFolder) + '/Final/' + str(regCode) + ' ' + str(regName)
                                            if os.path.isdir(fpath_reg) == False:
                                                os.mkdir(fpath_reg)
                                            fpath_prv = str(baseFolder) + '/Final/' + str(regCode) + ' ' + str(regName) + '/' + str(regCode) + ' ' + str(province)
                                            if os.path.isdir(fpath_prv) == False:
                                                os.mkdir(fpath_prv)
                                            finalFile = fpath_prv + '/' + str(commcode) + ' ' + str(province) + '_' + str(yr) + '.xlsx'
                                            print(f"PSA-LPSD (EDRW): Saving to file -> {finalFile}")
                                            dst.save(finalFile)
                                        else:
                                            print(f"File {srcFile}{fileExt} Not Found.")
                        else:
                            print(f"File {srcFile}{fileExt} Not Found.")
                else:
                    print("Region not found or has no provinces.")
            # Duck Egg
            if commcode == '09a':
                src_active = src["Backyard"] # Get Province Names from this worksheet
                # comm_arr = ["native","gamefowl","broiler","layer"]
                srv_arr = ["Backyard","Commercial","Total"]
                if selected_provinces:
                    for province in selected_provinces:
                        srcFile = str(commcode) + ' ' + str(province) + '_' + str(yr) # template files
                        fileExt = '.xlsx' # orig .xlsm
                        fpath = str(baseFolder) + '/Sources/' + str(regCode) + ' ' + str(regName) + '/' + str(regCode) + ' ' + str(province) + '/' + str(srcFile) + str(fileExt)
                        if os.path.isfile(fpath) == True:
                            for row in src_active.iter_rows(min_row=18, min_col=2, max_row=118, max_col=2):
                                for cell in row:
                                    if cell.value == province:
                                        #print(f"{province} {cell.row}")
                                        rNumSrc = cell.row

                                        #dst = load_workbook(filename=str(baseFolder) + '/Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt))
                                        dst = load_workbook(filename=fpath)
                                        #dst = xlrd.open_workbook('Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt))
                                        qtr_dst_ws = dst[qtr]
                                        currqtr = qtr[:-1] + str(int(qtr[-1])+1) # current quarter +1
                                        currqtr_dst_ws = dst[currqtr]
                                        #q1_dst_ws = dst.sheet_by_name(qtr)

                                        if os.path.isfile(fpath) == True:
                                            # for comm in comm_arr:
                                            for srv in srv_arr:
                                                if srv == "Backyard": # row number of destinations of copied values from SD
                                                    rNumDst = 22
                                                elif srv == "Commercial":
                                                    rNumDst = 28
                                                elif srv == "Total":
                                                    rNumDst = 32

                                                # sheetNameSrc = str(comm) + str(srv)
                                                qtr_src_ws = src[srv]
                                                print(f"PSA-LPSD (EDRW): Loading source -> {province} - {srv}")

                                                if srv != "Total":
                                                    #print(f"Copying Source B{rNumSrc} to E{rNumDst}")
                                                    qtr_dst_ws['I' + str(rNumDst)].value = qtr_src_ws['G' + str(rNumSrc)].value # PIECES (EGG PROD)
                                                    qtr_dst_ws['J' + str(rNumDst)].value = qtr_src_ws['H' + str(rNumSrc)].value # CONVERSION FACTOR
                                                    qtr_dst_ws['L' + str(rNumDst)].value = qtr_src_ws['J' + str(rNumSrc)].value # ESTIMATED HATCHING EGGS
                                                elif srv == "Total":
                                                    qtr_dst_ws['P' + str(rNumDst)].value = qtr_src_ws['N' + str(rNumSrc)].value # SHIPPED-OUT TO OTHER PRV
                                                print(f"PSA-LPSD (EDRW): Copied to destination -> {province} - {srv} at row {rNumSrc}")
                                            fpath_reg = str(baseFolder) + '/Final/' + str(regCode) + ' ' + str(regName)
                                            if os.path.isdir(fpath_reg) == False:
                                                os.mkdir(fpath_reg)
                                            fpath_prv = str(baseFolder) + '/Final/' + str(regCode) + ' ' + str(regName) + '/' + str(regCode) + ' ' + str(province)
                                            if os.path.isdir(fpath_prv) == False:
                                                os.mkdir(fpath_prv)
                                            finalFile = fpath_prv + '/' + str(commcode) + ' ' + str(province) + '_' + str(yr) + '.xls'
                                            print(f"PSA-LPSD (EDRW): Saving to file -> {finalFile}")
                                            dst.save(finalFile)
                                        else:
                                            print(f"File {srcFile}{fileExt} Not Found.")
                        else:
                            print(f"File {srcFile}{fileExt} Not Found.")
                else:
                    print("Region not found or has no provinces.")
            # Chicken Egg
            if commcode == '08a':
                src_active = src["Native_B"] # Get Province Names from this worksheet
                # comm_arr = ["native","gamefowl","broiler","layer"]
                srv_arr = ["Native_B","Native_C","Broiler_C","Layer_B","Layer_C"]
                if selected_provinces:
                    for province in selected_provinces:
                        srcFile = str(commcode) + ' ' + str(province) + '_' + str(yr) # template files
                        fileExt = '.xlsx' # orig .xlsm
                        fpath = str(baseFolder) + '/Sources/' + str(regCode) + ' ' + str(regName) + '/' + str(regCode) + ' ' + str(province) + '/' + str(srcFile) + str(fileExt)
                        if os.path.isfile(fpath) == True:
                            for row in src_active.iter_rows(min_row=18, min_col=2, max_row=118, max_col=2):
                                for cell in row:
                                    if cell.value == province:
                                        #print(f"{province} {cell.row}")
                                        rNumSrc = cell.row

                                        #dst = load_workbook(filename=str(baseFolder) + '/Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt))
                                        dst = load_workbook(filename=fpath)
                                        #dst = xlrd.open_workbook('Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt))
                                        qtr_dst_ws = dst[qtr]
                                        currqtr = qtr[:-1] + str(int(qtr[-1])+1) # current quarter +1
                                        currqtr_dst_ws = dst[currqtr]
                                        #q1_dst_ws = dst.sheet_by_name(qtr)

                                        if os.path.isfile(fpath) == True:
                                            # for comm in comm_arr:
                                            for srv in srv_arr:
                                                if srv == "Native_B": # row number of destinations of copied values from SD
                                                    rNumDst = 22
                                                elif srv == "Native_C":
                                                    rNumDst = 28
                                                elif srv == "Broiler_C":
                                                    rNumDst = 38
                                                elif srv == "Layer_B":
                                                    rNumDst = 44
                                                elif srv == "Layer_C":
                                                    rNumDst = 50

                                                # sheetNameSrc = str(comm) + str(srv)
                                                qtr_src_ws = src[srv]
                                                print(f"PSA-LPSD (EDRW): Loading source -> {province} - {srv}")

                                                if srv == "Native_B" or srv == "Native_C":
                                                    #print(f"Copying Source B{rNumSrc} to E{rNumDst}")
                                                    qtr_dst_ws['J' + str(rNumDst)].value = qtr_src_ws['H' + str(rNumSrc)].value # PIECES (EGG PROD)
                                                    qtr_dst_ws['K' + str(rNumDst)].value = qtr_src_ws['I' + str(rNumSrc)].value # CONVERSION FACTOR
                                                    qtr_dst_ws['M' + str(rNumDst)].value = qtr_src_ws['K' + str(rNumSrc)].value # ESTIMATED HATCHING EGGS
                                                    qtr_dst_ws['Q' + str(rNumDst)].value = qtr_src_ws['O' + str(rNumSrc)].value # SHIPPED-OUT TO OTHER PRV
                                                elif srv == "Broiler_C" or srv == "Layer_C":
                                                    qtr_dst_ws['I' + str(rNumDst)].value = qtr_src_ws['G' + str(rNumSrc)].value # ELER
                                                    qtr_dst_ws['J' + str(rNumDst)].value = qtr_src_ws['H' + str(rNumSrc)].value # PIECES (EGG PROD)
                                                    qtr_dst_ws['K' + str(rNumDst)].value = qtr_src_ws['I' + str(rNumSrc)].value # CONVERSION FACTOR
                                                    qtr_dst_ws['M' + str(rNumDst)].value = qtr_src_ws['K' + str(rNumSrc)].value # ESTIMATED HATCHING EGGS
                                                    qtr_dst_ws['Q' + str(rNumDst)].value = qtr_src_ws['O' + str(rNumSrc)].value # SHIPPED-OUT TO OTHER PRV
                                                elif srv == "Layer_B":
                                                    qtr_dst_ws['I' + str(rNumDst)].value = qtr_src_ws['G' + str(rNumSrc)].value # ELER
                                                    qtr_dst_ws['J' + str(rNumDst)].value = qtr_src_ws['H' + str(rNumSrc)].value # PIECES (EGG PROD)
                                                    qtr_dst_ws['K' + str(rNumDst)].value = qtr_src_ws['I' + str(rNumSrc)].value # CONVERSION FACTOR
                                                    qtr_dst_ws['Q' + str(rNumDst)].value = qtr_src_ws['O' + str(rNumSrc)].value # SHIPPED-OUT TO OTHER PRV
                                                print(f"PSA-LPSD (EDRW): Copied to destination -> {province} - {srv} at row {rNumSrc}")
                                            fpath_reg = str(baseFolder) + '/Final/' + str(regCode) + ' ' + str(regName)
                                            if os.path.isdir(fpath_reg) == False:
                                                os.mkdir(fpath_reg)
                                            fpath_prv = str(baseFolder) + '/Final/' + str(regCode) + ' ' + str(regName) + '/' + str(regCode) + ' ' + str(province)
                                            if os.path.isdir(fpath_prv) == False:
                                                os.mkdir(fpath_prv)
                                            finalFile = fpath_prv + '/' + str(commcode) + ' ' + str(province) + '_' + str(yr) + '.xls'
                                            print(f"PSA-LPSD (EDRW): Saving to file -> {finalFile}")
                                            dst.save(finalFile)
                                        else:
                                            print(f"File {srcFile}{fileExt} Not Found.")
                        else:
                            print(f"File {srcFile}{fileExt} Not Found.")
                else:
                    print("Region not found or has no provinces.")
            # else:
            #     print(f"Commodity code {commcode} not found.")