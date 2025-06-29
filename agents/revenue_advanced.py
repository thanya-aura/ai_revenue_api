# agents/revenue_advanced.py
import pandas as pd
from typing import Dict

def analyze_revenue_advanced(project_data: Dict[str, pd.DataFrame], config: dict = None) -> dict:
    try:
        results = {}
        for project_name, df in project_data.items():
            # ✅ Check required columns
            required_cols = {'Month', 'Planned', 'Actual'}
            if not required_cols.issubset(df.columns):
                raise ValueError(f"Missing required columns in {project_name}. Required: {required_cols}")

            # ✅ Clean and prepare data
            df['Month'] = pd.to_datetime(df['Month'])
            df['Planned'] = pd.to_numeric(df['Planned'], errors='coerce').fillna(0)
            df['Actual'] = pd.to_numeric(df['Actual'], errors='coerce').fillna(0)
            df['Variance'] = df['Actual'] - df['Planned']
            df['Status'] = df['Variance'].apply(lambda x: "Over" if x > 0 else ("Under" if x < 0 else "On Plan"))

            results[project_name] = {
                "total_planned": float(df['Planned'].sum()),
                "total_actual": float(df['Actual'].sum()),
                "total_variance": float(df['Variance'].sum()),
                "rows": df.to_dict(orient="records")
            }

        return {
            "status": "success",
            "summary": results
        }

    except Exception as e:
        raise ValueError(f"Unexpected error in advanced analysis: {e}")
