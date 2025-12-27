# PyMOL Protein Visualization Script
fetch 4UC1

# Clean up
remove solvent

# Color ligands
select ligands, organic
color cyan, ligands

# Highlight binding sites (within 5A of ligands)
select binding_site, byres (ligands around 5)
color grey70, binding_site

# Highlight specific residues
select trp_residues, resn TRP
color magenta, trp_residues

# Display styles
show sticks, ligands
show sticks, binding_site

# Ray-traced rendering
ray 1600, 1200
png ./protein_visualization.png , dpi=300
