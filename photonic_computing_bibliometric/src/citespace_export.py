"""
CiteSpace 导出模块 - 转换数据为 CiteSpace 兼容格式
支持输出格式：RIS、Bibtex、网络文件等
"""

import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Optional


def export_to_ris(df: pd.DataFrame, output_path: str) -> None:
    """
    将 WOS 数据导出为 RIS 格式（CiteSpace 支持）
    
    Parameters
    ----------
    df : pd.DataFrame
        清洗后的 WOS 数据
    output_path : str
        输出文件路径
    
    Notes
    -----
    RIS 格式是标准的文献交换格式，被 CiteSpace、Mendeley 等工具广泛支持
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, row in df.iterrows():
            f.write("TY  - JOUR\n")  # 期刊论文
            
            # 标题
            if pd.notna(row.get('TI')):
                f.write(f"TI  - {row['TI']}\n")
            
            # 作者（逗号分隔）
            if pd.notna(row.get('AU')):
                authors = str(row['AU']).split(';')
                for author in authors:
                    author = author.strip()
                    if author:
                        f.write(f"AU  - {author}\n")
            
            # 发表年份
            if pd.notna(row.get('PY')):
                f.write(f"PY  - {int(row['PY'])}\n")
            
            # 摘要
            if pd.notna(row.get('AB')):
                f.write(f"AB  - {row['AB']}\n")
            
            # 期刊
            if pd.notna(row.get('SO')):
                f.write(f"JO  - {row['SO']}\n")
            
            # 卷
            if pd.notna(row.get('VL')):
                f.write(f"VL  - {row['VL']}\n")
            
            # 期
            if pd.notna(row.get('IS')):
                f.write(f"IS  - {row['IS']}\n")
            
            # 页码
            if pd.notna(row.get('BP')):
                f.write(f"BP  - {row['BP']}\n")
            if pd.notna(row.get('EP')):
                f.write(f"EP  - {row['EP']}\n")
            
            # DOI
            if pd.notna(row.get('DI')):
                f.write(f"DO  - {row['DI']}\n")
            
            # 被引次数（作为自定义字段）
            if pd.notna(row.get('TC')):
                f.write(f"C1  - Cited: {int(row['TC'])}\n")
            
            # 关键词
            if pd.notna(row.get('KEYWORDS')):
                keywords = str(row['KEYWORDS']).split(';')
                for kw in keywords:
                    kw = kw.strip()
                    if kw:
                        f.write(f"KW  - {kw}\n")
            
            # Web of Science ID
            if pd.notna(row.get('UT')):
                f.write(f"ID  - {row['UT']}\n")
            
            # 记录结束
            f.write("ER  -\n\n")
    
    print(f"✅ RIS 格式已导出: {output_path}")


def export_to_bibtex(df: pd.DataFrame, output_path: str) -> None:
    """
    将 WOS 数据导出为 BibTeX 格式
    
    Parameters
    ----------
    df : pd.DataFrame
        清洗后的 WOS 数据
    output_path : str
        输出文件路径
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, row in df.iterrows():
            # 生成唯一的 citation key
            key = f"{row.get('AU', 'Unknown').split(';')[0].split()[-1]}{row.get('PY', 2024)}"
            key = key.replace(' ', '')[:15]  # 简化 key
            
            # 判断文献类型
            doc_type = str(row.get('DT', 'article')).lower()
            if 'proceedings' in doc_type or 'conference' in doc_type:
                entry_type = 'inproceedings'
            elif 'review' in doc_type:
                entry_type = 'article'
            else:
                entry_type = 'article'
            
            f.write(f"@{entry_type}{{{key},\n")
            
            # 标题
            if pd.notna(row.get('TI')):
                title = str(row['TI']).replace('{', '').replace('}', '')
                f.write(f"  title = {{{title}}},\n")
            
            # 作者
            if pd.notna(row.get('AU')):
                authors = str(row['AU']).split(';')
                authors = [a.strip() for a in authors if a.strip()]
                author_str = ' and '.join(authors)
                f.write(f"  author = {{{author_str}}},\n")
            
            # 发表年份
            if pd.notna(row.get('PY')):
                f.write(f"  year = {{{int(row['PY'])}}},\n")
            
            # 期刊
            if pd.notna(row.get('SO')):
                journal = str(row['SO']).replace('{', '').replace('}', '')
                f.write(f"  journal = {{{journal}}},\n")
            
            # 卷、期、页码
            if pd.notna(row.get('VL')):
                f.write(f"  volume = {{{row['VL']}}},\n")
            if pd.notna(row.get('IS')):
                f.write(f"  number = {{{row['IS']}}},\n")
            if pd.notna(row.get('BP')) and pd.notna(row.get('EP')):
                f.write(f"  pages = {{{row['BP']}--{row['EP']}}},\n")
            
            # DOI
            if pd.notna(row.get('DI')):
                f.write(f"  doi = {{{row['DI']}}},\n")
            
            # 摘要（注释）
            if pd.notna(row.get('AB')):
                abstract = str(row['AB']).replace('{', '').replace('}', '')[:200]
                f.write(f"  note = {{Abstract: {abstract}...}},\n")
            
            # 被引次数
            if pd.notna(row.get('TC')):
                f.write(f"  keywords = {{cited: {int(row['TC'])}}},\n")
            
            f.write("}\n\n")
    
    print(f"✅ BibTeX 格式已导出: {output_path}")


