import csv
import numpy as np
import getpass
import matplotlib.pyplot as plt
import os


Strip_MW_list = [0]


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
        FileForPlot = ParamDic['FileForPlot']
        for j in range(Strip_Amount+1):
            Strip_MW_list.append(int(ParamDic['Strip_MW_'  + str(j+1)]))


def determine_scope(xmass):
    for i in range(Strip_Amount+2):
        if xmass < Strip_MW_list[i]:
            xx = i-1
            return xx
            break        


with open('C:/Users/' + getpass.getuser() + '/Desktop/' + FileForPlot + '.csv') as f:
    reader = csv.reader(f)
    for csvline in reader:
        if reader.line_num == 1:
            continue
        for i in range(Replication_Amount):
            num_list1 = []  
            num_list2 = []
            num_list_sum = []
            numlistone = np.ones(Strip_Amount)
            for j in range(Strip_Amount):
                num_list1.append(int(csvline[3 + Strip_Amount*2*i + 2*j]))
                num_list2.append(int(csvline[3 + Strip_Amount*2*i + 2*j + 1]))
            for g in range(Strip_Amount):
                if num_list1[g] == 1:
                    if num_list2[g] == 0:
                        num_list_sum.append(1)
                    else:
                        num_list_sum.append(0)
                else:
                    num_list_sum.append(0)

            ind = np.arange(Replication_Amount)
            ind1 = np.arange(Replication_Amount+1)
            ind2 = []
            ind3 = []
            for p in range(Replication_Amount+1):
                ind2.append(ind1[p]-0.5)
            for q in range(Replication_Amount):
                ind3.append(ind[q]+1)
            width = 1
            
            sssss = determine_scope(int(csvline[1]))
            ddddd = determine_scope(int(csvline[2]))
            p1 = plt.barh(ind3, num_list_sum, width, fc = 'darkorange',edgecolor = 'darkorange')
            p3 = plt.barh(sssss, 1, 0.1,fc = 'deepskyblue',edgecolor = 'deepskyblue')
            p4 = plt.barh(ddddd, 1, 0.1,fc = 'yellowgreen',edgecolor = 'yellowgreen')

            frame = plt.gca()
            frame.axes.get_xaxis().set_visible(False)
            
            plt.title(csvline[0] + str(i+1))
            strStrip_MW_list = [str(int(Strip_MW_list[i]/1000)) + 'kD' for i in range(Replication_Amount+2)]
            plt.yticks(ind2,strStrip_MW_list[0:-1])
            plt.legend((p1[0],p3[0],p4[0]),('Detected Crosslinked MW','Theoretical Prey MW','Theoretical Crosslinked MW'),fontsize = 'x-small')
            bbbb = 'C:/Users/' + getpass.getuser() + '/Desktop/Figures/' + str(csvline[0])
            if not os.path.exists(bbbb):
                os.makedirs(bbbb)
            plt.savefig(bbbb +'/' + str(csvline[0]) + str(i+1) + '.png', dpi=1000)
            plt.close()
f.close()