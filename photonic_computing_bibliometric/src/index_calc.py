import pandas as pd
def calc_index(df):
    total=len(df)
    year_dict=df["年份"].value_counts().sort_index().to_dict()
    top_auth=df["作者"].str.split("; ").explode().value_counts().head(10).to_dict()
    top_jour=df["期刊"].value_counts().head(10).to_dict()
    top_key=df["关键词"].str.split("; ").explode().value_counts().head(10).to_dict()
    return {"总文献":total,"年度发文":year_dict,"TOP10作者":top_auth,"TOP10期刊":top_jour,"TOP10关键词":top_key}
