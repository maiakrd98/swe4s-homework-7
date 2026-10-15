import argparse
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

    pass


if __name__ == "__main__":
    main()
