import os
import csv
import getpass


Strip_MW_list = []


f_list = os.listdir('.')
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
        for j in range(Strip_Amount+1):
            Strip_MW_list.append(int(ParamDic['Strip_MW_'  + str(j+1)]))


def if_meet_conditions(protein_mass, crosslinked_mass, num_of_band):
    if protein_mass <= Strip_MW_list[num_of_band]:
        if crosslinked_mass <= Strip_MW_list[num_of_band]:
            return True
        else:
            return False
    else:
        return False


if os.path.isfile('C:/Users/' + getpass.getuser() + '/Desktop/' + ResultName3 + '.csv'):
    os.remove('C:/Users/' + getpass.getuser() + '/Desktop/' + ResultName3 + '.csv')

    
FinalResultFile3Name = 'C:/Users/' + getpass.getuser() + '/Desktop/' + ResultName3 + '.csv'
FinalResult3 = open(FinalResultFile3Name, 'w')
FinalResult3.write('Protein,Protein MW,Theoretical Crosslinked MW,')
for i in range(Replication_Amount):
    for j in range(int(Strip_Amount)):
        FinalResult3.write(str(i+1) + '+UV-' + str(j+1) + ',')
        FinalResult3.write(str(i+1) + '-UV-' + str(j+1) + ',')
FinalResult3.write('\n')


with open('C:/Users/' + getpass.getuser() + '/Desktop/' + ResultName2 + '.csv') as f:
    reader = csv.reader(f)
    for csvline in reader:
        xxx = 0
        yyy = 0
        if reader.line_num == 1:
            continue
        for i in range(Replication_Amount):
            for j in range(Strip_Amount):
                if int(csvline[3 + Strip_Amount*2*i + 2*j]) == 1:
                    if int(csvline[3 + Strip_Amount*2*i + 2*j + 1]) == 0:
                        if if_meet_conditions(int(csvline[1]), int(csvline[2]), (j+1)):
                            xxx = 1
            if xxx == 1:
                yyy = yyy + 1
            xxx = 0
        if yyy >= Replication_Met_Rules:
            FinalResult3.write(csvline[0] + ',' + csvline[1] + ',' + csvline[2] + ',')
            for a in range(Replication_Amount):
                for b in range(Strip_Amount):
                    FinalResult3.write(csvline[3 + Strip_Amount*2*a + 2*b] + ',')
                    FinalResult3.write(csvline[3 + Strip_Amount*2*a + 2*b + 1] + ',')
            FinalResult3.write('\n') 


FinalResult3.close()