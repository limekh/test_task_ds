import pandas as pd


class Summarizer:
    """
    Класс генерирует статистику по столбцам из датафрейма
    """

    def __init__(self, df: pd.DataFrame, output_type: str="markdown", out_filename: str="summary_statistics"):
        self.df = df.copy()
        self.output_type = output_type
        self.out_filename = out_filename
        self.stats_df: pd.DataFrame | None = None

    def get_column_category(self, series: pd.Series):
        dtype = series.dtype
        dtype_name = dtype.name

        if dtype_name.startswith(('Int', 'UInt', 'Float')):
            return "numeric"
        
        elif dtype_name == 'boolean':
            return "boolean"
        
        elif 'datetime' in dtype_name:
            return "datetime"
        
        return "categorical"