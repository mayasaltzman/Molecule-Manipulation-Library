#include "mol.h"

/******
atomset: copies values of element,x,y, and z into the atom stored at atom
In: atom *atom, char element[3], double *x, double *y, double *z
Out: void
*******/
void atomset(atom *atom, char element[3], double *x, double *y, double *z)
{
    strcpy(atom->element, element);
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

/******
atomget: copies values at atom to locations pointed to by element,x,y and z
In: atom *atom, char element[3], double *x, double *y, double *z
Out: void
*******/
void atomget(atom *atom, char element[3], double *x, double *y, double *z)
{
    strcpy(element, atom->element);
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

/******
bondset: copies values a1, a2, atoms, and epairs into bond and calls compute cords
In: bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs
Out: void
*******/
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;
    compute_coords(bond);
}

/******
bondget: copies attributes in bond to a1, a2, atoms, and epairs
In: bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs
Out: void
*******/
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;
}

/******
compute_coords: computes the z, x1, y1, x2, y2, len, dx, and dy values of the bond
and sets them in the struct memeber variables
In: bond *bond
Out: void
*******/
void compute_coords(bond *bond)
{
    // x1,y1,x2,y2 store the x and y cords of of atoms a2 and atoms a2
    bond->x1 = bond->atoms[bond->a1].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;

    // z store the average z value of a1 and a2
    bond->z = ((bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2);

    // len stores the distance from a1 to a2
    double coordDistance = ((bond->atoms[bond->a2].x - bond->atoms[bond->a1].x) * (bond->atoms[bond->a2].x - bond->atoms[bond->a1].x)) + ((bond->atoms[bond->a2].y - bond->atoms[bond->a1].y) * (bond->atoms[bond->a2].y - bond->atoms[bond->a1].y));
    bond->len = sqrt(coordDistance);

    // dx and dy store differences between the x and y values of a2 and a1 divided by the length of the bond
    bond->dx = (bond->atoms[bond->a2].x - bond->atoms[bond->a1].x) / bond->len;
    bond->dy = (bond->atoms[bond->a2].y - bond->atoms[bond->a1].y) / bond->len;
}

/******
molmalloc: gives arrays atoms, atom_ptrs and bonds and bond_ptrs enough memory to hold atom_max atoms and bond_max bonds
then returns the address of the malloced area of memory
In: unsigned short atom_max, unsigned short bond_max
Out: molecule
*******/
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max)
{
    molecule *molecule = malloc(sizeof(struct molecule));

    // NULL check
    if (molecule == NULL)
    {
        printf("malloc produced NULL in molmalloc");
        return NULL;
    }

    molecule->atom_max = atom_max; // copying value of atom_max
    molecule->atom_no = 0;         // setting atom_no to 0

    molecule->bond_max = bond_max; // copying value of atom_max
    molecule->bond_no = 0;         // setting bond_no to 0

    molecule->atoms = (struct atom *)malloc(atom_max * sizeof(struct atom)); // allocating atoms to be the size of atom_max

    // NULL check
    if (molecule->atoms == NULL)
    {
        printf("malloc produced NULL in molmalloc");
        return NULL;
    }

    molecule->atom_ptrs = (struct atom **)malloc(atom_max * sizeof(struct atom *)); // allocating atoms_ptrs to be the size of atom_max

    // NULL check
    if (molecule->atom_ptrs == NULL)
    {
        printf("malloc produced NULL in molcmalloc");
        return NULL;
    }

    // assigning atom_ptrs to point to each atom in atoms
    for (int i = 0; i < atom_max; i++)
    {
        molecule->atom_ptrs[i] = &molecule->atoms[i];
    }

    molecule->bonds = (struct bond *)malloc(bond_max * sizeof(struct bond)); // allocating bonds to be the size of bond_max

    // NULL check
    if (molecule->bonds == NULL)
    {
        printf("malloc produced NULL in molmalloc");
        return NULL;
    }

    molecule->bond_ptrs = (struct bond **)malloc(bond_max * sizeof(struct bond *)); // allocating bonds_ptrs to be the size of bond_max

    // NULL check
    if (molecule->bond_ptrs == NULL)
    {
        printf("malloc produced NULL in molmalloc");
        return NULL;
    }

    // assigning bonds_ptrs to point to each bond in bonds
    for (int i = 0; i < bond_max; i++)
    {
        molecule->bond_ptrs[i] = &molecule->bonds[i];
    }

    return molecule;
}

