import sys
initDataFile = sys.argv[1]

readHeader = True  # start reading init data header
readFooter = False
initHeader = []
initFooter = []

# Read in header (atom and bond types) and footer (coeffs, bonds, dihedrals)

with open(initDataFile,"r") as f:
        for line in f:
                # print(line)
                if line.find('xhi') > 0:
                        # Done reading header
                        readHeader = False
                if line.startswith('Masses'):
                        # start reading footer
                        readFooter = True
                if readHeader:
                        initHeader.append(line)
                if readFooter:
                        initFooter.append(line)

with open(initDataFile+'START',"w") as f:
        for line in initHeader:
                f.write(line)

with open(initDataFile+'END',"w") as f:
        for line in initFooter:
                f.write(line)
