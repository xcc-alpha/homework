"""
聚类分析模块 - Louvain 社团检测
"""

import pandas as pd
import numpy as np
import networkx as nx


def louvain_cluster(co_matrix, edge_thresh=2):
    """
    使用 Louvain 算法进行社团检测
    
    Parameters
    ----------
    co_matrix : pd.DataFrame or np.ndarray
        共现矩阵
    edge_thresh : int
        边权重阈值（小于此值的边被忽略）
    
    Returns
    -------
    tuple
        (网络图, 社团划分, 聚类结果数据框)
    """
    print("🔀 进行社团检测...")
    
    # 1. 构建网络
    if isinstance(co_matrix, pd.DataFrame):
        keywords = co_matrix.index.tolist()
        co_array = co_matrix.values
    else:
        co_array = co_matrix
        keywords = [f"keyword_{i}" for i in range(len(co_matrix))]
    
    # 2. 创建图
    G = nx.Graph()
    
    for i, kw in enumerate(keywords):
        G.add_node(kw)
    
    # 3. 添加边（只保留权重 >= edge_thresh 的边）
    for i in range(len(keywords)):
        for j in range(i+1, len(keywords)):
            weight = co_array[i, j]
            if weight >= edge_thresh:
                G.add_edge(keywords[i], keywords[j], weight=weight)
    
    print(f"  • 节点数: {G.number_of_nodes()}")
    print(f"  • 边数: {G.number_of_edges()}")
    
    # 4. Louvain 社团检测
    try:
        from networkx.algorithms.community import louvain_communities
        communities = list(louvain_communities(G, seed=42))
    except ImportError:
        print("⚠️ 需要安装 community 检测包，使用简单贪心算法")
        communities = _simple_community_detection(G)
    
    # 5. 创建社团映射
    part = {}
    for comm_id, community in enumerate(communities):
        for node in community:
            part[node] = comm_id
    
    print(f"  • 社团数: {len(communities)}")
    for i, comm in enumerate(communities):
        print(f"    - 社团 {i}: {len(comm)} 个关键词")
    
    # 6. 创建聚类结果数据框
    cluster_df = pd.DataFrame([
        {
            'keyword': kw,
            'cluster': part.get(kw, -1),
            'degree': G.degree(kw) if G.has_node(kw) else 0
        }
        for kw in keywords
    ])
    
    cluster_df = cluster_df.sort_values('cluster')
    
    print("✅ 社团检测完成")
    
    return G, part, cluster_df


def _simple_community_detection(G, num_communities=None):
    """
    简单的社团检测（当 louvain 不可用时）
    
    Parameters
    ----------
    G : nx.Graph
        网络
    num_communities : int, optional
        社团数
    
    Returns
    -------
    list
        社团列表
    """
    if G.number_of_nodes() == 0:
        return []
    
    # 获取连通分量
    components = list(nx.connected_components(G))
    
    return [set(comp) for comp in components]
