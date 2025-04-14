from pymol import cmd, stored


@cmd.extend
def hydrophobicity(selection="all", palette='blue_red', window=1, _self=cmd):
    """
        Function to compute hydrophobicity with window size

        Parameters
        ----------
        selection : str
            selected residues, default = "all"

        palette : pymol palette
            selected palette, default = "blue_red"

        window : int
            integer value of averaging window size

        Return
        ----------
        None

    """
    # check the window if it can convert to integer
    try:
        window = int(window)
    except:
        raise ValueError(f"window must be an integer not {window},type {type(window)}")
    # assertion of odd
    assert window % 2 == 1
    # check the pallete exist in pallete documentation : https://pymolwiki.org/index.php/Palette_Colorbars
    assert palette in ["blue_green", "blue_magenta", "blue_red", "blue_white_green", "blue_white_magenta", "rainbow",
                       "red_blue"]

    Kyte_Doolittle_scale = {'ALA': 1.8, 'ARG': -4.5, 'ASN': -3.5, 'ASP': -3.5, 'CYS': 2.5,
                            'GLN': -3.5, 'GLU': -3.5, 'GLY': -0.4, 'HIS': -3.2, 'ILE': 4.5,
                            'LEU': 3.8, 'LYS': -3.9, 'MET': 1.9, 'PHE': 2.8, 'PRO': -1.6,
                            'SER': -0.8, 'THR': -0.7, 'TRP': -0.9, 'TYR': -1.3, 'VAL': 4.2}

    # Color each residue in the PyMOL selection according to the Kyte-Doolittle hydrophobicity scale
    # The extension can be imported into PyMOL with: run hydrophobicity_pymol.py
    # Then launched with: hydrophobicity [, selection [, palette [, window]]]

    try:
        stored.items = []
        amino_acids = []
        cmd.select("selected", selection)
        cmd.iterate(selection="selected", expression="stored.items.append((resi,resn,name))")

        # extracting amino acids
        for s in stored.items:
            if s[2].strip() == "CA":
                if s[1] in Kyte_Doolittle_scale.keys():
                    amino_acids.append(s)
        stored.items = amino_acids
        hydrophobicity_values = [Kyte_Doolittle_scale.get(resn, 0) for resi, resn, name in stored.items]

        # create a halkf window to assign neighbor values
        smoothed_values = []
        half_window = window // 2
        for i in range(len(hydrophobicity_values)):
            # selecting neighboring residues before and after the residue according to the window size
            start = max(0, i - half_window)
            end = min(len(hydrophobicity_values), i + half_window + 1)

            # calculate the average hydrophobicity
            smoothed_values.append(sum(hydrophobicity_values[start:end]) / (end - start))
        # Assign smoothed hydrophobicity values to the B-factor field
        new_selection = []
        for i, (resi, _, _) in enumerate(stored.items):
            cmd.alter(f"{selection} and resi {resi}", f"b={smoothed_values[i]}")
            new_selection.append(resi)
        # Join the residue IDs into a valid PyMOL selection string
        residues_str = "+".join(map(str, new_selection))

        # Create a new selection using the updated residues
        cmd.select("modified", f"{selection} and resi {residues_str}")
        # Use spectrum to color based on hydrophobicity values
        cmd.spectrum("b", palette, selection="modified")
        cmd.deselect()
        print(f"Hydrophobicity-based coloring applied to residues in selection: {selection}")
    except Exception as e:
        print(e)
    finally:
        cmd.delete("modified")
        cmd.delete("selected")




