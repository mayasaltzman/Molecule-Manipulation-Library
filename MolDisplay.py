import molecule
import molsql

# radius = { 'H': 25,
# 'C': 40,
# 'O': 40,
# 'N': 40,
# }

# element_name = { 'H': 'grey',
# 'C': 'black',
# 'O': 'red',
# 'N': 'blue',
# }

# svg header
header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""

# svg footer
footer = """</svg>"""

# offsets
offsetx = 500
offsety = 500


# Atom class that is a wrapper class for atom class in C code
class Atom:
    def __init__(self, c_atom):  # constructor with atom class as its argument
        self.atom = c_atom  # storing atom class as struct memeber variable
        self.z = c_atom.z  # initializing variable z to be value of the wrapped class

    # returns element, x, y, and z of atom
    def __str__(self):
        return "%s %f %f %f" % (self.atom.element, self.atom.x, self.atom.y, self.z)

    # returns string that has the atoms: x coordinate of centre circle, y coordinate of center circle, radius of center circle and color or centre circle
    def svg(self):
        db = molsql.Database(reset=False)
        elements = db.conn.execute( "SELECT * FROM Elements;" ).fetchall()
        elementCodes = []
        
        for i in elements:
            elementCodes.append(i[1])
        
        self.atom.x = (  # computing x coordinate of the centre of the circle representing the atom
            self.atom.x * 100.0 + offsetx
        )
        self.atom.y = (  # computing y coordinate of the centre of the circle representing the atom
            self.atom.y * 100.0 + offsety
        )
        
        if self.atom.element in elementCodes:
            self.atom.radius = radius[  # looking up element name in radius dictionary to find radius of circle representing the atom
                self.atom.element
            ]
            self.atom.color = element_name[  # looking up element name in element_name dictionary to find color of circle representing the atom
                self.atom.element
            ]
            
        else:
            self.atom.radius = 25
            self.atom.color = 'default'

        return ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (
            self.atom.x,
            self.atom.y,
            self.atom.radius,
            self.atom.color,
            )

# Bond class that is a wrapper class for bond class in C code
class Bond:
    def __init__(self, c_bond):  # constructor with bond class as its argument
        self.bond = c_bond  # storing bond class as struct memeber variable
        self.z = c_bond.z  # initializing variable z to be value of the wrapped class

    # returns the bonds: a1, a2, epairs, x1, y1, x2, y2, x, len, dx, and dy
    def __str__(self):
        return (
            "a1: %d a2: %d epairs: %d x1: %f y1: %f x2: %f y2: %f z: %f len: %f dx: %f dy: %f"
            % (
                self.bond.a1,
                self.bond.a2,
                self.bond.epairs,
                self.bond.x1,
                self.bond.y1,
                self.bond.x2,
                self.bond.y2,
                self.bond.z,
                self.bond.len,
                self.bond.dx,
                self.bond.dy,
            )
        )

    # returns a string with 8 values representing the x and y cords of a rectangle that looks like a thick line
    # between that atoms at either side of the bond, first calculate the end points of the thick line similarly to
    # to the way the positions of the centres of the circles are used in atoms then determining the corners by
    # moving perpindicularly to the direction of the bond 10 pixels from the centre
    def svg(self):
        # calculating end points of the thick line
        endPoint1_x = self.bond.x1 * 100.0 + offsetx
        endPoint1_y = self.bond.y1 * 100.0 + offsety
        endPoint2_x = self.bond.x2 * 100.0 + offsetx
        endPoint2_y = self.bond.y2 * 100.0 + offsety

        # getting x and y cords of top left point in rectangle
        topLeft_x = endPoint1_x + self.bond.dy * 10.0
        topLeft_y = endPoint1_y - self.bond.dx * 10.0

        # getting x and y cords of bottom left point in rectangle
        bottomLeft_x = endPoint1_x - self.bond.dy * 10.0
        bottomLeft_y = endPoint1_y + self.bond.dx * 10.0

        # getting x and y cords of top right point in rectangle
        topRight_x = endPoint2_x + self.bond.dy * 10.0
        topRight_y = endPoint2_y - self.bond.dx * 10.0

        # getting x and y cords of bottom right point in rectangle
        bottomRight_x = endPoint2_x - self.bond.dy * 10.0
        bottomRight_y = endPoint2_y + self.bond.dx * 10.0

        return (
            ' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n'
            % (
                topLeft_x,
                topLeft_y,
                bottomLeft_x,
                bottomLeft_y,
                bottomRight_x,
                bottomRight_y,
                topRight_x,
                topRight_y,
            )
        )


