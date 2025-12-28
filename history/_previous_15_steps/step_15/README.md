# PyMOL Hydrophobicity Tools

> Protein hydrophobicity analysis and visualization toolkit for PyMOL

A collection of Python scripts and PyMOL extensions for analyzing and visualizing protein hydrophobicity profiles using the Kyte-Doolittle scale. This toolkit enables batch hydrophobicity calculation, smoothing analysis with configurable window sizes, and dynamic residue coloring directly in PyMOL.

## What It Does

This toolkit provides three complementary tools for protein hydrophobicity analysis:

1. **Automated PyMOL Visualization Script** (`visualize_protein.pml`) - Standardized protein structure visualization with automatic ligand detection, binding site highlighting, and residue-specific coloring
2. **Hydrophobicity Profiler** (`calculate_hydrophobicity.py`) - Command-line tool to calculate and plot hydrophobicity profiles with configurable smoothing windows
3. **Interactive PyMOL Extension** (`hydrophobicity_pymol.py`) - Dynamic coloring of protein residues by hydrophobicity values directly in PyMOL with customizable palettes and smoothing

## Problem & Approach

Protein hydrophobicity is crucial for understanding protein structure, stability, and function. Analyzing hydrophobicity patterns helps identify:
- Membrane-spanning regions
- Buried hydrophobic cores
- Surface-exposed residues
- Protein folding patterns

This toolkit automates the calculation and visualization process using the well-established **Kyte-Doolittle hydrophobicity scale**, providing both command-line and interactive PyMOL-based workflows.

## Tech Stack

- **Python 3.x**
- **PyMOL** (for molecular visualization)
- **BioPython** >= 1.79 (PDB file parsing)
- **Matplotlib** >= 3.3.0 (plotting)
- **NumPy** >= 1.21.0 (numerical operations)

## Repository Structure

```
.
├── calculate_hydrophobicity.py      # Command-line hydrophobicity calculator
├── hydrophobicity_pymol.py          # PyMOL extension (complete implementation)
├── hydrophobicity_pymol_template.py # PyMOL extension (template version)
├── visualize_protein.pml            # PyMOL visualization script
├── test_calculate_hydrophobicity.py # Unit tests
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Setup

### Prerequisites

1. **PyMOL** must be installed separately. Options:
   - PyMOL Open Source: `conda install -c conda-forge pymol-open-source`
   - Commercial PyMOL: https://pymol.org/

2. **Python 3.x** with pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Raminyazdani/pymol-hydrophobicity-tools.git
cd pymol-hydrophobicity-tools

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### 1. PyMOL Visualization Script

Automatically visualizes protein structures with standardized styling:

```bash
# Launch in PyMOL
pymol visualize_protein.pml

# Or from within PyMOL
PyMOL> run visualize_protein.pml
```

**What it does:**
- Fetches protein structure from PDB (default: 4UC1)
- Removes water molecules
- Colors ligands cyan
- Highlights binding sites (within 5Å of ligands) in grey
- Colors tryptophan residues magenta
- Represents ligands and binding sites as sticks
- Exports result as `protein_visualization.png`

**Customization:** Edit the PDB ID on line 2 of `visualize_protein.pml`

### 2. Command-Line Hydrophobicity Calculator

Calculate and plot hydrophobicity profiles from PDB files:

```bash
# Basic usage
python calculate_hydrophobicity.py <pdb_file>

# Example with a local PDB file
python calculate_hydrophobicity.py protein.pdb

# Customize output filename prefix (optional)
export HYDROPHOBICITY_OUTPUT_PREFIX=myprotein
python calculate_hydrophobicity.py protein.pdb
```

**Outputs:**
- `hydrophobicity_plot_window5.png` - Hydrophobicity plot with window size 5
- `hydrophobicity_plot_window7.png` - Hydrophobicity plot with window size 7
- `hydrophobicity_plot_window9.png` - Hydrophobicity plot with window size 9

The script analyzes **chain A** only and uses CA (alpha carbon) atoms for residue identification.

### 3. PyMOL Interactive Extension

Color protein residues by hydrophobicity directly in PyMOL:

```bash
# Launch PyMOL
pymol

# Inside PyMOL, load the extension
PyMOL> run hydrophobicity_pymol.py

# Load a protein structure
PyMOL> fetch 1ubq

# Apply hydrophobicity coloring
PyMOL> hydrophobicity

# With custom selection and palette
PyMOL> hydrophobicity chain A, blue_white_magenta

