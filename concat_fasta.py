#combine .fasta's

import argparse
import os

def merge_fasta(fastas, output):
    spacers = ""
    for name in fastas:
        name = open(name)
        spacers+=name.read()
    f = open(output, 'w')
    f.write(spacers)

def get_fas(folder):
    """Takes a directory and returns a list of files in that directory which end with the .fa file
    extension
    """
    files = os.listdir(folder)
    fas = list()
    for file in files:
        if file.endswith(".fa"):
            fas.append(folder+file)
    return fas

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", help="location of CRASS output")
    parser.add_argument("-o", "--output_file", help="name for merged spacer file")
    args = parser.parse_args()
    
    fas = get_fas(args.input_dir)
    merge_fasta(fas, args.output_file)
    
if __name__=="__main__":
    main()