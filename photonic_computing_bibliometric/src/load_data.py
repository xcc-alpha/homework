# src/load_data.py
import pandas as pd
import sys
import os
from pathlib import Path

# 将项目根目录加入 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import clean_author_name, clean_affiliation, parse_cited_refs

PROJECT_ROOT = Path(__file__).parent.parent

def load_raw_data(file_path=None):
    if file_path is None:
        base_path = PROJECT_ROOT / "data" / "raw"
        # 尝试 .xls 或 .xlsx
        xls_path = base_path / "wos_export.xls"
        xlsx_path = base_path / "wos_export.xlsx"
        if xls_path.exists():
            file_path = xls_path
        elif xlsx_path.exists():
            file_path = xlsx_path
        else:
            raise FileNotFoundError(f"找不到文件: {xls_path} 或 {xlsx_path}")
    
    df = pd.read_excel(file_path, engine=None)  # 自动选择引擎
    print(f"成功加载文件: {file_path}")
    
    # 重命名列（包含所有需要的字段）
    rename_dict = {
        'Article Title': 'title',
        'Authors': 'authors_raw',
        'Author Full Names': 'authors_full',
        'Affiliations': 'affiliations_raw',
        'Publication Year': 'year',
        'Source Title': 'source',
        'Abstract': 'abstract',
        'Author Keywords': 'keywords',
        'Cited References': 'cited_refs_raw',   # <--- 关键：添加这一行
        'Times Cited, WoS Core': 'tc',
        'DOI': 'doi',
        'UT (Unique WOS ID)': 'ut'
    }
    df.rename(columns=rename_dict, inplace=True, errors='ignore')
    return df

def clean_data(df):
    df_clean = df.dropna(subset=['title', 'year']).copy()
    
    # 作者清洗
    df_clean['authors_clean'] = df_clean['authors_raw'].apply(
        lambda x: [clean_author_name(a) for a in str(x).split(';')] if pd.notna(x) else []
    )
    
    # 机构清洗
    df_clean['affiliations_clean'] = df_clean['affiliations_raw'].apply(
        lambda x: clean_affiliation(str(x).split(';')[0]) if pd.notna(x) else ""
    )
    
    # 关键词拆分
    df_clean['keywords_list'] = df_clean['keywords'].apply(
        lambda x: [k.strip().lower() for k in str(x).split(';')] if pd.notna(x) else []
    )
    
    # 解析参考文献列表（关键！）
    df_clean['cited_refs_ids'] = df_clean['cited_refs_raw'].apply(
        lambda x: parse_cited_refs(str(x)) if pd.notna(x) else []
    )
    
    return df_clean

def save_processed_data(df, output_path=None):
    if output_path is None:
        output_path = PROJECT_ROOT / "data" / "processed" / "papers_cleaned.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"清洗后数据已保存至 {output_path}")

if __name__ == "__main__":
    raw = load_raw_data()
    cleaned = clean_data(raw)
    save_processed_data(cleaned)