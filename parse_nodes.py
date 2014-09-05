from Bio import SeqIO
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--contigs", help="location of contigs produced by IDBA-UD", default= "contig.fa")
    parser.add_argument("-s", "--spacers", help="location of spacers produced by CRASS", default="spcrs.fna")
    parser.add_argument("-o", "--out", help="prefix for output file", default="def")
    args = parser.parse_args()
    
    output = open(args.out+"_nodes_c.txt", "w")
    output.write("name" + '\t' + "short_name" + '\t' + "type" + '\t' + "length" + '\t' + "read_count" + '\n')
    
    file = open(args.contigs)    
    for record in SeqIO.parse(file, "fasta"):
        name = record.description
        ident = name.split(" ")
        short_name = ident[0]
        length = len(record.seq)
        read_count = ident[2].split("_")[2]
        output.write(">" + name + '\t' + short_name + '\t' + "contig" +'\t' + str(length) + '\t' + read_count + '\n')
    file.close()
    
    file = open(args.spacers)
    groups = dict()
    for record in SeqIO.parse(file, "fasta"):
        name = record.description
        ident = name.split("_")
        short_name = ident[0]
        length = len(record.seq)
        read_count = ident[2]
        group = ident[0].split("S")[0].replace("G","")
        print group
        output.write(">" + name + '\t' + short_name + '\t' + "spacer" + '\t' + str(length) + '\t' + read_count + '\n')
        if group in groups:
            groups[group].append(name)
        else:
            groups[group] = [name]
    
    for group in groups:
        output.write("Group " + group + '\t' + group + '\t' + "CRISPR" + '\t' + "" + '\t' + "" + '\n')
    
if __name__=="__main__":
    main()