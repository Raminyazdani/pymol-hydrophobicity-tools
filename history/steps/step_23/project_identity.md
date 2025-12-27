# Project Identity: PyMOL Hydrophobicity Tools

## Professional Project Identity

### Display Title
**PyMOL Hydrophobicity Tools**

### Repository Slug
`pymol-hydrophobicity-tools`

### Tagline
Protein hydrophobicity analysis and visualization toolkit for PyMOL

### GitHub Description
A collection of Python scripts and PyMOL extensions for analyzing and visualizing protein hydrophobicity profiles using the Kyte-Doolittle scale. Includes tools for batch hydrophobicity calculation, smoothing analysis, and dynamic residue coloring in PyMOL.

### Primary Stack
- Python 3.x
- PyMOL
- BioPython
- Matplotlib
- NumPy

### Topics/Keywords
1. pymol
2. protein-analysis
3. hydrophobicity
4. kyte-doolittle
5. bioinformatics
6. structural-biology
7. protein-visualization
8. computational-biology
9. python
10. bioinformatics-tool

### Problem & Approach

**Problem Solved:**
Protein hydrophobicity is a crucial property in understanding protein structure, stability, and function. Analyzing hydrophobicity patterns helps identify membrane-spanning regions, buried hydrophobic cores, and surface-exposed residues. However, manual calculation and visualization of hydrophobicity profiles across protein structures can be tedious and error-prone.

**Approach:**
This toolkit provides three integrated tools:
1. **Automated PyMOL visualization** - Script for standardized protein structure visualization with ligand and binding site highlighting
2. **Hydrophobicity profiler** - Command-line tool to calculate and plot hydrophobicity profiles with configurable smoothing windows using the Kyte-Doolittle scale
3. **Interactive PyMOL extension** - Dynamic coloring of protein residues by hydrophobicity values directly in PyMOL, with customizable color palettes and smoothing

### Inputs & Outputs

**Inputs:**
- PDB structure files (from PDB database or local files)
- Protein chain selection (default: chain A)
- Smoothing window size (for averaging)
- PyMOL selection syntax (for extension)
- Color palette selection

**Outputs:**
- PNG visualization images of protein structures
- Hydrophobicity profile plots (line graphs)
- PyMOL sessions with hydrophobicity-colored residues
- Numerical hydrophobicity values per residue
