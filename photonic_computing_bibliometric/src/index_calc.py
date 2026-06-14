"""
指标计算模块 - 文献计量学基本指标
"""

import pandas as pd
import numpy as np


def calc_index(df):
    """
    计算文献计量学基本指标
    
    Parameters
    ----------
    df : pd.DataFrame
        清洗后的数据框
    
    Returns
    -------
    dict
        包含各类指标的字典
    """
    print("📈 计算文献计量指标...")
    
    results = {}
    
    # 1. 发表统计
    results['total_papers'] = len(df)
    results['publication_years'] = sorted(df['PY'].unique().tolist()) if 'PY' in df.columns else []
    results['papers_per_year'] = df['PY'].value_counts().sort_index().to_dict() if 'PY' in df.columns else {}
    
    # 2. 引用统计
    if 'TC' in df.columns:
        results['total_citations'] = df['TC'].sum()
        results['avg_citations'] = df['TC'].mean()
        results['median_citations'] = df['TC'].median()
        results['max_citations'] = df['TC'].max()
        results['highly_cited_papers'] = len(df[df['TC'] > df['TC'].quantile(0.75)])
    else:
        results['total_citations'] = 0
        results['avg_citations'] = 0
    
    # 3. 作者统计
    if 'AU' in df.columns:
        all_authors = []
        for authors_str in df['AU'].dropna():
            if isinstance(authors_str, str):
                authors = [a.strip() for a in authors_str.split(';')]
                all_authors.extend(authors)
        
        results['total_authors'] = len(set(all_authors))
        results['avg_authors_per_paper'] = len(all_authors) / len(df) if len(df) > 0 else 0
        results['top_authors'] = pd.Series(all_authors).value_counts().head(10).to_dict()
    
    # 4. 机构统计
    if 'C1' in df.columns:
        all_institutions = []
        for inst_str in df['C1'].dropna():
            if isinstance(inst_str, str):
                insts = [i.strip() for i in inst_str.split(';')]
                all_institutions.extend(insts)
        
        results['total_institutions'] = len(set(all_institutions))
        results['top_institutions'] = pd.Series(all_institutions).value_counts().head(10).to_dict()
    
    # 5. 期刊统计
    if 'SO' in df.columns:
        results['total_journals'] = df['SO'].nunique()
        results['top_journals'] = df['SO'].value_counts().head(10).to_dict()
    
    # 6. 文献类型
    if 'DT' in df.columns:
        results['document_types'] = df['DT'].value_counts().to_dict()
    
    # 7. 创建摘要数据框
    summary_df = pd.DataFrame([
        {'指标': 'Total Papers', '数值': results['total_papers']},
        {'指标': 'Total Citations', '数值': results.get('total_citations', 0)},
        {'指标': 'Average Citations', '数值': results.get('avg_citations', 0)},
        {'指标': 'Total Authors', '数值': results.get('total_authors', 0)},
        {'指标': 'Total Institutions', '数值': results.get('total_institutions', 0)},
        {'指标': 'Total Journals', '数值': results.get('total_journals', 0)},
    ])
    
    results['summary_df'] = summary_df
    
    print("✅ 指标计算完成")
    
    return results


def calc_h_index(df):
    """
    计算 h-index
    
    Parameters
    ----------
    df : pd.DataFrame
        数据框（必须包含 'TC' 列）
    
    Returns
    -------
    int
        h-index 值
    """
    if 'TC' not in df.columns:
        return 0
    
    citations = sorted(df['TC'].values, reverse=True)
    h_index = 0
    
    for i, c in enumerate(citations, 1):
        if c >= i:
            h_index = i
        else:
            break
    
    return h_index