class Molecule(molecule.molecule):
    # prints out bonds and atoms in the molecule
    def __str__(self):
        molStr = ""
        # going through each atom in molecule
        for x in range(self.atom_no):
            atom = Atom(self.get_atom(x))  # get atom
            molStr = molStr + atom.__str__()  # add atom as string to molStr
        # going through each bond in molecule
        for y in range(self.bond_no):
            bond = Bond(self.get_bond(y))  # get bond
            molStr = molStr + bond.__str__()  # add atom as string to molStr
        return molStr

    # helper function to assist in sorting
    def sortZ(self, item):
        return item.z

    def svg(self):
        str = header
        item = []
        # adding all atoms to item
        for i in range(self.atom_no):
            atom = Atom(self.get_atom(i))
            item.append(atom)

        # adding all atoms to item
        for i in range(self.bond_no):
            bond = Bond(self.get_bond(i))
            item.append(bond)

        item.sort(key=self.sortZ)  # sorts items by their z valur

        # add each element of the sorted item as an svg to the str
        for i in item:
            str = str + i.svg()

        str = str + footer
        return str

    def parse(self, f):
        # reading lines of file object f starting at the 3rd line
        lines = f.readlines()[3:]  # this makes the file into a list starting at line 3
        firstLine = lines[0].split(
            " "
        )  # splitting first line of the list lines into spaces

        notSpaces = []
        # iterating over the first line to find elements that aren't spaces
        x = 0
        while x < len(firstLine):
            if firstLine[x] != "":
                notSpaces.append(firstLine[x])
            x += 1

        # getting the number of atoms
        atoms = int(notSpaces[0])
        lineCount = 1
        splitAtoms = []
        # iterating over the atoms and splitting them into a list seperates by spaces
        while lineCount <= atoms:
            splitAtoms.append(lines[lineCount].split(" "))
            lineCount += 1

        splitAtoms2 = []
        # parsing out spaces from splitAtoms
        for i in range(len(splitAtoms)):
            for j in range(len(splitAtoms[i])):
                if splitAtoms[i][j] != "":
                    splitAtoms2.append(splitAtoms[i][j])

        # seperating atoms into rows
        n = 16
        atomsSeperated = []
        atomsSeperated = [
            splitAtoms2[i * n : (i + 1) * n]
            for i in range((len(splitAtoms2) + n - 1) // n)
        ]

        # getting rid of info we dont need that comes after params before append_atom
        justAtomInfo = []
        for i in range(len(atomsSeperated)):
            for j in range(4):
                justAtomInfo.append(atomsSeperated[i][j])

        # breaking up the atom info by 4s so reach list can be params in append_atom
        n = 4
        atomsFinal = [
            justAtomInfo[i * n : (i + 1) * n]
            for i in range((len(justAtomInfo) + n - 1) // n)
        ]

        for i in range(len(atomsFinal)):
            self.append_atom(
                atomsFinal[i][3],
                float(atomsFinal[i][0]),
                float(atomsFinal[i][1]),
                float(atomsFinal[i][2]),
            )

        # getting the number of bonds
        bonds = int(notSpaces[1])
        lineCount2 = lineCount  # will start interating over bonds after atoms
        # splitting bonds by spaces
        splitBonds = []
        while (
            lineCount2 <= bonds + atoms
        ):  # start from index of last atom to bond + atoms
            splitBonds.append(lines[lineCount2].split(" "))
            lineCount2 += 1

        # removing spaces
        splitBondsNoSpaces = []
        for i in range(len(splitBonds)):
            for j in range(len(splitBonds[i])):
                if splitBonds[i][j] != "":
                    splitBondsNoSpaces.append(splitBonds[i][j])

        # seperating bonds into rows
        n = 7
        bondsSeperated = [
            splitBondsNoSpaces[i * n : (i + 1) * n]
            for i in range((len(splitBondsNoSpaces) + n - 1) // n)
        ]
        # getting rid of info we dont need that comes after params before append_bond
        justBondInfo = []
        for i in range(len(bondsSeperated)):
            for j in range(3):
                justBondInfo.append(bondsSeperated[i][j])

        # breaking up the bond info by 3s so reach list can be params in append_bond
        n = 3
        bondsFinal = [
            justBondInfo[i * n : (i + 1) * n]
            for i in range((len(justBondInfo) + n - 1) // n)
        ]
        
        for i in range(len(bondsFinal)):
            self.append_bond(
                int(bondsFinal[i][0])-1, int(bondsFinal[i][1])-1, int(bondsFinal[i][2])
            )
