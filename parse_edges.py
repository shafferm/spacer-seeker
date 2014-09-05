import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--results", help="location of results file produced by SS-e", default= "_results_c.txt")
    parser.add_argument("-o", "--out", help="prefix for output file", default="def")
    args = parser.parse_args()
    
    f = open(args.results)
    groups = dict()
    for line in f:
        name = line.split('\t')[0]
        group = name.split("S")[0].replace(">G","") 
        if group in groups:
            if name not in groups[group]:
                groups[group].append(name)
        else:
            groups[group] = [name]
    
    output2 = open(args.out+"_spacer_edges_c.txt", "w")
    for group in groups:
        grouplist = groups[group]
        for i in xrange(0, len(grouplist)):
            header1 = grouplist[i]
            output2.write("Group "+group + '\t' + "CRISPR" + '\t' + header1 + '\t'+ "1" +'\n')

if __name__=="__main__":
    main()