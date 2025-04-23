# ML IDS

A collection of Machine Learning tools to build an AI-powered IDS.

## Requirements

- Python 3.12 or above
- Pip (Python package manager)

## To train your own model

### 1. Git clone

### 2. Choose Cowrie or Honeytrap training

Use your own dataset or use our, located in datasets/<chosen_dataset>.

Example: for Cowrie training.
```sh
cp datasets/cowrie_dataset_40k.csv unsupervised_training/cowrie_training/cowrie_dataset_40k.csv
```
```sh
sh setup.sh
python3 train_supervised_cowrie.py
```
