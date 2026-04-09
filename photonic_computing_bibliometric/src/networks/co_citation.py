# src/networks/co_citation.py
import pandas as pd
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import sys
import ast

PROJECT_ROOT = Path(__file__).parent.parent.parent

def build_co_citation_matrix(df):
    all_cited = []
    for refs in df['cited_refs_ids']:
        all_cited.extend(refs)
    unique_cited = list(set(all_cited))
    cited_to_idx = {cid: i for i, cid in enumerate(unique_cited)}
    n_papers = len(df)
    n_cited = len(unique_cited)
    R = np.zeros((n_papers, n_cited), dtype=int)
    for i, refs in enumerate(df['cited_refs_ids']):
        for cid in refs:
            if cid in cited_to_idx:
                R[i, cited_to_idx[cid]] = 1
    C = R.T @ R
    np.fill_diagonal(C, 0)
    return C, unique_cited

def filter_and_cluster(C, node_names, threshold_top_n=30, similarity='cosine'):
    sim = cosine_similarity(C)
    filtered = np.zeros_like(sim)
    n = min(threshold_top_n, sim.shape[0])
    for i in range(sim.shape[0]):
        top_idx = np.argsort(sim[i])[-n:]
        filtered[i, top_idx] = sim[i, top_idx]
    G = nx.Graph()
    for i in range(len(node_names)):
        G.add_node(node_names[i])
    for i, j in zip(*np.where(filtered > 0)):
        if i < j:
            G.add_edge(node_names[i], node_names[j], weight=filtered[i,j])
    try:
        import community.community_louvain as community_louvain
        partition = community_louvain.best_partition(G, weight='weight')
        mod = nx.algorithms.community.modularity(G, [set(nodes) for nodes in partition.values()])
    except ImportError:
        print("未安装 python-louvain，跳过 Modularity 计算")
        partition = {node: cid for cid, comp in enumerate(nx.connected_components(G)) for node in comp}
        mod = 0
    return G, partition, mod

if __name__ == "__main__":
    data_path = PROJECT_ROOT / "data" / "processed" / "papers_cleaned.csv"
    if not data_path.exists():
        print("错误：请先运行 src/load_data.py")
        sys.exit(1)
    df = pd.read_csv(data_path)
    df['cited_refs_ids'] = df['cited_refs_ids'].apply(ast.literal_eval)
    
    # 检查是否有被引文献数据
    total_cited = sum(len(x) for x in df['cited_refs_ids'])
    if total_cited == 0:
        print("警告：没有提取到任何被引文献，无法构建共被引网络。")
        print("请检查 utils.py 中的 parse_cited_refs 函数是否正确解析了 cited_refs_raw 字段。")
        sys.exit(0)
    
    C, cited_names = build_co_citation_matrix(df)
    if len(cited_names) == 0:
        print("警告：共被引矩阵为空，跳过网络构建。")
        sys.exit(0)
    # 继续执行...