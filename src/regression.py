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

    for i, col in enumerate(df.columns):
        if col == args.gene_expr_start:
            gene_expr_start_index = i
        if col == args.gene_expr_end:
            gene_expr_end_index = i

    if gene_expr_start_index == -1 or gene_expr_end_index == -1:
        sys.exit('Expected first and last gene expression column '
                 'names not found')

    X = df.iloc[:, gene_expr_start_index:(gene_expr_end_index+1)]
    y = df.loc[:, "overall_survival_months"]

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.2,
                                                        random_state=args.seed,
                                                        shuffle=True)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    plt.scatter(y_test, y_pred)
    plt.plot([min(y_test), max(y_test)],
             [min(y_test), max(y_test)],
             color='purple',
             linestyle='--')
    plt.title("Testing data: actual vs predicted survival")
    plt.xlabel("Actual survival months")
    plt.ylabel("Predicted survival months")
    plt.savefig(args.out_folder + "/actual_vs_predicted_survival.png")
    plt.close()

    plt.hist(y_test-y_pred, bins=20)
    plt.axvline(x=0, color='purple', linestyle='--')
    plt.title("Residuals distribution")
    plt.xlabel("Residuals (actual survival months - "
               "predicted survival months)")
    plt.ylabel("Frequency")
    plt.savefig(args.out_folder + "/residuals.png")
    plt.close()

    coef_df = pd.DataFrame({"Feature": X.columns, "Coefficient": model.coef_})
    coef_df_sorted = coef_df.sort_values(by="Coefficient")

    important_features = coef_df_sorted.iloc[[0, 1, 2, 3, 4,
                                              -5, -4, -3, -2, -1], :]
    colors = ["red"]*5 + ["green"]*5

    plt.figure(figsize=(7, 5))
    plt.barh(important_features["Feature"],
             important_features["Coefficient"],
             color=colors)
    plt.xlabel("Coefficient value")
    plt.ylabel("Gene name")
    plt.suptitle("Gene importance (linear regression coefficients)")
    plt.title("Top 5 positive (green) and negative (red) coefficients",
              fontsize=10)
    plt.savefig(args.out_folder + "/coefficients.png")
    plt.close()


if __name__ == "__main__":
    main()
