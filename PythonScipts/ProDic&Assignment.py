import os
import csv
import numpy
import getpass


UV_list = []
NOUV_list = []
final_list = []
f_list = os.listdir('.')
file_num = 0


for i in f_list:
    if os.path.splitext(i)[1] == '.param':
        ParamDic = {}
        with open(i) as f:
            reader = csv.reader(f)
            for item in reader:
                ParamDic[item[0]] = item[1]
        
        Replication_Amount = int(ParamDic['Replication_Amount'])
        Strip_Amount = int(ParamDic['Strip_Amount'])
        Replication_Met_Rules = int(ParamDic['Replication_Met_Rules'])
        FTO_MW = int(ParamDic['FTO_MW'])
        Rownum_Protein = int(ParamDic['Rownum_Protein'])
        Rownum_Protein_MW = int(ParamDic['Rownum_Protein_MW'])
        Rownum_Spectral_Count = int(ParamDic['Rownum_Spectral_Count'])
        TrueOrFalse = int(ParamDic['TrueOrFalse'])
        ResultName1 = ParamDic['ResultName1']
        ResultName2 = ParamDic['ResultName2']
        ResultName3 = ParamDic['ResultName3']
        FileForPlot = ParamDic['FileForPlot']


for i in f_list:
    if os.path.splitext(i)[1] == '.csv':
        file_num = file_num + 1
NumInEachCopy = int(file_num/Replication_Amount)
xfile_num = 0

       
for i in f_list:
    if os.path.splitext(i)[1] == '.csv':
        xfile_num = xfile_num + 1
        if xfile_num-NumInEachCopy*int(xfile_num/NumInEachCopy) != 0:
            if xfile_num-NumInEachCopy*int(xfile_num/NumInEachCopy) <= int(NumInEachCopy/2):
                if os.path.splitext(i)[1] == '.csv':
                    UV_list.append(i)
        if xfile_num-NumInEachCopy*int(xfile_num/NumInEachCopy)== 0:
            if os.path.splitext(i)[1] == '.csv':
                NOUV_list.append(i)            
        if xfile_num-NumInEachCopy*int(xfile_num/NumInEachCopy)>int(NumInEachCopy/2):
            if os.path.splitext(i)[1] == '.csv':
                NOUV_list.append(i)               
for i in range(int(file_num/2)):
    final_list.append(UV_list[i])
    final_list.append(NOUV_list[i])


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


def is_TrueOrFalse(s):
    if int(s) >= TrueOrFalse:
        return 1
    else:
        return 0


if os.path.isfile('C:/Users/' + getpass.getuser() + '/Desktop/' + ResultName1 + '.csv'):
    os.remove('C:/Users/' + getpass.getuser() + '/Desktop/' + ResultName1 + '.csv')
if os.path.isfile('C:/Users/' + getpass.getuser() + '/Desktop/' + ResultName2 + '.csv'):
    os.remove('C:/Users/' + getpass.getuser() + '/Desktop/' + ResultName2 + '.csv')


ResultFileName = 'C:/Users/' + getpass.getuser() + '/Desktop/' + ResultName1 + '.csv'
ResultFile = open(ResultFileName, 'w')
ResultFile.write('Protein,Protein MW,Theoretical Crosslinked MW,')
for i in range(Replication_Amount):
    for j in range(int(NumInEachCopy/2)):
        ResultFile.write(str(i+1) + '+UV-' + str(j+1) + ',')
        ResultFile.write(str(i+1) + '-UV-' + str(j+1) + ',')
ResultFile.write('\n')


ResultFile2Name = 'C:/Users/' + getpass.getuser() + '/Desktop/' + ResultName2 + '.csv'
ResultFile2 = open(ResultFile2Name, 'w')
ResultFile2.write('Protein,Protein MW,Theoretical Crosslinked MW,')
for i in range(Replication_Amount):
    for j in range(int(NumInEachCopy/2)):
        ResultFile2.write(str(i+1) + '+UV-' + str(j+1) + ',')
        ResultFile2.write(str(i+1) + '-UV-' + str(j+1) + ',')
ResultFile2.write('\n')


ProteinDic = {}
ProteinDic2 = {}
for file_name in final_list:
    with open(file_name) as f:
        reader = csv.reader(f)
        column = [row[Rownum_Protein-1] for row in reader]
        for i in range(len(column)):
            ProteinDic[column[i]] = numpy.zeros(file_num,int)
            ProteinDic2[column[i]] = 0


count = -1
for filename in final_list:
    count = count + 1
    with open(filename) as f:
        reader = csv.reader(f)
        proteinrows = [row[Rownum_Protein-1] for row in reader]
    with open(filename) as f:
        reader = csv.reader(f)                
        valuerows = [row[Rownum_Spectral_Count-1] for row in reader]
    with open(filename) as f:
        reader = csv.reader(f)
        Massrows  = [row[Rownum_Protein_MW-1] for row in reader]               
    for i in range(len(proteinrows)):
        if valuerows[i]:
            if is_number(valuerows[i]):
                ProteinDic[proteinrows[i]][count] = valuerows[i]
            else:
                ProteinDic[proteinrows[i]][count] = 0
        else:
            ProteinDic[proteinrows[i]][count] = 0        
        if Massrows[i]:
            if is_number(Massrows[i]):
                ProteinDic2[proteinrows[i]] = Massrows[i]
            else:
                ProteinDic2[proteinrows[i]] = 0


for protein in ProteinDic.keys():
    qwert = 0
    for i in range(file_num):
        if ProteinDic[protein][i] != 0:
            qwert = 1
    if qwert == 1:
        ResultFile.write(protein + ',' + str(ProteinDic2[protein]) + ',' + str(int(ProteinDic2[protein]) + FTO_MW) + ',')
        for i in range(file_num):
            ResultFile.write(str(ProteinDic[protein][i]) + ',')
        ResultFile.write('\n')
ResultFile.close()


for protein in ProteinDic.keys():
    qwerty = 0
    for i in range(file_num):
        if ProteinDic[protein][i] != 0:
            qwerty = 1
    if qwerty == 1:
        ResultFile2.write(protein + ',' + str(ProteinDic2[protein]) + ',' + str(int(ProteinDic2[protein]) + FTO_MW) + ',')
        for i in range(file_num):
            ResultFile2.write(str(is_TrueOrFalse(ProteinDic[protein][i])) + ',')
        ResultFile2.write('\n')
ResultFile2.close()
