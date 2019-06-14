#!/bin/python
def Open_file():
    """Function for opening PDB file""" 
    global loaded_file 
    Input_File = input("Enter a valid PDB File: ")              #Prompts a user to enter a valid PDB file      
    file = Input_File.split("/")
    sep = "/".join(Input_File[:-1])  #Splits entered file name if file path is provided in input
    PDB_File = file[-1]
    print("The PDB file", PDB_File, "has been successfully loaded") #If PDB file is successfully loaded, user sees message
    loaded_file = open(PDB_File, "r")       #The entered PDB file is opened for reading
    return PDB_File

def Information():
    """This function enables a user to view information about the entered PDB file such as Title of file,
    the file name, no of chains, sheets and helix"""
    title_info = []
    for line in loaded_file:
        if line.startswith ('HEADER'):
            Lines = line.split()
            Header = Lines[4]          #Getting the file name
        if line.startswith('TITLE'):
            title_info.append(line[9:-4])
    print("PDB File: %s " %Header)
    Title = title_info[0] + title_info[1]     #Getting the file title
    print("Title:", Title)

    chains = []         #Empty list for appending chains present in pdb file
    loaded_file.seek(0) #Returns cursor to beginning of file after end of loops above
    for line in loaded_file:    
        if line.startswith('SEQRES'):  
            if line[11] not in chains:   #If chain is present on file and has not been appended to chains list,it is added
                chains.append(line[11])
    print("CHAINS:", chains[0], "and", chains[1])

    for chain in chains:
        Amino_list = []
        Helix = 0       #For getting number of Helices and sheets. Initially set to zero to allow for looping
        Sheet = 0
        loaded_file.seek(0)
        for line in loaded_file:
            if line.startswith('HELIX'): #Counts every instance of a helix on file
                if chain == line[19]:
                    Helix += 1
            if line.startswith("SHEET"):
                if chain == line[32]:      #Counts every instance of a sheet on file
                    Sheet += 1
            if line.startswith('SEQRES'):
                    Amino_dict = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLY':'G','GLN':'Q','GLU':'E','HIS':'H',\
                  'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
                    Lines = line.split()
                    Amino_seq = list(Lines[4:])
                    Dict_amino = {}                   #Getting the sequence of amino acids on file
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
        print("Sequence:",'\n          '.join([Amino_list[i:i+50] for i in range(0, len(Amino_list), 50)]))  #Limiting number of amino acids per line to 50
        return chains
        return title_info
        return Amino_list
    
def Histogram():
    """Function for generating a Histogram for user"""
    Acid_list = [] #Initilises an empty AMino acid list
    global AA_dict
    loaded_file.seek(0)
    for line in loaded_file:
        if line.startswith('SEQRES'):
            lines= line.split()[4:]
            for aa in lines:
                Acid_list.append(aa)
    AA_dict = {}
    for amino in Acid_list:     #Getting all amino acids appended to acid list and assigning them AA dictionary
        AA_dict[amino] = AA_dict.get(amino,0)+1   #For each amino acid in dictionary, get the number of times it occurs added.
    for key in AA_dict.keys():
        sortAmino_Acids()     

def sortAmino_Acids():
    """Function for ordering amino acids according to user's choice"""
    print("Choose an option to order by: \n number of amino acids - ascending (an) \n number of amino acids - descending (dn) \
    \n alphabetically - ascending (aa) \n alphabetically - descending (da)")
    option = input("Order by: ")
    if option.lower() == "q" or option.upper() == "Q":
        menu(PDB_File)
    if option.lower() == "an":
        for key, value in sorted(AA_dict.items(), key = lambda item: item[1]):     #sorts amino acids from AA_dict in ascending order according to their numbers
            print("%s ( %2s)" % (key, value),": %s" %("*"*int(value)))

    elif option.lower() == 'dn':
        for key, value in sorted(AA_dict.items(), key = lambda item: item[1], reverse = True):   #Amino acids in Descending order according to number of each amino acid in dictionary
            print("%s ( %2s)"  %(key, value),": %s" %("*"*int(value)))

    elif option.lower() == 'aa':
        for key in sorted(AA_dict):
            print('%s ( %2s)' %(key,AA_dict[key]),": %s"%("*"*int(AA_dict[key])))   #Ascending order of amino acids alphabetically

    elif option.lower() == 'da':
        for key in sorted(AA_dict,reverse = True):
            print('%s ( %2s)'%(key,AA_dict[key]),": %s"%("*"*int(AA_dict[key])))  #Descending order of Amino acids alphabetically
    else:
        print("Invalid option. Enter a valid option from the choices")
        option = input("Please enter a valid option from the menu: ")
        sortAmino_Acids()
def Sec_struct_info():
    """Function for extracting the secondary structure on a PDB file"""
    loaded_file.seek(0)
    global sequences
    Amino_dict = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLY':'G','GLN':'Q','GLU':'E','HIS':'H',\
    'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}

    globals()['chains'] = []         #Empty list for appending chains present in pdb file
    for line in loaded_file:    
        if line.startswith('SEQRES'):  
            if line[11] not in chains:   #If chain is present on file and has not been appended to chains list,it is added
                chains.append(line[11])            
    loaded_file.seek(0)
    for chain in chains:
        sequences = ""
        for line in loaded_file:
            if line.startswith('SEQRES') and line[11]==chain:
                Lines = line.split()
                Amino_seq = list(Lines[4:])
                Dict_amino = {}                   #Getting the sequence of amino acids on file

                for key in Amino_seq:
                    Dict_amino[key] = Amino_dict[key]
                    sequences += Dict_amino.get(key)
        Secondary_structure(sequences, chain)
        loaded_file.seek(0)        
        
