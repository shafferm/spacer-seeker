from Bio import SeqIO
from Bio.Alphabet.IUPAC import ambiguous_dna

from numpy import random

from collections import namedtuple

import argparse
import time
import bisect

SequenInfo = namedtuple('SequenInfo', ['read_len', 'ins_len', 'name', 'reads'])
SeqInfo = namedtuple('SeqInfo', ['seqs', 'weights'])

def get_list(file_loc):
    f = open(file_loc)
    l = list()
    for line in f:
        l.append(line.strip())
    return l

#shamelessly stolen (and then adapted) from http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
class WeightedRandomGenerator(object):
    def __init__(self, weights):
        self.seqs = weights.seqs
        self.totals = []
        running_total = 0

        for w in weights.weights:
            running_total += w
            self.totals.append(running_total)

    def next(self):
        rnd = random.random() * self.totals[-1]
        return self.seqs[bisect.bisect_right(self.totals, rnd)]

    def __call__(self):
        return self.next()


def gen_reads(sequen_info, seqs):
    reads = 0
    qual = "".join(sequen_info.read_len * ['~'])
    f = open(sequen_info.name, 'w')
    while reads < sequen_info.reads:
        seq = seqs.next()
        seq = make_read(sequen_info, seq) #gets insert, not two reads
       	f.write('@'+seq.description+'\n'+str(seq.seq[:sequen_info.read_len])+'\n+'+seq.description+'\n'+qual+'\n')
        f.write('@'+seq.description+'\n'+str(seq.seq[-sequen_info.read_len:])+'\n+'+seq.description+'\n'+qual)
        reads+=1
        print str(reads) + " out of " + str(sequen_info.reads) + " generated"
        if reads < sequen_info.reads:
            f.write('\n')

def make_read(sequen_info, seq):
    start1 = random.randint(0, len(seq))
    start2 = start1 + int(random.normal(sequen_info.ins_len, 5))
    if start2 > len(seq):
        start2 = start2-len(seq)
        return seq[start1:]+seq[:start2]
    else:
        return seq[start1:start2]

def process_seqs(directory, abund_file):
    weights = list()
    seqs = list()
    i = 0
    f = open(abund_file)
    for line in f:
        #each line contains two segments seperated by a \t, line[0] is the seq file name and line[1]
        #is the relative abundance
        line = line.strip().split('\t')
        
        seq = SeqIO.read(directory + line[0], "fasta", ambiguous_dna)
        seqs.append(seq)
        weight = float(line[1]) * float(len(seq))
        weights.append(weight)
        i+=1
    total = sum(weights)
    for i in xrange(0,len(weights)):
        weights[i] = weights[i]/total
    return SeqInfo(seqs, weights)

def main():
    #take in arguements
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_loc", help="location of output file + prefix, default = ~/test", default="/home/shafferm/course_proj/bacteria/reads.fastq")
    parser.add_argument("-i", "--input_file", help="file containing list of genomes and relative abundances for each genome", default="/home/shafferm/course_proj/bacteria/fastas.txt")
    parser.add_argument("-d", "--input_dir", help="directory of input fasta or multifasta genomes", default="/home/shafferm/course_proj/bacteria/genomes/")
    parser.add_argument("-I", "--ins_len", type=int, help="length of space between adaptors for sequencing", default=500)
    parser.add_argument("-r", "--read_len", type=int, help="length of sequencing read from either side of insert length", default=100)
    parser.add_argument("-R", "--reads_to_gen", type=int, help="number of reads to generate per enzyme", default=230000000)
    args = parser.parse_args()
    
    sequen_info = SequenInfo(args.read_len, args.ins_len, args.output_loc, args.reads_to_gen) 

    seqs = process_seqs(args.input_dir, args.input_file)
    seqs = WeightedRandomGenerator(seqs)
    print "sequences processed: weights made and sequeces stored"

    gen_reads(sequen_info, seqs)

    return 0


if __name__=="__main__":
    main()
