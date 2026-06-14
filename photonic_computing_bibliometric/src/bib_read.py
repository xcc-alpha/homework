"""
数据加载模块 - 读取 WOS 格式数据
"""

import pandas as pd
import os
from pathlib import Path


def load_wos(data_path):
    """
    加载 WOS 格式的数据文件
    
    Parameters
    ----------
    data_path : str
        WOS 数据文件所在目录路径
    
    Returns
    -------
    pd.DataFrame
        加载的原始数据
    
    Raises
    ------
    FileNotFoundError
        当数据目录不存在时
    ValueError
        当数据目录为空时
    """
    data_dir = Path(data_path)
    
    if not data_dir.exists():
        raise FileNotFoundError(f"数据目录不存在: {data_path}")
    
    # 查找所有数据文件（支持多种格式）
    files = []
    for ext in ['*.txt', '*.csv', '*.xlsx']:
        files.extend(list(data_dir.glob(ext)))
    
    if not files:
        raise ValueError(f"数据目录为空或无支持的文件格式: {data_path}")
    
    print(f"📁 找到 {len(files)} 个数据文件")
    
    dfs = []
    for file in files:
        try:
            if file.suffix == '.xlsx':
                df = pd.read_excel(file)
            elif file.suffix == '.csv':
                df = pd.read_csv(file, encoding='utf-8')
            elif file.suffix == '.txt':
                # WOS 导出的 txt 格式
                df = pd.read_csv(file, sep='\t', encoding='utf-8', on_bad_lines='skip')
            else:
                continue
            
            dfs.append(df)
            print(f"✅ 加载成功: {file.name} ({len(df)} 行)")
        except Exception as e:
            print(f"❌ 加载失败 {file.name}: {e}")
            continue
    
    if not dfs:
        raise ValueError("没有成功加载任何数据文件")
    
    # 合并所有数据
    df_combined = pd.concat(dfs, ignore_index=True)
    print(f"\n📊 总数据量: {len(df_combined)} 行 × {len(df_combined.columns)} 列")
    
    return df_combined


def load_wos_from_file(file_path):
    """
    从单个文件加载 WOS 数据
    
    Parameters
    ----------
    file_path : str
        WOS 数据文件路径
    
    Returns
    -------
    pd.DataFrame
        加载的数据
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if file_path.suffix == '.xlsx':
        df = pd.read_excel(file_path)
    elif file_path.suffix == '.csv':
        df = pd.read_csv(file_path, encoding='utf-8')
    elif file_path.suffix == '.txt':
        df = pd.read_csv(file_path, sep='\t', encoding='utf-8', on_bad_lines='skip')
    else:
        raise ValueError(f"不支持的文件格式: {file_path.suffix}")
    
    print(f"✅ 加载成功: {file_path.name} ({len(df)} 行)")
    return df
