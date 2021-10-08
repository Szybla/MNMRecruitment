import glob
import subprocess

#Extracting reads corresponded to chr1
def extract(file):
    if file+'.bai' not in glob.glob('*'):
        dump = f"samtools index {file}"
        try:
            subprocess.call(dump, shell=True)
        except:
            print(f"Error while create index for {file}")
            return 0
    dump = f"samtools view -h {file} 1 > {file.split('.bam')[0]}.chr1.sam"
    try:
        subprocess.call(dump, shell=True)
    except:
        print(f"Error while extracting for specific region")
        return 0
    dump = f"samtools view -bS {file.split('.bam')[0]}.chr1.sam > {file.split('.bam')[0]}.chr1.bam"
    try:
        subprocess.call(dump, shell=True)
    except:
        print(f"Error while converting sam to bam")
        return 0

def bam2fastq(file):
    dump = f"samtools bam2fq {file} > {file.split('.bam')[0]}.fastq"
    try:
        subprocess.call(dump, shell=True)
    except:
        print(f"Error while converting bam to fastq")
        return 0

#Realign to chr1
def align(file, ref):
    if 'index.'+ref not in glob.glob('*'):
        dump = f"bowtie2-build {ref} index.{ref}"  # budowanie indeksów
        try:
            subprocess.call(dump, shell=True)
        except:
            print(f"Error while making index")
            return 0
    dump = f"bowtie2 -x index.{ref} {file} -S {file.split('.fastq')[0]}.sam"
    try:
        subprocess.call(dump, shell=True)
    except:
        return 0

extract('miniMNM00065.bam')
bam2fastq('miniMNM00065.chr1.bam')
align('miniMNM00065.chr1.fastq', 'chr1.fa.gz')