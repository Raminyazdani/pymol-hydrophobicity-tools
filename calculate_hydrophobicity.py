import sys
import matplotlib.pyplot as plt
import os


class RaminCalc:
    # Base self designed Class for implementing statics method for extracting relevant data from PDB lines

    @staticmethod
    def get_data_pdb(pdb_line, items=None):
        # this function get a single pdb_line and the items is not mandatory
        # if items is None or not given it will return all the data according to the pdb file format documentation

        # this is template for key values stores in each pdb line ATOM and HETATM
        template_columns = {
            "Type": pdb_line[0:6].strip(),
            "Atom serial number": pdb_line[6:11].strip(),
            "Atom name": pdb_line[12:16].strip(),
            "Alternate location indicator": pdb_line[16].strip(),
            "Residue name": pdb_line[17:20].strip(),
            "Chain identifier": pdb_line[21].strip(),
            "Residue sequence number": pdb_line[22:26].strip(),
            "Code for insertions of residues": pdb_line[26].strip(),
            "X orthogonal Å coordinate": pdb_line[30:38].strip(),
            "Y orthogonal Å coordinate": pdb_line[38:46].strip(),
            "Z orthogonal Å coordinate": pdb_line[46:54].strip(),
            "Occupancy": pdb_line[54:60].strip(),
            "Temperature factor": pdb_line[60:66].strip(),
            "Segment identifier": pdb_line[72:76].strip(),
            "Element symbol": pdb_line[76:78].strip(),
            "Charge": pdb_line[78:80].strip(),
        }

        # return all extracted data from line
        if items is None:
            return template_columns

        # if items given to function it returns the desired items only in format of dictionary
        return_temp = {}
        for item in items:
            if item in template_columns.keys():
                return_temp[item] = template_columns[item]
        return return_temp

    @staticmethod
    def get_custom_data_pdb(pdb_line, template_get, simple=False):

        # get custom template design in arguments and accordingly extract the data from the pdb_line
        result_temp = "{"
        for key, value in template_get.items():
            result_temp += "'" + key + "'" + ":pdb_line" + str(value) + ",\n"
        result_temp += "}"

        # for one time evaluating , the result temp is string formated command for creating a dictionary
        result_temp = eval(result_temp)

        # if simple argument TRUE given to the function , instead of returning the dictionary it will only return the data value extracted
        # if there are multiple items in template to get from pdb lines , it will not return single data
        if simple == True and len(result_temp.items()) == 1:
            return list(result_temp.values())[0]
        return result_temp

    @staticmethod
    def get_template_pdb(items):

        # this is a function to generate a string template only for get_custom_data_pdb staticmethod for further eval() inside that function
        # it gets a list of items and returns the dictionary converted to key,value format of the pdb line docs
        template_columns = {
            "Type": "[0:6].strip()",
            "Atom serial number": "[6:11].strip()",
            "Atom name": "[12:16].strip()",
            "Alternate location indicator": "[16].strip()",
            "Residue name": "[17:20]",
            "Chain identifier": "[21].strip()",
            "Residue sequence number": "[22:26].strip()",
            "Code for insertions of residues": "[26].strip()",
            "X orthogonal Å coordinate": "[30:38].strip()",
            "Y orthogonal Å coordinate": "[38:46].strip()",
            "Z orthogonal Å coordinate": "[46:54].strip()",
            "Occupancy": "[54:60].strip()",
            "Temperature factor": "[60:66].strip()",
            "Segment identifier": "[72:76].strip()",
            "Element symbol": "[76:78].strip()",
            "Charge": "[78:80].strip()",
        }
        return_temp = {}
        for item in items:
            if item in template_columns.keys():
                return_temp[item] = template_columns[item]
        return return_temp


# Default prefix for output files (can be overridden via environment variable)
OUTPUT_PREFIX = os.environ.get('HYDROPHOBICITY_OUTPUT_PREFIX', 'hydrophobicity')


