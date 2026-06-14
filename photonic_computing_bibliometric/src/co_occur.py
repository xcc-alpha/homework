"""
共现分析模块 - 关键词共现矩阵构建
"""

import pandas as pd
import numpy as np
from collections import Counter


def build_co(df, top_k=50):
    """
    构建关键词共现矩阵
    
    Parameters
    ----------
    df : pd.DataFrame
        数据框（必须包含 'KEYWORDS' 列）
    top_k : int
        选取频率最高的 k 个关键词
    
    Returns
    -------
    tuple
        (共现矩阵, 关键词列表)
    """
    print(f"🔗 构建关键词共现矩阵 (top {top_k})...")
    
    if 'KEYWORDS' not in df.columns:
        print("⚠️ 数据框中无 'KEYWORDS' 列，返回空矩阵")
        return np.zeros((0, 0)), []
    
    # 1. 提取所有关键词
    all_keywords = []
    keyword_lists = []
    
    for kw_str in df['KEYWORDS'].dropna():
        if isinstance(kw_str, str) and len(kw_str) > 0:
            keywords = [k.strip().lower() for k in kw_str.split(';')]
            keywords = [k for k in keywords if len(k) > 2]  # 过滤过短的词
            all_keywords.extend(keywords)
            keyword_lists.append(keywords)
    
    # 2. 统计关键词频率
    keyword_freq = Counter(all_keywords)
    top_keywords = [kw for kw, _ in keyword_freq.most_common(top_k)]
    
    print(f"  • 关键词总数: {len(keyword_freq)}")
    print(f"  • 选取top {top_k}: {len(top_keywords)}")
    
    # 3. 构建共现矩阵
    co_matrix = np.zeros((len(top_keywords), len(top_keywords)))
    keyword_to_idx = {kw: i for i, kw in enumerate(top_keywords)}
    
    for keywords in keyword_lists:
        # 只保留在 top_keywords 中的关键词
        filtered_kws = [kw for kw in keywords if kw in keyword_to_idx]
        
        # 计算共现
        for i, kw1 in enumerate(filtered_kws):
            for kw2 in filtered_kws[i+1:]:
                idx1 = keyword_to_idx[kw1]
                idx2 = keyword_to_idx[kw2]
                co_matrix[idx1, idx2] += 1
                co_matrix[idx2, idx1] += 1
    
    # 4. 创建共现矩阵数据框
    co_df = pd.DataFrame(
        co_matrix,
        index=top_keywords,
        columns=top_keywords
    )
    
    print(f"✅ 共现矩阵构建完成: {co_df.shape}")
    
    return co_df, top_keywords


def get_keyword_freq(df, top_k=50):
    """
    获取关键词频率统计
    
    Parameters
    ----------
    df : pd.DataFrame
        数据框
    top_k : int
        返回频率最高的 k 个关键词
    
    Returns
    -------
    pd.DataFrame
        关键词频率表
    """
    if 'KEYWORDS' not in df.columns:
        return pd.DataFrame()
    
    all_keywords = []
    for kw_str in df['KEYWORDS'].dropna():
        if isinstance(kw_str, str) and len(kw_str) > 0:
            keywords = [k.strip().lower() for k in kw_str.split(';')]
            all_keywords.extend(keywords)
    
    freq = pd.Series(all_keywords).value_counts().head(top_k)
    
    return pd.DataFrame({
        'keyword': freq.index,
        'frequency': freq.values
    }).reset_index(drop=True)
