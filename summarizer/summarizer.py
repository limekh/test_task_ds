import pandas as pd

from pathlib import Path


class Summarizer:
    """
    Класс генерирует статистику по столбцам из датафрейма
    """

    def __init__(self, df: pd.DataFrame, output_type: str="markdown", out_filename: str="summary_statistics"):
        self.df = df.copy()
        self.output_type = output_type
        self.out_filename = out_filename
        self.stats_df: pd.DataFrame | None = None

    def get_column_category(self, series: pd.Series) -> str:
        dtype = series.dtype
        dtype_name = dtype.name

        if dtype_name.startswith(('Int', 'UInt', 'Float')):
            return "numeric"
        
        elif dtype_name == 'boolean':
            return "boolean"
        
        elif 'datetime' in dtype_name:
            return "datetime"
        
        return "categorical"
    
    def calculate_column_stats(self, column_name: str, series: pd.Series) -> dict:
        dtype = self.get_column_category(series)
        stats = {"Column": column_name, "Type": dtype}

        if dtype == "numeric":
            stats["Min"] = series.min()
            stats["Max"] = series.max()
            stats["Mean"] = series.mean()
            stats["Median"] = series.median()
            stats["Mode"] = series.mode()
            stats["Zero rows(%)"] = (series == 0).mean() * 100
            stats["Variance"] = series.var()
            stats["Std"] = series.std()
            stats["IQR"] = series.quantile(0.75) - series.quantile(0.25)
            stats["CV"] = (stats["std"] / abs(stats["mean"]))

        elif dtype == "boolean":
            stats["Min"] = int(series.min())
            stats["Max"] = int(series.max())
            stats["Zero rows(%)"] = (~series.astype(bool)).mean() * 100

        elif dtype in ("categorical", "datetime"):
            stats["Min"] = series.min()
            stats["Max"] = series.max()
            stats["Mode"] = series.mode()
            stats["Zero rows(%)"] = (~series.astype(bool)).mean() * 100

        return stats
    
    def get_summary(self) -> pd.DataFrame:
        rows = [self.compute_column_stats(col, self.df[col]) for col in self.df.columns]
        self.stats_df = pd.DataFrame(rows).set_index("Column")

        return self.stats_df
    
    def get_report(self) -> str:
        if self.stats_df is None:
            self.get_summary()

        filepath = Path(self.out_filename)

        if self.output_type == "markdown":
            pass
        elif self.output_type == "xslx":
            pass
        elif self.output_type == "html":
            pass
        
        return "test"