# With smoothing window (must be odd number)
PyMOL> hydrophobicity chain A, blue_red, 3
```

**Parameters:**
- `selection` (optional, default: "all") - PyMOL selection syntax
- `palette` (optional, default: "blue_red") - Color palette:
  - `blue_green`, `blue_magenta`, `blue_red`, `blue_white_green`, `blue_white_magenta`, `rainbow`, `red_blue`
- `window` (optional, default: 1) - Smoothing window size (must be odd number)

**Color mapping:**
- Blue/cool colors: Hydrophilic residues (negative Kyte-Doolittle values)
- Red/warm colors: Hydrophobic residues (positive Kyte-Doolittle values)

## Data Requirements

### Input Format

**PDB Files:** Standard Protein Data Bank format files

**Obtaining PDB files:**
1. Download from RCSB PDB: https://www.rcsb.org/
2. Use PyMOL's `fetch` command (e.g., `fetch 1ubq`)
3. Use your own experimental structures

**Expected structure:**
- ATOM records with chain identifiers
- CA (alpha carbon) atoms for each residue
- Standard 3-letter amino acid codes

### Supported Amino Acids

The Kyte-Doolittle scale covers all 20 standard amino acids:
- Hydrophobic: ILE (4.5), VAL (4.2), LEU (3.8), PHE (2.8), CYS (2.5), MET (1.9), ALA (1.8)
- Neutral: GLY (-0.4), THR (-0.7), SER (-0.8), TRP (-0.9), TYR (-1.3), PRO (-1.6)
- Hydrophilic: HIS (-3.2), GLN (-3.5), ASN (-3.5), GLU (-3.5), ASP (-3.5), LYS (-3.9), ARG (-4.5)

## Output Descriptions

### Visualization Outputs
- **`protein_visualization.png`** - Rendered PyMOL scene with ligands, binding sites, and colored residues

### Hydrophobicity Plots
- **Line graphs** showing hydrophobicity values across amino acid positions
- **X-axis:** Amino acid position in sequence
- **Y-axis:** Averaged Kyte-Doolittle hydrophobicity value
- **Smoothing:** Values averaged using sliding window approach

### PyMOL Sessions
- Protein residues colored by hydrophobicity (stored in B-factor field)
- Interactive: rotate, zoom, and inspect specific residues
- Export as PyMOL session (`.pse`) or images as needed

## Reproducibility Notes

### Environment
- Tested with Python 3.8+
- BioPython 1.79+, Matplotlib 3.3.0+, NumPy 1.21.0+
- PyMOL 2.x (open-source or commercial)

### Algorithm Details
- **Kyte-Doolittle Scale:** Standard hydrophobicity scale from Kyte & Doolittle (1982)
- **Smoothing:** Sliding window average (configurable window size, must be odd)
- **Residue Selection:** Only CA atoms from chain A (for `calculate_hydrophobicity.py`)
- **Missing Residues:** Non-standard residues are filtered out

### Deterministic Behavior
- Results are deterministic (no randomization)
- Output depends only on input PDB structure and window size
- Color mapping is fixed per the Kyte-Doolittle scale

## Testing

Run the test suite:

```bash
# Install pytest if needed
pip install pytest

# Run tests
pytest test_calculate_hydrophobicity.py -v
```

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'Bio'`
- **Solution:** Install BioPython: `pip install biopython>=1.79`

**Issue:** `command not found: pymol`
- **Solution:** PyMOL must be installed separately. Use conda or download from pymol.org

**Issue:** `AssertionError` when using even window size
- **Solution:** Window size must be an odd number (1, 3, 5, 7, 9, etc.)

**Issue:** No output plots generated
- **Solution:** Ensure the PDB file path is correct and contains chain A with standard amino acids

**Issue:** PyMOL extension not working
- **Solution:** Verify you ran `run hydrophobicity_pymol.py` from within PyMOL (not from terminal)

**Issue:** Plot shows very few data points
- **Solution:** Check that your PDB file contains chain A. Modify line 136 in `calculate_hydrophobicity.py` to use a different chain if needed.

### Getting Help

- Check the code comments for implementation details
- Review the Kyte-Doolittle scale reference: https://web.expasy.org/protscale/
- PyMOL Wiki: https://pymolwiki.org/

## References

- Kyte, J., & Doolittle, R. F. (1982). A simple method for displaying the hydropathic character of a protein. *Journal of Molecular Biology*, 157(1), 105-132.
- Kyte-Doolittle Scale: https://web.expasy.org/protscale/
- PyMOL: https://pymol.org/

## License

This project is available for educational and research purposes. See repository for license details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
