import subprocess

def loadFile(filename):
    f = open(filename, 'r')
    file = f.readlines()
    f.close()
    return file

SNVfile = loadFile('T1_vs_N1_head.strelka.somatic.snvs.norm.vcf')
INDELfile = loadFile('T1_vs_N1_head.strelka.somatic.indels.norm.vcf')

#Discard all the variants which are failed to pass the filtering
def filtering(file, outputname):
    passList = []
    for rec in file:
        if rec.startswith('#'):
            passList.append(rec)
            continue
        if rec.split()[6] == 'PASS':
            passList.append(rec)
    f = open(outputname, 'w')
    f.write(''.join(passList))
    f.close()
#filtering(SNVfile, 'T1_vs_N1_head.strelka.somatic.snvs.norm.filter.vcf')
#filtering(INDELfile, 'T1_vs_N1_head.strelka.somatic.indels.norm.filter.vcf')

SNVfile = loadFile('T1_vs_N1_head.strelka.somatic.snvs.norm.filter.vcf')
INDELfile = loadFile('T1_vs_N1_head.strelka.somatic.indels.norm.filter.vcf')

def SNVvariant():
    f = open('output_SNV.vcf', 'w')
    f.close()
    f = open('output_SNV.vcf', 'a')
    for i in SNVfile:
        if i.split()[0].startswith('##'):
            f.write(i)
            continue
        if i.split()[0].startswith('#CHROM'):
            f.write('\t'.join(i.split() + ['NORMAL_VAF', 'TUMOR_VAF', '\n']))
            continue
        j = i.split()
        for n in range(2):
            ref_letter = i.split()[3]
            alt_letter = i.split()[4]
            allCount = int(i.split()[9 + n].split(':')[0])
            if ref_letter == 'A':
                refCount = int(i.split()[9 + n].split(':')[4].split(',')[0])
            elif ref_letter == 'C':
                refCount = int(i.split()[9 + n].split(':')[5].split(',')[0])
            elif ref_letter == 'G':
                refCount = int(i.split()[9 + n].split(':')[6].split(',')[0])
            elif ref_letter == 'T':
                refCount = int(i.split()[9 + n].split(':')[7].split(',')[0])

            if alt_letter == 'A':
                altCount = int(i.split()[9 + n].split(':')[4].split(',')[0])
            elif alt_letter == 'C':
                altCount = int(i.split()[9 + n].split(':')[5].split(',')[0])
            elif alt_letter == 'G':
                altCount = int(i.split()[9 + n].split(':')[6].split(',')[0])
            elif alt_letter == 'T':
                altCount = int(i.split()[9 + n].split(':')[7].split(',')[0])
            j.append(str(allCount / (altCount + refCount)))
        f.write('\t'.join(j + ['\n']))
    f.close()

def INDELvariant():
    f = open('output_INDEL.vcf', 'w')
    f.close()
    f = open('output_INDEL.vcf', 'a')
    for i in INDELfile:
        if i.split()[0].startswith('##'):
            f.write(i)
            continue
        if i.split()[0].startswith('#CHROM'):
            f.write('\t'.join(i.split() + ['NORMAL_VAF', 'TUMOR_VAF', '\n']))
            continue
        j = i.split()
        for n in range(2):
            refCount = int(i.split()[9 + n].split(':')[2].split(',')[0])
            altCount = int(i.split()[9 + n].split(':')[3].split(',')[0])
            j.append(str(altCount / (altCount + refCount)))
        f.write('\t'.join(j + ['\n']))
    f.close()
SNVvariant()
INDELvariant()