def Secondary_structure(Full, chain):
    """Works together with Sec_struct_info function. Takes full sequences and the chains to determine the sheets and Helices """
    loaded_file.seek(0)
    Helix_index = []
    Sheet_index = []
    Dashes = []
    Label_spaces = []
    Helix_label = []
    Helix_labels_index = []
    Sheet_label = []
    Sheet_labels_index = []
    for line in loaded_file:
        liney = line.split()
        if line.startswith("HELIX") and chain == liney[7]:
            Helix_line = line.split()
            Helic = Helix_line[5]          #Getting the Helix indices & labels and appending them to the empty Helix lists above
            Helic2 = Helix_line[8]
            Helix_labels_index.append(Helic)
            Helix_label.append(Helix_line[2]) 
            for i in range (int(Helic),int(Helic2)+1):
                Helix_index.append(i)
        if line.startswith("SHEET") and chain == liney[8]:
            sheet_line = line.split()
            sheet = sheet_line[6]        #Extracting sheets, their indices together with labels and appending to sheet lists 
            sheet2 = sheet_line[9]
            Sheet_labels_index.append(sheet)
            Sheet_label.append(str(sheet_line[1]) + str(sheet_line[2]))
            for j in range (int(sheet),int(sheet2)+1):
                Sheet_index.append(j)
                
    for i in range(0,len(Helix_labels_index)):
        Helix_labels_index[i]= int(Helix_labels_index[i])  
    for i in range(0, (len(Full))):
        Dashes.append('-')             #Assigning dashes that correspond to length of amino sequence
        Label_spaces.append(" ")
    for l,k in zip(Helix_labels_index,Helix_label):
        Label_spaces[l-1] = k
        
    for i in range(0,len(Helix_index)):
        Helix_index[i]= int(Helix_index[i])
    Helix_symbol = []
    for i in range(0,len(Helix_index)):   #Assigning the forward slash to the respective Helix 
        Helix_symbol.append('/')
    for index,symbol in zip(Helix_index,Helix_symbol):
        Dashes[index-1]= symbol
        
    for i in range(0,len(Sheet_labels_index)):
        Sheet_labels_index[i]= int(Sheet_labels_index[i])
    for sl,si in zip(Sheet_labels_index, Sheet_label):
        if len(si) > 1:
            Label_spaces[sl-1:sl+len(si)-1]=si
        else:
            Label_spaces[sl-1] = si
        
    for i in range(0,len(Sheet_index)):
        Sheet_index[i]= int(Sheet_index[i])
    Sheet_symbol = []
    for i in range(0,len(Sheet_index)):      #Assign | to extracted sheets 
        Sheet_symbol.append('|')
    for index,s in zip(Sheet_index,Sheet_symbol):
        Dashes[index-1]= s
    Sec_struct(''.join(sequences), ''.join(Dashes),''.join(Label_spaces), chain )
    
    
def Sec_struct(sequences, Dashes, Label_spaces,chain):
    """Function for printing the secondary structure. Takes input from the Secondary_structure and Sec_struct functions"""
    print('Chain:', chain)    
    print("(1)")
    for c in range(0,len(sequences),80):
        print(sequences[c:c+80],'\n', Dashes[c:c+80],'\n', Label_spaces[c:c+80])
    print("(",len(sequences),")\n")
    
Output_File = "Results/PDB_Export.txt"    
def ExportPDB(Output_File):
    """Function that exports information on loaded PDB file to a txt file in results folder"""
    with open(Output_File, 'a+') as Export_file:
        Export_file.write(str(Information()))

def Exit():
    loaded_file.close()
    menu(PDB_File)
    
PDB_File = "None"  #Initial, currently loaded PDB file is none when no file input
def menu(PDB_File):
    def printMenu():
        
        """Function for displaying the menu for PDB file Analyzer program"""
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

       
        option = str(input(":"))
        return option
    option =printMenu()
    if option.lower() in ('o','q','1','6'): 
        if option.lower() == 'o' or option.upper() == 'O' or option == '1':
            PDB_File = Open_file()     #Indicates currently loaded PDB file
            option = printMenu()
            def myOptions(option):
                if option.lower() in ('o','i','h','s','q','x','1','2','3','4','5','6'):
                    if option.lower() == 'i' or option.upper() == 'I' or option == '2':
                        Information()
                        option = printMenu()                                                           #Conditions for Various Menu Options
                        myOptions(option)
                    if option.lower() == 'h' or option.upper() == 'H' or option == '3':
                        Histogram()
                        option = printMenu()
                        myOptions(option)
                    if option.lower() == 's' or option.upper() == 'S' or option == '4':
                        Sec_struct_info()
                        option = printMenu()
                        myOptions(option)
                    if option.lower() == 'x' or option.upper() == 'X' or option == '5':
                        ExportPDB(Output_File)
                        option = printMenu()
                        myOptions(option)
                    if option.lower() == 'q' or option.upper() == 'Q' or option == '6':
                        Exit()
                else:
                    if option.lower() == 'o' or option.upper() == 'O' or option == '1':
                        print("Do you wish to replace current file?(Y/N)")
                        select = input(": ")
                        if select.lower() == "Y":
                            Exit()
                        elif select.lower() == "N":
                            printMenu()
                            myOptions(option)                                     #Allows user to replace currently loaded file
            myOptions(option)
    
            if option.lower() == 'o' or option.upper() == 'O' or option == '1':
                print("Do you wish to replace current file?(Y/N)")
                select = input(": ")
                if select.lower() == "y":
                    Exit()
                elif select.lower() == "n":
                    printMenu()
                    myOptions(option)

    else:
        if option.lower() == 'q' or option.upper() == 'Q' or option == '6':
            Exit()

        else:
            print("Invalid Choice. Please choose a valid option from the menu")
            menu(PDB_File)
menu(PDB_File)