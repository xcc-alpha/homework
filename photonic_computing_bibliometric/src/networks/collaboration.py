# src/networks/collaboration.py
import pandas as pd
import networkx as nx
import ast
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent

def build_coauthorship_network(df):
    G = nx.Graph()
    for authors in df['authors_clean']:
        if len(authors) < 2:
            continue
        for i in range(len(authors)):
            for j in range(i+1, len(authors)):
                a1, a2 = authors[i], authors[j]
                if G.has_edge(a1, a2):
                    G[a1][a2]['weight'] += 1
                else:
                    G.add_edge(a1, a2, weight=1)
    return G

def compute_centrality(G):
    deg = nx.degree_centrality(G)
    between = nx.betweenness_centrality(G, weight='weight')
    try:
        eigen = nx.eigenvector_centrality(G, weight='weight', max_iter=1000)
    except:
        eigen = {n: 0 for n in G.nodes()}
    return deg, between, eigen

def top_authors_table(deg, between, eigen, top_n=15):
    nodes = list(deg.keys())
    table = []
    for node in nodes[:top_n]:
        table.append({
            'Author': node,
            'Degree': round(deg[node], 4),
            'Betweenness': round(between.get(node,0), 4),
            'Eigenvector': round(eigen.get(node,0), 4)
        })
    return pd.DataFrame(table)

if __name__ == "__main__":
    data_path = PROJECT_ROOT / "data" / "processed" / "papers_cleaned.csv"
    if not data_path.exists():
        print("错误：请先运行 src/load_data.py")
        sys.exit(1)
    df = pd.read_csv(data_path)
    df['authors_clean'] = df['authors_clean'].apply(ast.literal_eval)
    G = build_coauthorship_network(df)
    deg, bet, eig = compute_centrality(G)
    top_df = top_authors_table(deg, bet, eig)
    out_csv = PROJECT_ROOT / "outputs" / "tables" / "top_authors.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    top_df.to_csv(out_csv, index=False)
    print(f"合作网络中心性Top15已保存至 {out_csv}")
    out_gexf = PROJECT_ROOT / "outputs" / "coauthorship_network.gexf"
    nx.write_gexf(G, out_gexf)
    print(f"合作网络图已保存至 {out_gexf}")