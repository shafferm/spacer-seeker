from Bio import SeqIO

import argparse
import random

def mutate_seq(sequence, error_rate):
    new_seq = ""
    for nt in sequence:
        if random.random() < error_rate:
            if nt == 'C' or nt == 'c':
                index = random.randint(0,2)
                if index == 0:
                    new_seq+='A'
                if index == 1:
                    new_seq+='T'
                else:
                    new_seq+='G'    
            if nt == 'T' or nt == 't':
                index = random.randint(0,2)
                if index == 0:
                    new_seq+='A'
                if index == 1:
                    new_seq+='C'
                else:
                    new_seq+='G'
            if nt == 'A' or nt == 'a':
                index = random.randint(0,2)
                if index == 0:
                    new_seq+='T'
                if index == 1:
                    new_seq+='C'
                else:
                    new_seq+='G'
            else:
                index = random.randint(0,2)
                if index == 0:
                    new_seq+='T'
                if index == 1:
                    new_seq+='C'
                else:
                    new_seq+='A'
        else:
            new_seq+=nt
    return new_seq

def main():
    #take in arguements
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input fasta file")
    parser.add_argument("-r", "--error_rate", help="decimal error rate (0-1)", type=float, default=.01)
    args = parser.parse_args()
    
    seq_records = SeqIO.parse(args.input, "fasta")
    new_records = list()
    
    for record in seq_records:
        old_seq = record.seq
        record.seq = mutate_seq(record.seq, args.error_rate)
        if old_seq == record.seq:
            print "got issues"
        else:
            new_records.append(record)
        
    output = open("".join(args.input.split('.')[:-1])+"_"+str(args.error_rate)+".fasta", "w")
    for record in new_records:
        output.write(">"+record.description+'\n'+record.seq+'\n')
    output.close()

if __name__=="__main__":
    main()