/******
molcopy: copied values from src into new molecule structure, allocates memory of atoms, atom_ptrs, bonds, and bond_ptrs
to match the size of src then returns the address of the malloced area of memory
In: molecule *src
Out: molecule
*******/
molecule *molcopy(molecule *src) // this doesn't work lol
{
    molecule *mol;

    mol = molmalloc(src->atom_max, src->bond_max); // allocating memory to match the size of src

    // NULL check
    if (mol == NULL)
    {
        printf("malloc produced NULL in molcopy");
        return NULL;
    }

    // adding atoms from src to new molecule
    for (int i = 0; i < src->atom_no; i++)
    {
        molappend_atom(mol, &src->atoms[i]);
    }

    // adding bonds from src to new molecule
    for (int j = 0; j < src->bond_no; j++)
    {
        molappend_bond(mol, &src->bonds[j]);
    }

    return mol;
}

/******
molfree: frees memory associated with ptr
In: molecule *ptr
Out: void
*******/
void molfree(molecule *ptr)
{
    free(ptr->atoms);     // free atoms
    free(ptr->atom_ptrs); // free array of ptrs
    free(ptr->bonds);     // free bonds
    free(ptr->bond_ptrs); // free array of ptrs
    free(ptr);
}

/******
molappend_atom: copies atom to be the first empty atom in the atoms array
then set the first empty ptr in atom_ptrs to the atom in the atoms array and increments atom_no
if atom_no = atom_max then the capacity of atoms and atom_ptrs is increased with realloc
if atom_max is 0 it is incremented to one
if atom_max is not 0 it is doubled
In: molecule *molecule, atom *atom
Out: void
*******/
void molappend_atom(molecule *molecule, atom *atom)
{
    // do this before add the atom if
    if (molecule->atom_no == molecule->atom_max) // checking to see if arrays need to be resized
    {
        if (molecule->atom_max == 0)
        {
            molecule->atom_max = 1;
        }
        else
        {
            molecule->atom_max = molecule->atom_max * 2;
        }
        molecule->atoms = (struct atom *)realloc(molecule->atoms, molecule->atom_max * sizeof(struct atom));                // increasing capacity of atoms
        molecule->atom_ptrs = (struct atom **)realloc(molecule->atom_ptrs, (molecule->atom_max) * (sizeof(struct atom *))); // increasing capacity of atom_ptrs

        // making pointers point to corresponding atoms in new array
        for (int i = 0; i < molecule->atom_max; i++)
        {
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    }

    molecule->atoms[molecule->atom_no] = *atom;                                   // assign "empty" atom int atoms to be atom
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no]; // assign "empty" atom in atom_ptrs to point to index of atom in atoms array
    molecule->atom_no++;                                                          // incrementing atom_no
}

/******
molappend_bond: operates the same as molappend_atom but for bonds
In: molecule *molecule, bond *bond
Out: void
*******/
void molappend_bond(molecule *molecule, bond *bond)
{
    // printf("in mol append bond\n");
    if (molecule->bond_no == molecule->bond_max) // checking to see if arrays need to be resized
    {
        // printf("array needs to be resized\n");
        if (molecule->bond_max == 0)
        {
            // printf("size is 0");
            molecule->bond_max = 1;
        }
        else
        {
            // printf("size doubles by 2\n");
            molecule->bond_max = molecule->bond_max * 2;
        }
        // printf("reallocing\n");
        molecule->bonds = (struct bond *)realloc(molecule->bonds, molecule->bond_max * sizeof(struct bond));                // increasing capacity of bonds
        molecule->bond_ptrs = (struct bond **)realloc(molecule->bond_ptrs, (molecule->bond_max) * (sizeof(struct bond *))); // increasing capacity of bond_ptrs
        // printf("reallocing done\n");

        // making pointers point to corresponding bonds in new array
        for (int i = 0; i < molecule->bond_max; i++)
        {
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
        // printf("pointers are matched to new array\n");
    }

    molecule->bonds[molecule->bond_no] = *bond;                                   // assign "empty" bond int bonds to be atom
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no]; // assign "empty" bond in bond_ptrs to point to index of bond in bonds array
    molecule->bond_no++;
    // printf("function finished\n"); // incrementing bond_no
}

/******
atom_ptrs_cmp: helper function for qsort, compares the z values in the atom struct
returns a value less than, equal, or greater than zero if the first argument is less than
equal to, or greater than the second
In: const void *a, const void *b
Out: int
*******/
int atom_ptrs_cmp(const void *a, const void *b)
{
    int toReturn = 0;
    struct atom **a_ptr, **b_ptr;
    a_ptr = (struct atom **)a;
    b_ptr = (struct atom **)b;

    // returning a value based on if the first argument is less than, equal, to, or greater than the second
    if (((**a_ptr).z) < ((**b_ptr).z))
    {
        toReturn = -1;
    }
    else if ((**a_ptr).z == (**b_ptr).z)
    {
        toReturn = 0;
    }
    else if ((**a_ptr).z > (**b_ptr).z)
    {
        toReturn = 1;
    }

    return toReturn;
}