def get_residues(pdb_file):
    """
        Function to read PDB files

        Parameters
        ----------
        pdb_file : str
            path to pdb file

        Return
        ----------
        residues : list
            list of amino acid residues 3-letter code ex: ["ARG", "TRP", "LYS"]

    """

    residues = []

    # Read PDB file and extract amino acid residues from chain A
    # Filter for CA (alpha carbon) atoms to get one entry per residue

    # read the file with context manager "with"
    with open(pdb_file, "r") as f:
        # only stores non empty lines
        lines = [x for x in f.read().split("\n") if x.strip() != ""]

    # define keys that we want from each line
    needed_cols_temp = ["Residue name", "Residue sequence number", "Chain identifier", "Atom name"]
    # get the template
    temp_template = RaminCalc.get_template_pdb(needed_cols_temp)
    Kyte_Doolittle_scale = {'ALA': 1.8, 'ARG': -4.5, 'ASN': -3.5, 'ASP': -3.5, 'CYS': 2.5,
                            'GLN': -3.5, 'GLU': -3.5, 'GLY': -0.4, 'HIS': -3.2, 'ILE': 4.5,
                            'LEU': 3.8, 'LYS': -3.9, 'MET': 1.9, 'PHE': 2.8, 'PRO': -1.6,
                            'SER': -0.8, 'THR': -0.7, 'TRP': -0.9, 'TYR': -1.3, 'VAL': 4.2}
    # iterate over each line and get the relevant data from it
    for l in lines:
        data = RaminCalc.get_custom_data_pdb(l, temp_template)
        if data["Atom name"] == "CA" and data["Chain identifier"]=="A":
            if data["Residue name"] not in Kyte_Doolittle_scale.keys():
                continue
            # first adding to residues
            if len(residues) == 0:
                residues.append(data)
                continue
            if residues[-1] != data:
                residues.append(data)
    # remove unwanted data from residue list items
    residues = [x["Residue name"] for x in residues]

    return residues


def compute_hydrophobicity(residues, window_size):
    """
        Function to compute hydrophobicity with window size

        Parameters
        ----------
        residues : list
            list of amino acid residues 3-letter code ex: ["ARG", "TRP", "LYS"]

        window_size : int
            integer value of window size

        Return
        ----------
        None

    """

    Kyte_Doolittle_scale = {'ALA': 1.8, 'ARG': -4.5, 'ASN': -3.5, 'ASP': -3.5, 'CYS': 2.5,
                            'GLN': -3.5, 'GLU': -3.5, 'GLY': -0.4, 'HIS': -3.2, 'ILE': 4.5,
                            'LEU': 3.8, 'LYS': -3.9, 'MET': 1.9, 'PHE': 2.8, 'PRO': -1.6,
                            'SER': -0.8, 'THR': -0.7, 'TRP': -0.9, 'TYR': -1.3, 'VAL': 4.2}

    average_values = []
    # create a new list of residues but instead of residue name we put Kyhte doolittle scale values for each residue in original order
    hydrophobicity_values = [Kyte_Doolittle_scale[x] for x in residues]

    # window size re declaration
    window_size = 3

    # creating window with iteration and calculate the average value and append to average value list
    for i in range(len(residues) - window_size + 1):
        window = hydrophobicity_values[i:i + window_size]
        average_values.append(sum(window) / window_size)
    
    # Calculate average hydrophobicity values using sliding window approach
    # Reference: https://resources.qiagenbioinformatics.com/manuals/clcgenomicsworkbench/2305/index.php?manual=BE_Protein_hydrophobicity.html
    # Reference: https://web.expasy.org/protscale/
    plt.plot(average_values)
    plt.xlabel("AA position")
    plt.ylabel("Hydrophobicity")
    plt.savefig(f"./{OUTPUT_PREFIX}_plot_window{window_size}.png")
    plt.clf()


# Main entry point
if __name__ == "__main__":
    # OOPS: Forgot to check argv length, will cause IndexError if no arguments
    residues = get_residues(sys.argv[1])
    print(f"Length of residues: {len(residues)}")
    window_sizes = [5, 9]
    for window_size in window_sizes:
        compute_hydrophobicity(residues, window_size)
        plt.clf()

    for window_size in [3, 7]:
        compute_hydrophobicity(residues, window_size)
    os.remove(f"./{OUTPUT_PREFIX}_plot_window3.png")

