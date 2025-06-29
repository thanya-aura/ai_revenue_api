import pandas as pd

def process(df: pd.DataFrame) -> dict:
    required_cols = ['Month', 'Planned', 'Actual']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df['Variance'] = df['Actual'] - df['Planned']
    df['Status'] = df['Variance'].apply(lambda x: "Over" if x > 0 else "Under" if x < 0 else "On Target")

    summary = {
        "total_planned": float(df['Planned'].sum()),
        "total_actual": float(df['Actual'].sum()),
        "total_variance": float(df['Variance'].sum()),
        "rows": df.to_dict(orient="records")
    }

    return summary
