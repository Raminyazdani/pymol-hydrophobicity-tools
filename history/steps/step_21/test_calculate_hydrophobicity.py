import pytest
from calculate_hydrophobicity import get_residues, compute_hydrophobicity
import os
import matplotlib.pyplot as plt

# Sample PDB data for testing
pdb_content = """
ATOM      1  N   MET A   0      24.275   8.497  -9.497  1.00 57.77           N  
ATOM      2  CA  MET A   0      24.332   9.927  -9.719  1.00 40.14           C  
ATOM      3  C   MET A   0      25.697  10.317 -10.231  1.00 21.56           C  
ATOM      4  O   MET A   0      26.666   9.570 -10.094  1.00 38.27           O  
ATOM      5  CB  MET A   0      24.037  10.686  -8.435  1.00 47.29           C  
ATOM      6  CG  MET A   0      24.374   9.833  -7.230  1.00 49.95           C  
ATOM      7  SD  MET A   0      23.953  10.742  -5.746  1.00 50.67           S  
ATOM      8  CE  MET A   0      24.522  12.391  -6.243  1.00 28.11           C  
ATOM      9  N   VAL A   1      25.756  11.492 -10.833  1.00 26.35           N  
ATOM     10  CA  VAL A   1      26.989  11.962 -11.396  1.00 26.09           C  
ATOM     11  C   VAL A   1      27.194  13.441 -11.150  1.00 23.89           C  
ATOM     12  O   VAL A   1      26.342  14.253 -11.487  1.00 24.43           O  
ATOM     13  CB  VAL A   1      27.058  11.644 -12.886  1.00 36.78           C  
ATOM     14  CG1 VAL A   1      28.384  12.143 -13.436  1.00 34.03           C  
ATOM     15  CG2 VAL A   1      26.940  10.135 -13.111  1.00 37.22           C  
ATOM     16  N   LEU A   2      28.328  13.785 -10.556  1.00 13.67           N  
ATOM     17  CA  LEU A   2      28.630  15.176 -10.301  1.00 15.99           C  
ATOM     18  C   LEU A   2      29.248  15.823 -11.532  1.00 15.95           C  
ATOM     19  O   LEU A   2      29.953  15.207 -12.340  1.00 15.59           O  
ATOM     20  CB  LEU A   2      29.553  15.394  -9.079  1.00 11.52           C  
ATOM     21  CG  LEU A   2      28.830  15.496  -7.734  1.00 18.00           C  
ATOM     22  CD1 LEU A   2      28.409  14.098  -7.277  1.00 12.56           C  
ATOM     23  CD2 LEU A   2      29.770  16.127  -6.705  1.00 13.08           C  
ATOM     24  N   SER A   3      28.988  17.104 -11.665  1.00 10.19           N  
ATOM     25  CA  SER A   3      29.587  17.847 -12.750  1.00 15.52           C  
ATOM     26  C   SER A   3      30.977  18.340 -12.326  1.00 12.50           C  
ATOM     27  O   SER A   3      31.280  18.367 -11.141  1.00 10.25           O  
ATOM     28  CB  SER A   3      28.700  19.014 -13.108  1.00 19.54           C  
ATOM     29  OG  SER A   3      28.918  20.027 -12.150  1.00 15.48           O  
ATOM     30  N   GLU A   4      31.844  18.716 -13.267  1.00  9.27           N  
ATOM     31  CA  GLU A   4      33.175  19.166 -12.901  1.00 10.50           C  
ATOM     32  C   GLU A   4      33.113  20.385 -11.989  1.00 14.18           C  
ATOM     33  O   GLU A   4      33.940  20.594 -11.105  1.00 13.24           O  
ATOM     34  CB  GLU A   4      34.005  19.462 -14.166  1.00 11.71           C  
ATOM     35  CG  GLU A   4      35.395  20.045 -13.884  1.00 17.20           C  
ATOM     36  CD  GLU A   4      36.362  19.050 -13.303  1.00 26.49           C  
ATOM     37  OE1 GLU A   4      36.018  17.832 -13.282  1.00 28.47           O  
ATOM     38  OE2 GLU A   4      37.463  19.487 -12.842  1.00 30.24           O  
ATOM     39  N   GLY A   5      32.117  21.210 -12.255  1.00 13.03           N  
ATOM     40  CA  GLY A   5      31.874  22.424 -11.485  1.00 17.99           C  
ATOM     41  C   GLY A   5      31.589  22.130 -10.012  1.00 10.89           C  
ATOM     42  O   GLY A   5      32.099  22.818  -9.126  1.00  9.75           O  
ATOM     43  N   GLU A   6      30.775  21.096  -9.775  1.00 11.36           N  
ATOM     44  CA  GLU A   6      30.456  20.617  -8.452  1.00 10.19           C  
ATOM     45  C   GLU A   6      31.701  20.022  -7.798  1.00 13.85           C  
ATOM     46  O   GLU A   6      32.010  20.381  -6.670  1.00  9.43           O  
ATOM     47  CB  GLU A   6      29.277  19.631  -8.462  1.00 11.02           C  
ATOM     48  CG  GLU A   6      27.992  20.292  -8.988  1.00  8.50           C  
ATOM     49  CD  GLU A   6      26.894  19.331  -9.321  1.00 10.83           C  
ATOM     50  OE1 GLU A   6      27.177  18.181  -9.769  1.00 16.38           O  
ATOM     51  OE2 GLU A   6      25.732  19.722  -9.091  1.00 14.04           O  
ATOM     52  N   TRP A   7      32.471  19.197  -8.523  1.00  7.58           N  
ATOM     53  CA  TRP A   7      33.703  18.659  -7.963  1.00  6.37           C  
ATOM     54  C   TRP A   7      34.631  19.774  -7.503  1.00  9.94           C  
ATOM     55  O   TRP A   7      35.269  19.698  -6.460  1.00  9.99           O  
ATOM     56  CB  TRP A   7      34.438  17.705  -8.935  1.00  5.86           C  
ATOM     57  CG  TRP A   7      33.767  16.373  -8.979  1.00 10.70           C  
ATOM     58  CD1 TRP A   7      33.183  15.769 -10.050  1.00  9.24           C  
ATOM     59  CD2 TRP A   7      33.594  15.506  -7.867  1.00  7.85           C  
ATOM     60  NE1 TRP A   7      32.697  14.542  -9.688  1.00  6.35           N  
ATOM     61  CE2 TRP A   7      32.891  14.376  -8.337  1.00 10.62           C  
ATOM     62  CE3 TRP A   7      33.978  15.602  -6.528  1.00  6.55           C  
ATOM     63  CZ2 TRP A   7      32.549  13.332  -7.474  1.00 11.33           C  
ATOM     64  CZ3 TRP A   7      33.630  14.581  -5.681  1.00 12.71           C  
ATOM     65  CH2 TRP A   7      32.954  13.447  -6.159  1.00 10.61           C  
ATOM     66  N   GLN A   8      34.765  20.803  -8.333  1.00  8.13           N  
ATOM     67  CA  GLN A   8      35.642  21.916  -8.033  1.00  7.29           C  
ATOM     68  C   GLN A   8      35.251  22.602  -6.730  1.00 10.26           C  
ATOM     69  O   GLN A   8      36.082  23.014  -5.928  1.00 12.04           O  
ATOM     70  CB  GLN A   8      35.585  22.967  -9.154  1.00 14.97           C  
ATOM     71  CG  GLN A   8      36.361  22.629 -10.442  1.00 19.54           C  
ATOM     72  CD  GLN A   8      36.380  23.830 -11.366  1.00 65.38           C  
ATOM     73  OE1 GLN A   8      37.441  24.373 -11.680  1.00 80.00           O  
ATOM     74  NE2 GLN A   8      35.178  24.309 -11.733  1.00 80.00           N  
ATOM     75  N   LEU A   9      33.957  22.760  -6.526  1.00  8.91           N  
ATOM     76  CA  LEU A   9      33.487  23.363  -5.288  1.00 11.29           C  
ATOM     77  C   LEU A   9      33.854  22.500  -4.059  1.00 11.69           C  
ATOM     78  O   LEU A   9      34.179  23.015  -2.982  1.00  9.37           O  
ATOM     79  CB  LEU A   9      31.964  23.613  -5.342  1.00  9.01           C  
ATOM     80  CG  LEU A   9      31.544  24.742  -6.278  1.00 19.22           C  
ATOM     81  CD1 LEU A   9      30.060  24.638  -6.599  1.00 12.77           C  
ATOM     82  CD2 LEU A   9      31.808  26.076  -5.601  1.00 16.45           C  
ATOM     83  N   VAL A  10      33.757  21.183  -4.231  1.00  6.28           N  
ATOM     84  CA  VAL A  10      34.073  20.228  -3.184  1.00  4.53           C  
ATOM     85  C   VAL A  10      35.549  20.287  -2.910  1.00  7.54           C  
ATOM     86  O   VAL A  10      35.970  20.460  -1.782  1.00  7.48           O  
ATOM     87  CB  VAL A  10      33.648  18.797  -3.543  1.00  8.07           C  
ATOM     88  CG1 VAL A  10      34.283  17.721  -2.644  1.00  5.30           C  
ATOM     89  CG2 VAL A  10      32.130  18.697  -3.515  1.00  8.42           C  
ATOM     90  N   LEU A  11      36.338  20.200  -3.970  1.00  8.63           N  
ATOM     91  CA  LEU A  11      37.769  20.165  -3.811  1.00  6.65           C  
ATOM     92  C   LEU A  11      38.354  21.451  -3.273  1.00  8.56           C  
ATOM     93  O   LEU A  11      39.340  21.463  -2.544  1.00  8.84           O  
ATOM     94  CB  LEU A  11      38.472  19.592  -5.047  1.00  9.81           C  
ATOM     95  CG  LEU A  11      38.013  18.159  -5.288  1.00 10.40           C  
ATOM     96  CD1 LEU A  11      38.656  17.600  -6.552  1.00 14.15           C  
ATOM     97  CD2 LEU A  11      38.331  17.291  -4.074  1.00 12.47           C  
ATOM     98  N   HIS A  12      37.691  22.538  -3.597  1.00  8.79           N  
ATOM     99  CA  HIS A  12      38.103  23.834  -3.130  1.00  8.68           C  
ATOM    100  C   HIS A  12      37.908  23.989  -1.629  1.00  9.13           C  
ATOM    101  O   HIS A  12      38.803  24.458  -0.942  1.00 11.19           O  
ATOM    102  CB  HIS A  12      37.424  24.934  -3.940  1.00  7.47           C  
ATOM    103  CG  HIS A  12      37.822  26.290  -3.509  1.00 22.37           C  
ATOM    104  ND1 HIS A  12      39.022  26.863  -3.920  1.00 36.54           N  
ATOM    105  CD2 HIS A  12      37.165  27.185  -2.733  1.00 22.35           C  
ATOM    106  CE1 HIS A  12      39.069  28.080  -3.389  1.00 19.42           C  
ATOM    107  NE2 HIS A  12      37.971  28.303  -2.663  1.00 26.26           N  
ATOM    108  N   VAL A  13      36.779  23.565  -1.063  1.00  8.94           N  
ATOM    109  CA  VAL A  13      36.692  23.645   0.388  1.00 11.31           C  
ATOM    110  C   VAL A  13      37.613  22.613   1.034  1.00  9.92           C  
ATOM    111  O   VAL A  13      38.190  22.850   2.091  1.00  6.44           O  
ATOM    112  CB  VAL A  13      35.319  23.316   0.961  1.00 18.81           C  
ATOM    113  CG1 VAL A  13      34.836  24.349   1.964  1.00 17.71           C  
ATOM    114  CG2 VAL A  13      34.292  22.928  -0.083  1.00 21.50           C  
ATOM    115  N   TRP A  14      37.668  21.410   0.449  1.00  6.19           N  
ATOM    116  CA  TRP A  14      38.517  20.354   0.983  1.00  7.03           C  
ATOM    117  C   TRP A  14      39.978  20.791   1.191  1.00  9.39           C  
ATOM    118  O   TRP A  14      40.651  20.408   2.159  1.00  9.35           O  
ATOM    119  CB  TRP A  14      38.447  19.088   0.129  1.00  4.00           C  
ATOM    120  CG  TRP A  14      38.904  17.929   0.943  1.00  9.15           C  
ATOM    121  CD1 TRP A  14      40.090  17.301   0.872  1.00 10.42           C  
ATOM    122  CD2 TRP A  14      38.184  17.339   2.023  1.00 11.09           C  
ATOM    123  NE1 TRP A  14      40.143  16.328   1.839  1.00  7.96           N  
ATOM    124  CE2 TRP A  14      38.995  16.337   2.566  1.00  6.95           C  
ATOM    125  CE3 TRP A  14      36.968  17.640   2.621  1.00  9.17           C  
ATOM    126  CZ2 TRP A  14      38.573  15.552   3.635  1.00 14.62           C  
ATOM    127  CZ3 TRP A  14      36.549  16.878   3.680  1.00 14.80           C  
ATOM    128  CH2 TRP A  14      37.354  15.855   4.190  1.00 14.72           C  
ATOM    129  N   ALA A  15      40.493  21.585   0.245  1.00  8.54           N  
ATOM    130  CA  ALA A  15      41.845  22.094   0.311  1.00  6.22           C  
ATOM    131  C   ALA A  15      42.051  22.901   1.592  1.00  9.04           C  
ATOM    132  O   ALA A  15      43.121  22.864   2.199  1.00  8.44           O  
ATOM    133  CB  ALA A  15      42.189  22.888  -0.940  1.00  7.57           C  
ATOM    134  N   LYS A  16      40.992  23.576   2.054  1.00 11.41           N  
ATOM    135  CA  LYS A  16      41.047  24.330   3.303  1.00  6.63           C  
ATOM    136  C   LYS A  16      41.010  23.387   4.487  1.00  9.64           C  
ATOM    137  O   LYS A  16      41.701  23.612   5.476  1.00 11.79           O  
ATOM    138  CB  LYS A  16      39.961  25.378   3.469  1.00  9.27           C  
ATOM    139  CG  LYS A  16      39.784  26.263   2.251  1.00  8.79           C  
ATOM    140  CD  LYS A  16      41.091  26.906   1.843  1.00 14.12           C  
ATOM    141  CE  LYS A  16      40.924  28.094   0.911  1.00 28.13           C  
ATOM    142  NZ  LYS A  16      42.177  28.438   0.218  1.00 25.12           N  
ATOM    143  N   VAL A  17      40.214  22.325   4.380  1.00  4.67           N  
ATOM    144  CA  VAL A  17      40.214  21.332   5.418  1.00  7.09           C  
ATOM    145  C   VAL A  17      41.621  20.766   5.589  1.00  7.14           C  
ATOM    146  O   VAL A  17      42.069  20.539   6.711  1.00  5.93           O  
ATOM    147  CB  VAL A  17      39.244  20.232   5.025  1.00  4.76           C  
ATOM    148  CG1 VAL A  17      39.267  19.029   5.968  1.00  4.58           C  
ATOM    149  CG2 VAL A  17      37.848  20.826   4.962  1.00  9.86           C  
ATOM    150  N   GLU A  18      42.309  20.485   4.470  1.00  5.48           N  
ATOM    151  CA  GLU A  18      43.655  19.918   4.475  1.00  6.24           C  
ATOM    152  C   GLU A  18      44.718  20.757   5.178  1.00  9.13           C  
ATOM    153  O   GLU A  18      45.764  20.242   5.555  1.00  7.99           O  
ATOM    154  CB  GLU A  18      44.095  19.528   3.070  1.00  9.01           C  
ATOM    155  CG  GLU A  18      43.189  18.415   2.530  1.00 13.75           C  
ATOM    156  CD  GLU A  18      43.777  17.765   1.324  1.00 10.41           C  
ATOM    157  OE1 GLU A  18      44.450  18.483   0.529  1.00 23.27           O  
ATOM    158  OE2 GLU A  18      43.544  16.543   1.163  1.00 16.46           O  
ATOM    159  N   ALA A  19      44.450  22.037   5.388  1.00  7.61           N  
ATOM    160  CA  ALA A  19      45.377  22.859   6.140  1.00  9.33           C  
ATOM    161  C   ALA A  19      45.437  22.391   7.583  1.00 10.12           C  
ATOM    162  O   ALA A  19      46.388  22.695   8.287  1.00 12.03           O  
ATOM    163  CB  ALA A  19      44.958  24.323   6.161  1.00  4.81           C  
ATOM    164  N   ASP A  20      44.401  21.695   8.068  1.00  6.81           N  
ATOM    165  CA  ASP A  20      44.413  21.254   9.459  1.00  7.78           C  
ATOM    166  C   ASP A  20      43.624  19.966   9.627  1.00  6.81           C  
ATOM    167  O   ASP A  20      42.511  19.963  10.163  1.00  8.30           O  
ATOM    168  CB  ASP A  20      43.824  22.356  10.372  1.00  9.66           C  
ATOM    169  CG  ASP A  20      43.633  21.927  11.805  1.00 21.03           C  
ATOM    170  OD1 ASP A  20      44.372  21.000  12.249  1.00 12.36           O  
ATOM    171  OD2 ASP A  20      42.756  22.526  12.496  1.00 21.17           O
"""

@pytest.fixture
def create_pdb_file(tmp_path):
    pdb_file = tmp_path / "test.pdb"
    pdb_file.write_text(pdb_content)
    return pdb_file

def test_get_residues(create_pdb_file):
    pdb_file = create_pdb_file
    residues = get_residues(str(pdb_file))
    print(residues)
    assert residues == ['MET', 'VAL', 'LEU', 'SER', 'GLU', 'GLY', 'GLU', 'TRP', 'GLN', 'LEU', 'VAL', 'LEU', 'HIS', 'VAL', 'TRP', 'ALA', 'LYS', 'VAL', 'GLU', 'ALA', 'ASP']

def test_compute_hydrophobicity(create_pdb_file, tmp_path):
    pdb_file = create_pdb_file
    residues = get_residues(str(pdb_file))
    hydrophobicity = compute_hydrophobicity(residues, 2)
    assert hydrophobicity == 1