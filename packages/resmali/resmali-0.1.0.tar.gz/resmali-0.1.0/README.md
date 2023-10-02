# reSMALI
Scoring matrix-assisted ligand identification (SMALI) rewritten

A tool for predicting SH2 domain binding from peptide sequences with the format xx-Y-xxxx

The original SMALI was described in Huang H, Li L, Wu C, et al. Defining the specificity space of the human SRC homology 2 domain. Mol Cell Proteomics. 2008;7(4):768-784. doi:10.1074/mcp.M700312-MCP200 . However the tool is no longer hosted and is therefore no longer accessible. As the SMALI prediction tool was based on a experimental dataset, the loss of the tool represents the loss of a unique datapoint for making SH2 domain prediction. 

The complete OPAL array dataset upon which the original SMALI tool used was not published. However normalised intensinty values making up 20% or more of the total intensity for a given position within the peptide sequence was published. reSMALI uses this data to generage its own 'reSMALI' scores which are an attempt to emulate the scores provided by the original tool.

## Installing

```
pip install resmali
```

## Predict SH2 domain binding

To predict SH2 domain binding with a com

```python
predict_protein(protein_seq, sh2 = None, local_threshold='preset')
```

Where 'protein_seq' is your protein sequence. When 'sh2' is set to 'None', predictions will be made for all SH2 domains.

This function will return a list with the columns [positon, sequence, sh2motif, sh2_threshold, score ]

The local threshold is precalculated as the top 5% of scores for all valid phospho-tyrosines within the human proteome for that SH2 domain.

Note this function will only return SH2 domains where the reSMALI score is above the set local_threshold

To show the reSMALI scores for all valid phospo-tyrosine motifs and SH2 domains the  'local_threshold' can be set to '0' when using the predictProtein function. 

###Example

```python
import resmali
resmali.predict_protein("EEVVARyLNRNyWEkKQEEARyLN")

>>>[[6, 'ARYLNRN', 'GADS', 1.88, 2.0],
 [6, 'ARYLNRN', 'GRAP', 1.33, 2.96],
 [6, 'ARYLNRN', 'GRB2', 0.99, 1.73],
 [6, 'ARYLNRN', 'GRB7', 0.85, 0.98],
 [6, 'ARYLNRN', 'HSH2D', 0.73, 2.77],
 [6, 'ARYLNRN', 'SH2D2A', 1.72, 2.87],
 [6, 'ARYLNRN', 'SHE', 1.19, 1.2]]
```

## Just give me predictions

```
condensed_list(protein_seq, sh2 = None, local_threshold='preset')
```

This function will return a list with only SH2 domain predictions in the format '[Position, SH2 domain]'

###Example

```python
import resmali
resmali.condensed_list("EEVVARyLNRNyWEkKQEEARyLN")

>>>[[6, ['GADS', 'GRAP', 'GRB2', 'GRB7', 'HSH2D', 'SH2D2A', 'SHE']]]
 ```
