from matplotlib import pyplot
import math

def loadFile(filename):
    f = open(filename, 'r')
    file = f.readlines()
    f.close()
    return file

file = loadFile('tumor_vs_normal.manta.somatic.vcf')

#Count the total number of variants represented in the form of breakends.
def totalnumber(file):
    n=0
    for i in file:
       if i.startswith('#'):
           continue
       else:
           n = n + 1
    print(f"total number of variants represented in the form of breakends: {n}")

#Make a boxplots of the deletion length per each chromosome.
def boxplotmaking(file):
    delList = []
    for i in file:
        if 'SVTYPE=DEL' in i:
            delList.append(i.split())
    d = {}
    for rec in delList:
        if rec[0] not in d:
            d[rec[0]] = []
        if rec[4] == '<DEL>': nh = 0
        else: nh = len(rec[4])
        n = len(rec[3]) - nh
        d[rec[0]].append(n)
    data = []
    names = []
    for i in d:
        data.append(d[i])
        names.append(i)
    fig = pyplot.figure(figsize = (10,7))
    pyplot.boxplot(data, labels=names)
    pyplot.show()
boxplotmaking(file)

#Count how many variants failed to pass the filtering. Make a piechart of most frequent reasons to fail.
def piechartmaking(file):
    failList = []
    d = {}
    for rec in file:
        if rec.startswith('#'): continue
        if rec.split()[6] != 'PASS':
            failList.append(rec.split())
            if rec.split()[6] not in d:
                d[rec.split()[6]] = 1
            else:
                d[rec.split()[6]] = d[rec.split()[6]]+1
    data = []
    names = []
    for i in d:
        data.append(d[i])
        names.append(i)
    fig = pyplot.figure(figsize = (10,7))
    pyplot.pie(data, labels=names)
    pyplot.show()
    print(f"variants failed to pass the filtering: {sum(data)}")
piechartmaking(file)

#Find the variant with the widest confidence interval around POS;
def widestCIPOS(file):
    ciList = []
    ci = []
    for rec in file:
        if rec.startswith('#'): continue
        if 'CIPOS' in rec.split()[7]:
            ciList.append(rec.split())
            ci.append(rec.split()[7].split(';'))
    for i in range(len(ci)):
        for j in ci[i]:
            if j.startswith("CIPOS="):
                ci[i] = j
                break
    for i in range(len(ci)):
        l = ci[i].split('=')[1].split(',')
        ci[i] = math.fabs(int(l[0]) - int(l[1]))
    print(f"value: {max(ci)} \nvariant: {'  '.join(ciList[ci.index(max(ci))])}")
widestCIPOS(file)

#What type of stractural variant represented by ID MantaBND:28842:0:1:0:0:0:0
for rec in file:
    if rec.startswith('#'): continue
    if 'MantaBND:28842:0:1:0:0:0:0' in rec.split():
        for i in rec.split()[7].split(';'):
            if i.startswith('SVTYPE'):
                print(f"stractural variant: {i}")

