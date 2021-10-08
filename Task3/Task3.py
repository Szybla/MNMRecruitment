import subprocess

def loadFile(filename):
    f = open(filename, 'r')
    file = f.readlines()
    f.close()
    return file

file = loadFile('tumor_vs_normal.strelka.somatic.snvs.vcf')
#Discard all the variants which are failed to pass the filtering
def filtering(file):
    passList = []
    for rec in file:
        if rec.startswith('#'):
            passList.append(rec)
            continue
        if rec.split()[6] == 'PASS':
            passList.append(rec)
    f = open('tumor_vs_normal.strelka.somatic.snvs.filter.vcf', 'w')
    f.write(''.join(passList))
    f.close()
filtering(file)

#Annotate filtered variants with the SNPeff using hg19 database
def annotate(file):
    dump = f"java -Xmx8G -jar snpEff/snpEff.jar hg19 {file} > {file.split('.vcf')[0]}_snpEff.vcf"
    try:
        subprocess.call(dump, shell=True)
    except:
        print(f"Error while annotating {file}")
        return 0
annotate('tumor_vs_normal.strelka.somatic.snvs.filter.vcf')

#Count the variants that change the protein encoded by the gene in which the variant is located. The list of possible consequences of changes
def countvariants():
    SNPeffFile = loadFile('tumor_vs_normal.strelka.somatic.snvs.filter_snpEff.vcf')
    h = []
    for i in SNPeffFile:
        if i.startswith('#'):
            continue
        else:
            h.append(i)
    SNPeffFile = h
    d = {}
    for i in range(len(h)):
        h[i] = h[i].split()[7].split(';')
        if h[i][13].split('|')[1] not in d:
            d[h[i][13].split('|')[1]] = 1
        else:
            d[h[i][13].split('|')[1]] = d[h[i][13].split('|')[1]] + 1
    print(d)
countvariants()

#List a genes which are affected with the predicted Loss of function effect.
def listAgenes(file):
    dump = f"java -Xmx8G -jar snpEff/snpEff.jar -v -lof hg19 {file} > {file.split('.vcf')[0]}_snpEff_lof.vcf"
    try:
        subprocess.call(dump, shell=True)
    except:
        print(f"Error while annotating {file}")
        return 0
listAgenes('tumor_vs_normal.strelka.somatic.snvs.filter.vcf')
def listingGene():
    lgFile = loadFile('tumor_vs_normal.strelka.somatic.snvs.filter_snpEff_lof.vcf')
    h = []
    for i in lgFile:
        if i.startswith('#'):
            continue
        else:
            h.append(i)
    SNPeffFile = h
    h = set()
    for i in SNPeffFile:
        h.add(i.split()[7].split(';')[13].split('|')[4])
    h.remove('')
    print(h)
listingGene()
#(Additional, not obligatory) Make a short EDA(explaratory data analysis) of the assigned effect predictions