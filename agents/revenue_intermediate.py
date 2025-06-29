import pandas as pd
from typing import Dict

def analyze_multi_project_revenue(project_data: Dict[str, pd.DataFrame], config: dict = None) -> dict:
    summary = {}
    for sheet_name, df in project_data.items():
        if not all(col in df.columns for col in ["Month", "Planned", "Actual"]):
            raise ValueError(f"Missing required columns in {sheet_name}")

        df["Variance"] = df["Actual"] - df["Planned"]
        total_planned = df["Planned"].sum()
        total_actual = df["Actual"].sum()
        total_variance = df["Variance"].sum()

        summary[sheet_name] = {
            "total_planned": int(total_planned),
            "total_actual": int(total_actual),
            "total_variance": int(total_variance),
        }

    return summary
