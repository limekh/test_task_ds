import numpy as np
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
        if pd.api.types.is_bool_dtype(series):
            return "boolean"
        elif pd.api.types.is_numeric_dtype(series):
            return "numeric"
        elif pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"
        return "categorical"
    
    @staticmethod
    def get_min(series: pd.Series) -> any:
        try:
            return series.min()
        except TypeError:
            return None
    
    @staticmethod
    def get_max(series: pd.Series) -> any:
        try:
            return series.max()
        except TypeError:
            return None
    
    @staticmethod
    def get_mode(series: pd.Series) -> any:
        mode_values = series.mode()
        return mode_values.iloc[0] if len(mode_values) > 0 else None
    
    def calculate_column_stats(self, column_name: str, series: pd.Series) -> dict:
        dtype = self.get_column_category(series)
        stats = {"Column": column_name, "Type": dtype}

        stats["distinct_values"] = series.nunique()
        stats["null_count"] = series.isna().sum()
        stats["% nulls"] = (series.isna().mean() * 100) if len(series) > 0 else 0.0

        if dtype == "numeric":
            stats["min"] = self.get_min(series)
            stats["max"] = self.get_max(series)
            stats["mean"] = series.mean()
            stats["median"] = series.median()
            stats["mode"] = self.get_mode(series)
            stats["zero rows(%)"] = (series == 0).mean() * 100
            stats["variance"] = series.var()
            stats["std"] = series.std(ddof=0) if len(series) > 0 else np.nan
            stats["IQR"] = series.quantile(0.75) - series.quantile(0.25)
            stats["CV"] = (stats["std"] / abs(stats["mean"])) if pd.notna(stats["mean"]) and stats["mean"] != 0 else np.nan

        elif dtype == "boolean":
            stats["min"] = int(series.min()) if series.notna().any() else None
            stats["max"] = int(series.max()) if series.notna().any() else None
            stats["mode"] = self.get_mode(series)
            stats["zero rows(%)"] = (~series).mean() * 100

        elif dtype in ("categorical", "datetime"):
            stats["min"] = self.get_min(series)
            stats["max"] = self.get_max(series)
            stats["mode"] = self.get_mode(series)
            stats["zero rows(%)"] = None

        return stats
    
    def get_summary(self) -> pd.DataFrame:
        rows = [self.calculate_column_stats(col, self.df[col]) for col in self.df.columns]
        self.stats_df = pd.DataFrame(rows).set_index("Column")

        return self.stats_df
    
    def get_report(self) -> str:
        if self.stats_df is None:
            self.get_summary()

        filepath = Path(self.out_filename)

        if self.output_type == "markdown":
            filepath = filepath.with_suffix(".md")
            content = self.stats_df.to_markdown(floatfmt=".2f")
            filepath.write_text(content, encoding="utf-8")

        elif self.output_type == "xlsx":
            filepath = filepath.with_suffix(".xlsx")
            with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
                self.stats_df.to_excel(writer, sheet_name="Summary")

        elif self.output_type == "html":
            filepath = filepath.with_suffix(".html")
            html_table = self.stats_df.to_html(float_format=lambda x: f"{x:.2f}" if pd.notna(x) else "")
            full_html = f"""<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Summary</title></head>
<body><h1>Summary statistics</h1>{html_table}</body>
</html>"""
            filepath.write_text(full_html, encoding="utf-8")

        else:
            raise ValueError(f"Unsupported report format type: {self.output_type}")
        
        return str(filepath.resolve())
    