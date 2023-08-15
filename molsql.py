import os
import sqlite3
import MolDisplay

class Database:
    
    #creates a data base connection and stores it as a class attribute
    #if reset is set to true it deletes old database and creates a fresh one
    def __init__(self, reset = False):
        
        #if reset is true and database exists remove it
        if(reset == True):
            if os.path.exists('molecules.db'):
                os.remove('molecules.db')

        self.conn = sqlite3.connect('molecules.db') #creates and opens new database connection

    #creates SQL tables
    def create_tables(self):
        
        #Elements table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Elements 
                 ( ELEMENT_NO     INTEGER NOT NULL,
                   ELEMENT_CODE   VARCHAR(3) NOT NULL,
                   ELEMENT_NAME  VARCHAR(32) NOT NULL,
                   COLOUR1    CHAR(6) NOT NULL,
                   COLOUR2    CHAR(6) NOT NULL,
                   COLOUR3   CHAR(6) NOT NULL,
                   RADIUS   DECIMAL(3) NOT NULL,
                   PRIMARY KEY (ELEMENT_CODE) );""" )
        
        #Atoms table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Atoms 
                 ( ATOM_ID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   ELEMENT_CODE   VARCHAR(3) NOT NULL,
                   X    DECIMAL(7,4) NOT NULL,
                   Y    DECIMAL(7,4) NOT NULL,
                   Z    DECIMAL(7,4) NOT NULL,
                   FOREIGN KEY (ELEMENT_CODE) REFERENCES ELEMENTS );""" )
        
        #Bonds table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Bonds 
                 ( BOND_ID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   A1 INTEGER NOT NULL,
                   A2 INTEGER NOT NULL,
                   EPAIRS INTEGER NOT NULL );""" )
        
        #Molecules table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Molecules 
                 ( MOLECULE_ID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   NAME TEXT UNIQUE NOT NULL );""" )
        
        #MoleculeAtom table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom 
                 ( MOLECULE_ID     INTEGER NOT NULL,
                   ATOM_ID     INTEGER NOT NULL,
                   PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                   FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                   FOREIGN KEY (ATOM_ID) REFERENCES Atoms);""" )
        
        #MoleculeBond table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond 
                 ( MOLECULE_ID     INTEGER NOT NULL,
                   BOND_ID     INTEGER NOT NULL,
                   PRIMARY KEY (MOLECULE_ID, BOND_ID),
                   FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                   FOREIGN KEY (BOND_ID) REFERENCES Bonds);""" )
    
    #sets values in table based on tuple values
    #got help from lab
    def __setitem__(self, table, values):
      temp = len(values)
      str = "(" + ",".join(["?"]*temp) + ")"
      query = f"INSERT INTO {table} VALUES {str}"
      cursor = self.conn.cursor()
      cursor.execute(query,values)
      self.conn.commit()
      
    
    #adds attributes of the atom object to the Atoms table
    #and adds an entry to MoleculeAtom that links the named molecule to the atom entry
    def add_atom(self, molname, atom): 
      cursor = self.conn.cursor()
      
      #query and parameters for atoms table 
      atomsQuery = "INSERT INTO Atoms (ELEMENT_CODE,X,Y,Z) VALUES (?,?,?,?)"  
      atomsParams = (atom.element,atom.x,atom.y,atom.z) 
      cursor.execute(atomsQuery,atomsParams) #inserting into Atoms table
      
      atom_id = cursor.execute("""SELECT last_insert_rowid();""").fetchone() #getting atom id
      
      #query for molecule atoms table
      moleculeAtomQuery = "INSERT INTO MoleculeAtom (MOLECULE_ID, ATOM_ID) VALUES (?,?)"
      
      #getting molecule ID
      molecule_id = cursor.execute("""SELECT Molecules.MOLECULE_ID FROM Molecules;""").fetchall()
      #params for MoleculeAtom table
      moleculeAtomParams = (int(len(molecule_id) - 1) + 1,int(atom_id[0])) #first param gets last entry to molecule ID
      
      cursor.execute(moleculeAtomQuery,moleculeAtomParams) #inserting into MoleculeAtom table
    
    #add attributes of the bond object to the Bonds table
    #adds entry to MoleculeBond table to link named molecule to the entry in the Bonds table
    def add_bond(self, molname, bond):
      cursor = self.conn.cursor()
      
      #query and parameters for Bonds table 
      bondsQuery = "INSERT INTO Bonds (A1,A2,EPAIRS) VALUES (?,?,?)"  
      bondsParams = (bond.a1,bond.a2,bond.epairs) 
      cursor.execute(bondsQuery,bondsParams) #inserting into Bonds table
      bond_id = cursor.execute("""SELECT last_insert_rowid();""").fetchone()
      
      #query for molecule atoms table
      moleculeBondQuery = "INSERT INTO MoleculeBond (MOLECULE_ID, BOND_ID) VALUES (?,?)"
      
      #getting molecule ID
      molecule_id = cursor.execute("""SELECT Molecules.MOLECULE_ID FROM Molecules;""").fetchall()
      
      #params for MoleculeBond table
      moleculeBondParams = (int(len(molecule_id) - 1) + 1,bond_id[0]) #first param gets last entry to molecule ID
      
      cursor.execute(moleculeBondQuery,moleculeBondParams) #inserting into MoleculeAtom table
     
    #creates a Molecule object and parses fp, adds an entry to the Molecules table
    #calls add_atom and add_bond on the data base for each atom and bond returned by 
    #get_atom and get_bond
    def add_molecule(self, name, fp):
      
      mol = MolDisplay.Molecule() #creating object
      mol.parse(fp) #parsing fp
      
      moleculesQuery = "INSERT INTO Molecules (NAME) VALUES (?)" 
      moleculesParams = ((name,))
      
      cursor = self.conn.cursor()
      
      cursor.execute(moleculesQuery,moleculesParams)
      
      #adding each atom in the molecule to the table
      for i in range(mol.atom_no):
        atom = mol.get_atom(i)
        self.add_atom(name,atom)
      
      #adding each bond in the molecule to the table
      for j in range(mol.bond_no):
        bond = mol.get_bond(j)
        self.add_bond(name,bond)
      
      # self.conn.commit()
      # print(cursor.execute("SELECT * FROM Molecules").fetchall())
    
    #retrieve all the atoms and bonds in the data base associated with the molecule name
    #and append them to the molecule in order of increasing ID
    def load_mol(self,name):
      mol = MolDisplay.Molecule()
      cursor = self.conn.cursor()
      
      #join between Molecules, MoleculeAtom, and Atoms table to find all atoms associated with the molecule name
      atomsQuery = "SELECT * FROM Molecules, MoleculeAtom, Atoms WHERE Molecules.NAME = (?) AND Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID AND Atoms.ATOM_ID = MoleculeAtom.ATOM_ID ORDER BY ATOM_ID ASC"
      atomsParams = ((name,))
      
      #getting all rows of the joined table and finding the num rows
      atomsTable = cursor.execute(atomsQuery,atomsParams).fetchall()
      numRows = len(atomsTable)
      
      #append each atom in each row
      for i in range(numRows):
        #index 5: element name, 6: x, 7: y, 8: z
        mol.append_atom(atomsTable[i][5], atomsTable[i][6], atomsTable[i][7], atomsTable[i][8])
      
      #join between Molecules, MoleculeBond, and Bonds table to find all occurences associated with the molecule name
      bondsQuery = "SELECT * FROM Molecules, MoleculeBond, Bonds WHERE Molecules.NAME = (?) AND Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID AND Bonds.BOND_ID = MoleculeBond.BOND_ID ORDER BY BOND_ID ASC"
      bondsParams = ((name,))
      
      #getting all rows of joined table and finding the num rows
      bondsTable = cursor.execute(bondsQuery,bondsParams).fetchall()
      numRows2 = len(bondsTable)
      
      #append each bond in each row
      for i in range(numRows2):
        #index 5: a1, 6: a2 7: epairs
        mol.append_bond(bondsTable[i][5], bondsTable[i][6], bondsTable[i][7])
      
      return mol
    
    #returns python dictonary mapping ELEMENT_CODE values to RADIUS values in Elements table 
    def radius(self):
      #sampe dictionary
      # radius = { 'H': 25,
                  # 'C': 40,
                  # 'O': 40,
                  # 'N': 40,
                # }
      
      cursor = self.conn.cursor()
      dict = {}
      
      #getting all the ELEMENT_CODE values from Elements table
      codeQuery = "SELECT ELEMENT_CODE FROM Elements ORDER BY RADIUS"
      elementCodes = cursor.execute(codeQuery).fetchall()
      size  = len(elementCodes)
      
      
      #getting all the RADIUS values from Elements table
      radiusQuery = "SELECT RADIUS FROM Elements"
      radiuses = cursor.execute(radiusQuery).fetchall()
      
      #adding element codes and radiuses to dictonary 
      for i in range(size):
        temp1 = ''.join(elementCodes[i])
        dict[temp1] = radiuses[i][0]
      
      
      return dict
    
    #returns a python dictornary mapping ELEMENT_CODE values to RADIUS values based on Elements table
    def element_name(self):
        #element_name = { 'H': 'Hydrogen',
                        # 'C': 'Carbon',
                        # 'O': 'Oxygen',
                        # 'N': 'Nitrogen',
                        # }
      
      cursor = self.conn.cursor()
      dict = {}
      
      #getting all the ELEMENT_CODE values from Elements table
      codeQuery = "SELECT ELEMENT_CODE FROM Elements ORDER BY RADIUS"
      elementCodes = cursor.execute(codeQuery).fetchall()
      size  = len(elementCodes)
      
      #getting all the ELEMENT_NAME values from Elements table
      nameQuery = "SELECT ELEMENT_NAME FROM Elements"
      elementNames = cursor.execute(nameQuery).fetchall()
      
      #adding elements name and code to dictionary
      for i in range(size):
        temp1 = ''.join(elementCodes[i])
        temp2 = ''.join(elementNames[i])
        dict[temp1] = temp2
      
      return dict
    
    #returns a python string consisting of multiple concatenations of the following string constant
    #got help in the lab
    def radial_gradients(self):
      cursor = self.conn.cursor()
      myString = ""
      radialGradientSVG = """
          <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
          <stop offset="0%%" stop-color="#%s"/>
          <stop offset="50%%" stop-color="#%s"/>
          <stop offset="100%%" stop-color="#%s"/>
          </radialGradient>"""

      #getting values needed from element table
      temp = cursor.execute("""SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements""").fetchall()
      #adding values to radial gradient string
      for i in temp:
        tempString = radialGradientSVG % (i[0], i[1], i[2], i[3])
        myString += tempString
      
      myString +="""
          <radialGradient id="default" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
          <stop offset="0%" stop-color="#FFFFFF"/>
          <stop offset="50%" stop-color="#050505"/>
          <stop offset="100%" stop-color="#020202"/>
          </radialGradient>"""
    
      return myString
      