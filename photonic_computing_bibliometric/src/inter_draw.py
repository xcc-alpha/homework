"""
交互式图表绘制模块
"""

import pandas as pd
import networkx as nx
import json
from pathlib import Path
import config


def draw_html_net(G, part):
    """
    使用 vis.js 绘制交互式网络图
    
    Parameters
    ----------
    G : nx.Graph
        网络
    part : dict
        节点到社团的映射
    """
    print("🌐 生成交互式网络图...")
    
    if G.number_of_nodes() == 0:
        print("⚠️ 网络为空")
        return
    
    # 1. 准备节点数据
    nodes = []
    colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
        '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#52C4A1'
    ]
    
    community_colors = {}
    for comm_id in set(part.values()):
        community_colors[comm_id] = colors[comm_id % len(colors)]
    
    for node in G.nodes():
        nodes.append({
            'id': node,
            'label': node,
            'color': community_colors.get(part.get(node, -1), '#gray'),
            'size': G.degree(node) * 5 + 20,
            'title': f"Degree: {G.degree(node)}<br>Community: {part.get(node, -1)}"
        })
    
    # 2. 准备边数据
    edges = []
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 1)
        edges.append({
            'from': u,
            'to': v,
            'width': weight / 2,
            'title': f"Weight: {weight}"
        })
    
    # 3. 生成 HTML
    html_content = _generate_vis_html(nodes, edges)
    
    # 4. 保存文件
    output_path = Path(config.HTML_OUT) / '共现网络.html'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 网络图已保存: {output_path}")


def _generate_vis_html(nodes, edges):
    """
    生成 vis.js 交互式网络图的 HTML
    """
    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>光子计算文献计量 - 知识图谱</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        .header {{
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 24px;
            margin-bottom: 5px;
        }}
        #network {{
            flex: 1;
            background: white;
        }}
        .controls {{
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 15px;
            display: flex;
            gap: 10px;
            justify-content: center;
        }}
        button {{
            padding: 8px 15px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔬 光子计算文献计量分析</h1>
        <p>交互式知识图谱</p>
    </div>
    
    <div id="network"></div>
    
    <div class="controls">
        <button onclick="network.fit()">适应屏幕</button>
        <button onclick="network.setOptions({{physics: {{enabled: !network.options.physics.enabled}}}})">
            物理模拟
        </button>
    </div>

    <script type="text/javascript">
        var nodes = new vis.DataSet({nodes_json});
        var edges = new vis.DataSet({edges_json});
        var container = document.getElementById('network');
        var data = {{ nodes: nodes, edges: edges }};
        
        var options = {{
            physics: {{
                enabled: true,
                stabilization: {{ iterations: 200 }},
                barnesHut: {{
                    gravitationalConstant: -26000,
                    centralGravity: 0.3,
                    springLength: 200
                }}
            }}
        }};
        
        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>"""
    
    return html
