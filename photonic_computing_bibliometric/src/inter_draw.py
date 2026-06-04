from pyvis.network import Network,config
def draw_html_net(G,part):
    net=Network(width="100%",height="750px",bgcolor="#222222",font_color="white")
    net.barnes_hut()
    colors=["#FF6B6B","#4ECDC4","#45B7D1","#FECA57","#FF9FF3","#54A0FF"]
    for node in G.nodes:
        cid=part[node]
        size=G.degree(node)*4+8
        tip=f"关键词:{node}\n聚类:{cid}\n节点度:{G.degree(node)}"
        net.add_node(node,size=size,color=colors[cid%len(colors)],title=tip)
    for u,v,d in G.edges(data=True):
        net.add_edge(u,v,width=d["weight"]/2,title=f"共现:{d['weight']}")
    net.show(f"{config.HTML_OUT}/keyword_network.html",False)