def export_to_tab_delimited(df: pd.DataFrame, output_path: str) -> None:
    """
    导出为制表符分隔格式（CiteSpace 直接支持）
    
    Parameters
    ----------
    df : pd.DataFrame
        清洗后的 WOS 数据
    output_path : str
        输出文件路径
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 选择 CiteSpace 需要的关键字段
    export_cols = {
        'PT': 'Publication Type',
        'AU': 'Author',
        'TI': 'Title',
        'SO': 'Source',
        'PY': 'Year',
        'VL': 'Volume',
        'IS': 'Issue',
        'BP': 'Begin Page',
        'EP': 'End Page',
        'DI': 'DOI',
        'TC': 'Cited Count',
        'Z9': 'ISI Essential Science Indicators',
        'U1': 'Usage Count',
        'U2': 'Usage Count Last 180 Days',
        'PU': 'Publisher',
        'PI': 'Publisher City',
        'PA': 'Publisher Address',
        'SN': 'ISSN',
        'EI': 'EISSN',
        'BN': 'ISBN',
        'J9': 'Journal ISO Abbreviation',
        'JI': 'Journal Index',
        'PD': 'Publication Date',
        'PY': 'Year Published',
        'GA': 'ISI Document Delivery Number',
        'UT': 'Unique Identifier',
        'PM': 'PubMed ID',
        'KEYWORDS': 'Keywords Plus'
    }
    
    # 选择存在的列
    cols_to_export = [col for col in export_cols.keys() if col in df.columns]
    
    # 导出为制表符分隔
    df[cols_to_export].to_csv(
        output_path,
        sep='\t',
        index=False,
        encoding='utf-8',
        quoting=1  # QUOTE_ALL
    )
    
    print(f"✅ 制表符分隔格式已导出: {output_path}")


def export_network_for_citespace(co_matrix: pd.DataFrame, 
                                output_dir: str,
                                threshold: int = 2) -> None:
    """
    导出网络数据以供 CiteSpace 的高级导入功能使用
    
    Parameters
    ----------
    co_matrix : pd.DataFrame
        共现矩阵
    output_dir : str
        输出目录
    threshold : int
        边权重阈值
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 导出为 Pajek 网络格式 (.net)
    # CiteSpace 可以导入这种格式进行进一步分析
    pajek_file = os.path.join(output_dir, 'keywords_network.net')
    export_to_pajek(co_matrix, pajek_file, threshold)
    
    # 2. 导出为简单的边表格式
    edge_list_file = os.path.join(output_dir, 'keywords_edges.csv')
    export_to_edgelist(co_matrix, edge_list_file, threshold)
    
    # 3. 导出为 GML 格式
    gml_file = os.path.join(output_dir, 'keywords_network.gml')
    export_to_gml(co_matrix, gml_file, threshold)


def export_to_pajek(co_matrix: pd.DataFrame, output_path: str, threshold: int = 2) -> None:
    """
    导出为 Pajek 网络格式
    """
    nodes = co_matrix.index.tolist()
    n_nodes = len(nodes)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # 节点部分
        f.write(f"*Vertices {n_nodes}\n")
        for i, node in enumerate(nodes, 1):
            f.write(f'{i} "{node}"\n')
        
        # 边部分
        f.write("*Edges\n")
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if i < j:
                    weight = co_matrix.loc[node1, node2]
                    if weight >= threshold:
                        f.write(f"{i+1} {j+1} {int(weight)}\n")
    
    print(f"✅ Pajek 格式已导出: {output_path}")


