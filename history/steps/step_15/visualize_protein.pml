# Load protein structure
fetch 4uc1

# Remove water molecules
remove resn HOH
remove solvent

# Represent the protein as cartoon
as cartoon

# Colour protein to X
color yellow

# Colour ligands (organic molecules) X
# colour ligands (organic molecules) cyan
select ligand, organic
color cyan, ligand

# Colour binding sites (residues within 5 angstroms of the ligands) X
# colour binding sites (residues within 5 angstroms of the ligands) grey
select binding_site, byres (ligand around 5)
color grey , binding_site

# Colour X residues X
# colour Tryptophan residues magenta
select tryptophan_residues, resn TRP
color magenta, tryptophan_residues

# Represent the ligand and binding site as sticks
show sticks, ligand
show sticks, binding_site

# deselect
deselect

# Export result as png file in your working directory
png ./protein_visualization.png , dpi=300
