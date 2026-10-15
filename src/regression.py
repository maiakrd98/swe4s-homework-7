import argparse
import sys
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def main():

    parser = argparse.ArgumentParser(
        description='Run a linear regression using gene expression to predict '
                    'breast cancer survival months')

    parser.add_argument('--data_file',
                        type=str,
                        help='File path containing data on gene expression '
                             'and outcomes for breast cancer patients',
                        required=True)

    parser.add_argument('--out_folder',
                        type=str,
                        help='Path to folder to save images in',
                        required=True)

    parser.add_argument('--seed',
                        type=int,
                        help='Random seed',
                        required=True)

    parser.add_argument('--gene_expr_start',
                        type=str,
                        help='Name of first gene expression column name',
                        required=True)

    parser.add_argument('--gene_expr_end',
                        type=str,
                        help='Name of last gene expression column name',
                        required=True)

    args = parser.parse_args()

    try:
        df = pd.read_csv(args.data_file, low_memory=False)
    except FileNotFoundError:
        sys.exit('Could not find ' + args.data_file)

    # identify column indexes of start and end of gene expression data
    gene_expr_start_index = -1
    gene_expr_end_index = -1

    for i,col in enumerate(df.columns):
        if col == args.gene_expr_start:
            gene_expr_start_index = i
        if col == args.gene_expr_end:
            gene_expr_end_index = i

    if gene_expr_start_index == -1 or gene_expr_end_index == -1:
        sys.exit('Expected first and last gene expression column names not found')

    print(gene_expr_start_index)
    print(gene_expr_end_index)

if __name__ == "__main__":
    main()
