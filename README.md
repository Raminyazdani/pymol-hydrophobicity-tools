THEORETICAL EXERCISES
1. Choose a protein structure that you find interesting. Explain why you chose
this specific structure (1 Bonus point for the student with the best explana-
tion). Download the structure from PDB and load it in PyMOL, then describe
the complete protein structure organisation (you can rely on topology diagrams
and databases such as CATH/SCOP). (2 points)
2. Assume there is a mutation in the structure that increases the free energy value.
How would it affect the structure? Explain your answer. (1 point)
3. What is the significance of the Ramachandran plot in understanding protein
structure, and how can it be used to detect conformational strain? (1 point)
4. Why do the phi and psi angles of peptide bonds rarely fall into certain regions
of the Ramachandran plot, and what does this imply about protein folding? (1
point)

2 PROGRAMMING EXERCISES
1. Write a PyMOL script that will:
• load the structure of a protein (I recommend the 4UC1 structure, but you
can pick any protein you like)
• remove the water molecules
• colour ligands (organic molecules) cyan
• colour binding sites (residues within 5 angstroms of the ligands) grey
• colour Tryptophan residues magenta
• represent the ligand and binding site as sticks
• represent the rest of the protein as cartoon of your preferred colour (other
than colours mentioned above)
• export the result as a png file
The script should be launchable with the
pymol assignment2_1_template.pml or through the internal PyMOL script run-
ning command, and should include the fetching of the structure from PDB. (1
point)
2. Write a Python script by filling TODO parts in assignment2_2_template.py that
will calculate the hydrophobicity of a provided protein structure for amino acid
chain A with a window size of 3 for smoothing/averaging. Refer to the Kyte-
Doolittle scale for the exact values. Plot the resulting averaged values as a line
graph (save it as png). The PDB structure needs to be provided as the command-
line argument to the script. (2 points)
3. Write a PyMOL extension by filling TODO parts in assignment2_3_template.py
that will colour each residue in a given PyMOL selection according to the Kyte-
Doolittle scale. The extension has to be imported into PyMOL with run sur-
name_matriculatonnumber_assignment2_3.py from the PyMOL command line,
and has to be launchable with the hydrophobicity [, selection [, palette]]
from inside PyMOL. Refer to the PyMOL wiki and provided code snippet for guid-
ance. (2 points)
4. Add a window keyword argument to the PyMOL extension that will be able to ap-
ply a smoothing window (like question 2) of arbitrary odd-valued size. (1 bonus
point)