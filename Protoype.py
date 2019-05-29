def Open_file():
    """Function for opening PDB file""" 
    global loaded_file 
    PDB_File = input("Enter a valid PDB File: ")
    print("The PDB file", PDB_File, "has been successfully loaded")
    loaded_file = open(PDB_File, "r")
    return PDB_File

def Information():
    titlelist = []
    for line in loaded_file:
        if line.startswith ('HEADER'):
            lineList = line.split()
            Header = lineList[4]    
        if line.startswith('TITLE'):
            titlelist.append(line[9:-4])
    print("PDB File: %s " %Header)
    Title = titlelist[0] + titlelist[1] 
    print("Title:", Title)

    chains = []
    loaded_file.seek(0)
    for line in loaded_file:    
        if line.startswith('SEQRES'):
            if line[11] not in chains:
                chains.append(line[11])
    print("CHAINS:", chains[0], "and", chains[1])

    for chain in chains:
        Amino_list = []
        Helix = 0
        Sheet = 0
        loaded_file.seek(0)
        for line in loaded_file:
            if line.startswith('HELIX'):
                if chain == line[19]:
                    Helix += 1
            if line.startswith("SHEET"):
                if chain == line[32]:
                    Sheet += 1
            if line.startswith('SEQRES'):
                    Amino_dict = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLY':'G','GLN':'Q','GLU':'E','HIS':'H',\
                  'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
                    lineList = line.split()
                    Amino_seq = list(lineList[4:])
                    Dict_amino = {}
                    sequences = ""
                    for key in Amino_seq:
                        Dict_amino[key] = Amino_dict[key]
                        sequences += Dict_amino.get(key)
                    if chain == line[11]:
                        Amino_list.append(sequences)                       
        Amino_list = "".join(Amino_list)
        print("- Chain: %s " %chain)
        print("Number of amino acids %d " %len(Amino_list))
        print("Number of helix: ", Helix)
        print("Number of Sheet: ", Sheet) 
        print("Sequence:",'\n'.join([Amino_list[i:i+50] for i in range(0, len(Amino_list), 50)]) ,end ="\n")
   
    
def Histogram():
    Acid_list = []
    global AA_dict
    loaded_file.seek(0)
    for line in loaded_file:
        if line.startswith('SEQRES'):
            linelist= line.split()[4:]
            for aa in linelist:
                Acid_list.append(aa)
    AA_dict = {}
    for amino in Acid_list:
        AA_dict[amino] = AA_dict.get(amino,0)+1
    for key in AA_dict.keys():
        sortAmino_Acids()

def sortAmino_Acids():
    print("Choose an option to order by: \n number of amino acids - ascending (an) \n number of amino acids - descending (dn) \
    \n alphabetically - ascending (aa) \n alphabetically - descending (da)")
    option = input("Order by: ")
    if option.lower() == "an":
        for key, value in sorted(AA_dict.items(), key = lambda item: item[1]):
            print("%s ( %2s)" % (key, value),": %s" %("*"*int(value)))

    elif option.lower() == 'dn':
        for key, value in sorted(AA_dict.items(), key = lambda item: item[1], reverse = True):
            print("%s ( %2s)"  %(key, value),": %s" %("*"*int(value)))

    elif option.lower() == 'aa':
        for key in sorted(AA_dict):
            print('%s ( %2s)' %(key,AA_dict[key]),": %s"%("*"*int(AA_dict[key])))

    elif option.lower() == 'da':
        for key in sorted(AA_dict,reverse = True):
            print('%s ( %2s)'%(key,AA_dict[key]),": %s"%("*"*int(AA_dict[key])))
    else:
        print("Invalid option. Enter a valid option from the choices")
        option = input("Please enter a valid option from the menu: ")
        sortAmino_Acids()
    
PDB_File = "None" 
def menu(PDB_File):
    print("*"*103)
    print("*  PDB FILE ANALYZER                                                                                  *")
    print("*"*103)
    print("* Select an option from below: ")
    print("*                                                                                                     *")
    print("*   1) Open a PDB File                (O)                                                             *")
    print("*   2) Information                    (I)                                                             *")
    print("*   3) Show histogram of amino acids  (H)                                                             *")
    print("*   4) Display Secondary Structure    (S)                                                             *")
    print("*   5) Export PDB File                (X)                                                             *")
    print("*   6) Exit                           (Q)                                                             *")
    print("*                                                                                                     *")
        
    print("*                                                                    Current PDB: ", PDB_File,          )
    print("*"*103) 
            
    option = input(":")
    if option.lower() in ('o','i','h','s','1','2','3'): 
        if option.lower() == 'o' or option.upper() == 'O' or option == '1':
            PDB_File = Open_file()
            menu(PDB_File)
        elif option.lower() == 'i' or option.upper() == 'I' or option == '2':
            Information()
            menu(PDB_File)
        elif option.lower() == 'h' or option.upper() == 'H' or option == '3':
            Histogram()
            menu(PDB_File)
        else:
            print("Invalid Choice. Please choose a valid option from the menu")
            
    
menu(PDB_File)