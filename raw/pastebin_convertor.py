__author__ = 'RdX'

import sys

HELP_MSG = """
`pastebin_convertor` is silly tool useful in life saving conditions.
The python scripts available on `pastebin.com`  leaves fucking 4 places at start of each line.
This prevents direct execution of script.
So this script will rip those 4 spaces and will give u back same script 
as `ready to run`
"""

def stripAndCopy(input_file, output_file, strip_count):
    lines = []
    #read input file
    f = open(input_file, 'r')
    data = f.readlines()
    for line in data:
        line = line[int(strip_count):]
        lines.append(line)
    f.close()
    #write output file
    f = open(output_file, 'w')
    f.writelines(lines)
    f.close()

def main():
    args = sys.argv
    if  len(args) <= 1 or len(args) > 4:
        print 'Give somethin like `pastebin_convertor <inputfile> <outputfile> [<strip_count>]`'
    if len(args) == 2:
        if args[1].lower() == 'help':
            print HELP_MSG
        else:
            print 'Takein default strip count 4 spaces...'
            output_file = '_'.join(['copy', args[1]])
            print 'Taking output file as %s ...'  %(output_file)
            stripAndCopy(args[1], output_file, 4)
    if len(args) == 3:
        print 'Takein default strip count 4 spaces...'
        stripAndCopy(args[1], args[2], 4)
    if len(args) == 4:
        stripAndCopy(args[1], args[2], args[3])

if __name__ == "__main__":
    main()