def export_to_edgelist(co_matrix: pd.DataFrame, output_path: str, threshold: int = 2) -> None:
    """
    导出为边表格式（CSV）
    """
    edges = []
    for i, node1 in enumerate(co_matrix.index):
        for j, node2 in enumerate(co_matrix.index):
            if i < j:
                weight = co_matrix.loc[node1, node2]
                if weight >= threshold:
                    edges.append({
                        'source': node1,
                        'target': node2,
                        'weight': int(weight)
                    })
    
    edge_df = pd.DataFrame(edges)
    if len(edge_df) > 0:
        edge_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ 边表已导出: {output_path} ({len(edge_df)} 条边)")
    else:
        print(f"⚠️ 无效边（阈值设置可能过高）")


def export_to_gml(co_matrix: pd.DataFrame, output_path: str, threshold: int = 2) -> None:
    """
    导出为 GML 图形格式（CiteSpace 和 Gephi 都支持）
    """
    nodes = co_matrix.index.tolist()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("graph [\n")
        f.write('  directed 0\n')
        
        # 节点
        for i, node in enumerate(nodes):
            f.write(f"  node [\n")
            f.write(f'    id {i}\n')
            f.write(f'    label "{node}"\n')
            f.write(f"  ]\n")
        
        # 边
        edge_id = 0
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if i < j:
                    weight = co_matrix.loc[node1, node2]
                    if weight >= threshold:
                        f.write(f"  edge [\n")
                        f.write(f"    id {edge_id}\n")
                        f.write(f"    source {i}\n")
                        f.write(f"    target {j}\n")
                        f.write(f"    weight {int(weight)}\n")
                        f.write(f"  ]\n")
                        edge_id += 1
        
        f.write("]\n")
    
    print(f"✅ GML 格式已导出: {output_path}")


def export_complete_citespace_package(df: pd.DataFrame, 
                                     co_matrix: pd.DataFrame,
                                     output_base_dir: str,
                                     threshold: int = 2) -> None:
    """
    一键导出完整的 CiteSpace 兼容数据包
    
    Parameters
    ----------
    df : pd.DataFrame
        原始 WOS 数据
    co_matrix : pd.DataFrame
        共现矩阵
    output_base_dir : str
        基础输出目录
    threshold : int
        网络边的权重阈值
    """
    print("\n" + "="*60)
    print("📦 开始导出 CiteSpace 兼容数据包...")
    print("="*60)
    
    # 创建 CiteSpace 专用目录
    citespace_dir = os.path.join(output_base_dir, 'citespace')
    os.makedirs(citespace_dir, exist_ok=True)
    
    # 1. 导出 RIS 格式（推荐用于导入到 CiteSpace）
    print("\n1️⃣  导出 RIS 格式...")
    ris_file = os.path.join(citespace_dir, 'export.ris')
    export_to_ris(df, ris_file)
    
    # 2. 导出 BibTeX 格式
    print("\n2️⃣  导出 BibTeX 格式...")
    bibtex_file = os.path.join(citespace_dir, 'export.bib')
    export_to_bibtex(df, bibtex_file)
    
    # 3. 导出制表符分隔格式
    print("\n3️⃣  导出制表符分隔格式...")
    tsv_file = os.path.join(citespace_dir, 'export.txt')
    export_to_tab_delimited(df, tsv_file)
    
    # 4. 导出网络文件
    print("\n4️⃣  导出网络分析文件...")
    network_dir = os.path.join(citespace_dir, 'networks')
    export_network_for_citespace(co_matrix, network_dir, threshold)
    
    print("\n" + "="*60)
    print("✅ CiteSpace 数据包导出完成！")
    print("="*60)
    print(f"\n📂 输出位置: {citespace_dir}")
    print(f"\n使用方法:")
    print(f"  1. 打开 CiteSpace")
    print(f"  2. 菜单 → File → Import → Select {ris_file}")
    print(f"  3. 系统会自动识别并导入参考文献数据")
    print(f"  4. 可选：使用 networks/ 中的网络文件进行进一步分析")
    print()