/******
bond_ptrs_cmp: helper function for qsort, compares the z values in the bond struct
returns a value less than, equal, or greater than zero if the first argument is less than
equal to, or greater than the second
In: const void *a, const void *b
Out: int
*******/
int bond_ptrs_cmp(const void *a, const void *b)
{
    int toReturn = 0;
    struct bond **a_ptr, **b_ptr;
    a_ptr = (struct bond **)a;
    b_ptr = (struct bond **)b;

    // // returning a value based on if the first argument is less than, equal, to, or greater than the second
    if (((**a_ptr).z) < ((**b_ptr).z))
    {
        toReturn = -1;
    }
    else if ((**a_ptr).z == (**b_ptr).z)
    {
        toReturn = 0;
    }
    else if ((**a_ptr).z > (**b_ptr).z)
    {
        toReturn = 1;
    }

    return toReturn;
}

/******
molsort: sorts atom_ptrs array in order of increasing z value
sorts bond_ptrs in order of increasing z value (for bonds z value is average of two z values in their atoms)
uses qsort
In: molecule *molecule
Out: void
*******/
void molsort(molecule *molecule)
{
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom *), atom_ptrs_cmp); // sorting atom_ptrs array
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond *), bond_ptrs_cmp); // sorting bond_ptrs array
}

/******
xrotation: set values in an affine transformation matrix corresponding to a
roation of degrees around the x-axis
In: xform_matrix xform_matrix, unsigned short deg
Out: void
*******/
void xrotation(xform_matrix xform_matrix, unsigned short deg)
{
    double rad = deg * (PI / 180.0); // converting degrees to radians
    // sample matrix for rotation around the x axis
    //                   0  1  2
    //  xform_matrix = {{1, 0, 0},        0
    //                  {0, cos, -sin,},   1
    //                  {0, sin, cos,}};   2

    // setting values of the 0th row
    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;

    // setting the values 1st row
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = -sin(rad);

    // seting the values 2nd row
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);
}

/******
yrotation: set values in an affine transformation matrix corresponding to a
roation of degrees around the y-axis
In: xform_matrix xform_matrix, unsigned short deg
Out: void
*******/
void yrotation(xform_matrix xform_matrix, unsigned short deg)
{
    double rad = deg * (PI / 180.0); // converting degrees to radians
    // sample matrix for rotation around the y axis
    //
    //  xform_matrix = {{cos, 0, sin},
    //                  {0, 1, 0,},
    //                  {-sin, 0, cos,}};

    // setting values of the 0th row
    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(rad);

    // setting the values 1st row
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;

    // seting the values 2nd row
    xform_matrix[2][0] = -sin(rad);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(rad);
}

/******
zrotation: set values in an affine transformation matrix corresponding to a
roation of degrees around the z-axis
In: xform_matrix xform_matrix, unsigned short deg
Out: void
*******/
void zrotation(xform_matrix xform_matrix, unsigned short deg)
{
    double rad = deg * (PI / 180.0); // converting degrees to radians

    // sample matrix for rotation around the z axis
    //
    //  xform_matrix = {{cos, -sin, 0},
    //                  {sin, cos, 0,},
    //                  {0, 0, 1}};

    // setting values of the 0th row
    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = -sin(rad);
    xform_matrix[0][2] = 0;

    // setting the values 1st row
    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0;

    // seting the values 2nd row
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

/******
mol_xform: apply the transformation matrix to all the atoms of the molecule
by performing a vector matrix multiplication on the x,y,z coordinates and
applying the compute coords function to each bond in the molecule
In: molecule *molecule, xform_matrix matrix
Out: void
*******/
void mol_xform(molecule *molecule, xform_matrix matrix)
{
    // temp variables for matrix multiplication
    double x = 0;
    double y = 0;
    double z = 0;

    for (int i = 0; i < molecule->atom_no; i++)
    {
        // performing matrix multiplication on rows and cols
        x = (matrix[0][0] * molecule->atoms[i].x) + (matrix[0][1] * molecule->atoms[i].y) + (matrix[0][2] * molecule->atoms[i].z);

        y = (matrix[1][0] * molecule->atoms[i].x) + (matrix[1][1] * molecule->atoms[i].y) + (matrix[1][2] * molecule->atoms[i].z);

        z = (matrix[2][0] * molecule->atoms[i].x) + (matrix[2][1] * molecule->atoms[i].y) + (matrix[2][2] * molecule->atoms[i].z);

        // setting values of the molecule
        molecule->atoms[i].x = x;

        molecule->atoms[i].y = y;

        molecule->atoms[i].z = z;
    }

    molecule->bonds->atoms = molecule->atoms; // bonds now points to new atoms array

    // calling compute coords on each bond in the molecule
    for (int i = 0; i < molecule->bond_no; i++)
    {
        compute_coords(&molecule->bonds[i]);
    }
}
