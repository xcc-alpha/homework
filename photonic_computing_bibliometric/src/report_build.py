import pandas as pd,config
def make_md_report(base_ind,clus_df,co_mat):
    path=f"{config.TAB_OUT}/光子计算文献计量报告.md"
    md=f"""# 光子计算领域文献计量分析报告
## 一、基础统计
总文献数量：{base['总文献']}
### 1.年度发文
{pd.Series(base_ind['年度发文']).to_markdown()}
### 2.TOP10高产作者
{pd.Series(base_ind['TOP10作者']).to_markdown()}
###3.TOP10刊载期刊
{pd.Series(base_ind['TOP10期刊']).to_markdown()}
###4.TOP10高频关键词
{pd.Series(base_ind['TOP10关键词']).to_markdown()}

##二、关键词聚类结果
{clus_df.to_markdown(index=False)}

##三、可视化附件
1.年度趋势图：{config.FIG_OUT}/year_trend.png
2.交互式聚类图谱（浏览器打开）：{config.HTML_OUT}/keyword_network.html
"""
    with open(path,"w",encoding="utf-8") as f:
        f.write(md)
    co_mat.to_csv(f"{config.TAB_OUT}/co_occur_matrix.csv",encoding="utf-8-sig")
    clus_df.to_csv(f"{config.TAB_OUT}/cluster_info.csv",encoding="utf-8-sig",index=False)
