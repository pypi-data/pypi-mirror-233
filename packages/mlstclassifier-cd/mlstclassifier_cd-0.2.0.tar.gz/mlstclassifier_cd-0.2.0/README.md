# MLSTclassifier_cd

## Table of Contents

- [Overview](#overview)

- [Installation](#installation)

- [Usage](#usage)

- [Output](#output)

## Overview

Enhance your clade prediction process with MLSTclassifier_cd, a powerful machine learning tool that employs K-Nearest Neighbors (KNN) algorithm. Designed specifically for Multi-Locus Sequence Type (MLST) analysis of _C.difficile_ strains, including cryptic variants, this tool streamlines and accelerates clade prediction. MLSTclassifier_cd achieves accuracy of approximately 92% for predictions.

StatQuest methodology was used to build the model (https://www.youtube.com/watch?v=q90UDEgYqeI&t=3327s). Powered by the Scikit-learn library, MLSTclassifier_cd is a good tool to have a first classification of your _C.difficile_ strains including cryptic ones.

The model was trained using data from PubMLST (May 2023): https://pubmlst.org/bigsdb?db=pubmlst_cdifficile_seqdef&page=downloadProfiles&scheme_id=1. Cryptic strains for training were assessed manually using phylogenetic tree construction, fastbaps and popPUNK to refine clustering.

GitHub repo: https://github.com/eliottBo/MLSTclassifier_cd

## Installation:

It is recommended to use a virtual environment.

**Install PyPI package:**
`pip install mlstclassifier-cd`

https://pypi.org/project/mlstclassifier-cd/

## Usage:


The query can be a .txt file (as the one extracted from PubMLST), a csv file with the same structure as the example "MLST_file_example.csv" or an output file from [FastMLST](https://github.com/EnzoAndree/FastMLST).

Make sure you match the input file extension with the input type argument:
- Text file (.txt) from PubMLST: `pubmlst` argument;
- CSV file with the same structure as "MLST_file_example.csv": `csv` argument;
- Output from FastMLST: `fastmlst` argument.

### Basic Command:
`MLSTclassifier_cd [query file path] [output path] [input type]`

Example: `MLSTclassifier_cd /Desktop/folder_name/MLST_file_example.csv /Desktop/folder_name/exmple_output.csv csv`

## Output:

After running MLSTclassifier_cd, the output file should contain an additional column named "predicted_clade".
It also creates the following files:

- "pie_chart.html" displays the proportions of the different classes found.
- "count.csv" a csv file containing the raw value count of your predicted clades for you to generate your own graphs!