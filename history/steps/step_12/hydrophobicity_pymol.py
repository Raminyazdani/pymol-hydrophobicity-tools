#!/usr/bin/env python3
"""
PyMOL extension for coloring protein residues by hydrophobicity.
"""
from pymol import cmd
# FIXED: Correct module name
from calculate_hydrophobicity import get_residues


# Kyte-Doolittle hydrophobicity scale
HYDROPHOBICITY_SCALE = {
    'ILE': 4.5, 'VAL': 4.2, 'LEU': 3.8, 'PHE': 2.8, 'CYS': 2.5,
    'MET': 1.9, 'ALA': 1.8, 'GLY': -0.4, 'THR': -0.7, 'SER': -0.8,
    'TRP': -0.9, 'TYR': -1.3, 'PRO': -1.6, 'HIS': -3.2, 'GLN': -3.5,
    'ASN': -3.5, 'GLU': -3.5, 'ASP': -3.5, 'LYS': -3.9, 'ARG': -4.5
}


# Color palettes
COLOR_PALETTES = {
    'blue_red': ['blue', 'red'],
    'blue_green': ['blue', 'green'],
    'rainbow': ['blue', 'cyan', 'green', 'yellow', 'orange', 'red']
}


def hydrophobicity(selection='all', palette='blue_red', window=1):
    """Color residues by hydrophobicity values.
    
    Args:
        selection: PyMOL selection (default: 'all')
        palette: Color palette name (default: 'blue_red')
        window: Smoothing window size (default: 1, must be odd)
    """
    print(f"Applying hydrophobicity coloring to {selection}")
    print(f"Palette: {palette}, Window: {window}")
    
    # Basic skeleton - full implementation coming next


# Register with PyMOL
cmd.extend('hydrophobicity', hydrophobicity)
