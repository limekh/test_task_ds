import pandas as pd 

from summarizer.summarizer import Summarizer


def main():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "class"]
    df = pd.read_csv(url, header=None, names=columns)

    summarizer = Summarizer(df=df, output_type="html", out_filename="iris_stat")

    path = summarizer.get_report()
    print(f"Report saved: {path}")

if __name__ == "__main__":
    main()
