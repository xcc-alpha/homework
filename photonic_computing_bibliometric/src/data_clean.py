"""
数据清洗模块 - 数据预处理和质量控制
"""

import pandas as pd
import numpy as np


def clean_data(df):
    """
    清洗 WOS 原始数据
    
    Parameters
    ----------
    df : pd.DataFrame
        原始数据框
    
    Returns
    -------
    pd.DataFrame
        清洗后的数据框
    """
    print("🧹 开始数据清洗...")
    
    df = df.copy()
    original_len = len(df)
    
    # 1. 删除重复记录
    df = df.drop_duplicates(subset=['UT'] if 'UT' in df.columns else None)
    print(f"  • 删除重复: {original_len} → {len(df)} 行")
    
    # 2. 处理缺失值
    # 标题字段不能为空
    if 'TI' in df.columns:
        df = df.dropna(subset=['TI'])
        print(f"  • 删除无标题: {len(df)} 行")
    
    # 3. 标准化列名
    df.columns = df.columns.str.strip().str.upper()
    
    # 4. 数据类型转换
    if 'PY' in df.columns:  # 发表年份
        df['PY'] = pd.to_numeric(df['PY'], errors='coerce')
    
    if 'TC' in df.columns:  # 被引次数
        df['TC'] = pd.to_numeric(df['TC'], errors='coerce').fillna(0).astype(int)
    
    # 5. 文本字段清洗
    text_cols = ['TI', 'AB', 'DE', 'ID', 'AU']  # 标题、摘要、关键词等
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna('').astype(str).str.strip()
    
    # 6. 删除不符合要求的记录（如无标题）
    if 'TI' in df.columns:
        df = df[df['TI'].str.len() > 0]
    
    print(f"✅ 清洗完成: {len(df)} 有效记录")
    
    return df


def extract_keywords(df):
    """
    提取和规范化关键词
    
    Parameters
    ----------
    df : pd.DataFrame
        清洗后的数据框
    
    Returns
    -------
    pd.DataFrame
        添加了关键词列的数据框
    """
    df = df.copy()
    
    # 优先使用 DE（author keywords），其次 ID（WOS keywords）
    if 'DE' in df.columns and 'ID' in df.columns:
        df['KEYWORDS'] = df['DE'].fillna('') + ';' + df['ID'].fillna('')
    elif 'DE' in df.columns:
        df['KEYWORDS'] = df['DE'].fillna('')
    elif 'ID' in df.columns:
        df['KEYWORDS'] = df['ID'].fillna('')
    else:
        df['KEYWORDS'] = ''
    
    # 清洗关键词
    df['KEYWORDS'] = (df['KEYWORDS']
                      .str.lower()
                      .str.strip()
                      .str.replace(r'\s*;+\s*', ';', regex=True))
    
    return df


def get_data_summary(df):
    """
    获取数据摘要统计信息
    
    Parameters
    ----------
    df : pd.DataFrame
        数据框
    
    Returns
    -------
    dict
        数据摘要信息
    """
    summary = {
        'total_papers': len(df),
        'year_range': (df['PY'].min(), df['PY'].max()) if 'PY' in df.columns else (None, None),
        'total_citations': df['TC'].sum() if 'TC' in df.columns else 0,
        'avg_citations': df['TC'].mean() if 'TC' in df.columns else 0,
        'languages': df['LA'].unique().tolist() if 'LA' in df.columns else [],
        'doc_types': df['DT'].unique().tolist() if 'DT' in df.columns else [],
    }
    return summary
