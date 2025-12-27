#!/usr/bin/env python3
"""
Utility for parsing PDB files and analyzing protein hydrophobicity.
"""
import os
import sys
from Bio import PDB


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
