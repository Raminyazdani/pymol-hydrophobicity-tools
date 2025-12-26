#!/usr/bin/env python3
"""
Utility for parsing PDB files and analyzing protein hydrophobicity.
"""
import os
import sys
from Bio import PDB



# Kyte-Doolittle hydrophobicity scale
HYDROPHOBICITY_SCALE = {
    'ILE': 4.5, 'VAL': 4.2, 'LEU': 3.8, 'PHE': 2.8, 'CYS': 2.5,
    'MET': 1.9, 'ALA': 1.8, 'GLY': -0.4, 'THR': -0.7, 'SER': -0.8,
    'TRP': -0.9, 'TYR': -1.3, 'PRO': -1.6, 'HIS': -3.2, 'GLN': -3.5,
    'ASN': -3.5, 'GLU': -3.5, 'ASP': -3.5, 'LYS': -3.9, 'ARG': -4.5
}

class RaminCalc:
    """Utility class for PDB file operations."""
    
    def __init__(self, filename):
        """Initialize with PDB filename.
        
        Args:
            filename: Path to PDB file
        """
        self.filename = filename
        self.structure = None
        
    def read_pdb(self):
        """Parse the PDB file and return structure object.
        
        Returns:
            Bio.PDB.Structure: Parsed protein structure
        """
        parser = PDB.PDBParser(QUIET=True)
        self.structure = parser.get_structure('protein', self.filename)
        return self.structure
    
    def get_chain(self, chain_id='A'):
        """Extract a specific chain from the structure.
        
        Args:
            chain_id: Chain identifier (default: 'A')
            
        Returns:
            Bio.PDB.Chain: The requested chain
        """
        if self.structure is None:
            self.read_pdb()
        
        for model in self.structure:
            for chain in model:
                if chain.id == chain_id:
                    return chain
        return None


def get_residues(pdb_file):
    """Extract amino acid residues from PDB file.
    
    Args:
        pdb_file: Path to PDB file
        
    Returns:
        list: Three-letter amino acid codes
    """
    calc = RaminCalc(pdb_file)
    chain = calc.get_chain('A')
    
    if chain is None:
        return []
    
    residues = []
    for residue in chain:
        if residue.get_id()[0] == ' ':  # Standard amino acid
            if 'CA' in residue:  # Has alpha carbon
                residues.append(residue.get_resname())
    
    return residues


def compute_hydrophobicity(residues, window_size):
    """Calculate hydrophobicity values with sliding window averaging.
    
    Args:
        residues: List of three-letter amino acid codes
        window_size: Size of smoothing window (must be odd)
        
    Returns:
        list: Smoothed hydrophobicity values
    """
    # Map residues to hydrophobicity values
    values = []
    for res in residues:
        if res in HYDROPHOBICITY_SCALE:
            values.append(HYDROPHOBICITY_SCALE[res])
    
    # Apply sliding window average
    smoothed = []
    half_window = window_size // 2
    
    for i in range(len(values)):
        start = max(0, i - half_window)
        end = min(len(values), i + half_window + 1)
        window = values[start:end]
        avg = sum(window) / len(window)
        smoothed.append(avg)
    
    return smoothed



# Default prefix for output files
OUTPUT_PREFIX = os.environ.get('HYDROPHOBICITY_OUTPUT_PREFIX', 'hydrophobicity')


if __name__ == '__main__':
    # BUG: No validation of sys.argv length
    pdb_file = sys.argv[1]  # This will crash if no arguments provided!
    
    # Get residues
    residues = get_residues(pdb_file)
    
    # Calculate hydrophobicity
    hydro_values = compute_hydrophobicity(residues, 5)
    
    print(f"Analyzed {len(residues)} residues")
    print(f"Hydrophobicity range: {min(hydro_values):.2f} to {max(hydro_values):.2f}")
