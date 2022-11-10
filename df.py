import matplotlib.pyplot as plt
import pandas as pd


def read_outfile(filepath: str, last_col: int = 13) -> pd.DataFrame:
    df = pd.read_csv(
        filepath,
        sep="|",
        header=0,
        usecols=list(range(4, last_col)),
        dtype=float,
        skiprows=[0, 2],
        skipfooter=1,
        engine="python"
    )
    df.columns = [c.strip() for c in df.columns]
    return df


if __name__ == "__main__":
    df1 = read_outfile("endc.out")
    df2 = read_outfile("endc2.out", last_col=12)
    
    df = pd.concat((df1, df2), join="outer", ignore_index=True)
    # df["alpha"].fillna(1e-4, inplace=True)
    # df = read_outfile("endc.out")
    print(df)

    params = ["alpha", "det", "punct", "power_positional", "power_syntactic"]
    metrics = ["top1_acc_train", "top3_acc_train", "top1_acc_valid", "top3_acc_valid"]

    for i, param in enumerate(params):
        plt.subplot(1, 5, i+1)
        for metric in metrics:
            plt.scatter(df[param], df[metric], s=1, alpha=1, label=metric)
        plt.title(param)
        plt.legend()
        plt.grid(True)
        plt.ylim(0.5, 1)
        if param == "alpha":
            plt.xscale("log")

    plt.tight_layout()
    plt.show()
