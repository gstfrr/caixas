import pandas as pd
from dataclasses import dataclass


# Define classes for each sheet
@dataclass
class Planilha1:
    caixa_id: int
    item: str
    pecas: int


# Function to map DataFrame columns to class attributes
def map_columns(df: pd.DataFrame, mapping: dict):
    df = df.rename(columns=mapping)
    return df


# Function to read data from Excel and create class instances
def read_excel(file_path: str):
    xlsx = pd.ExcelFile(file_path)
    data_classes = {
        "Planilha1": (Planilha1, {"Caixa Id": "caixa_id", "Item": "item", "Peças": "pecas"})
    }

    data_instances = {}

    for sheet_name in xlsx.sheet_names:
        df = xlsx.parse(sheet_name)
        cls, mapping = data_classes[sheet_name]
        df = map_columns(df, mapping)
        instances = [cls(**{k: (v if pd.notna(v) else None) for k, v in row.items()}) for index, row in df.iterrows()]
        data_instances[sheet_name] = instances

    return data_instances
