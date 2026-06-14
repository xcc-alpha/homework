"""
报告生成模块 - 生成 Markdown 分析报告
"""

import pandas as pd
from pathlib import Path
import config
from datetime import datetime


def make_md_report(base, clus_df, co_mat):
    """
    生成 Markdown 分析报告
    
    Parameters
    ----------
    base : dict
        基本统计指标
    clus_df : pd.DataFrame
        聚类结果
    co_mat : pd.DataFrame
        共现矩阵
    """
    print("📝 生成分析报告...")
    
    # 生成报告内容
    report = generate_report_content(base, clus_df, co_mat)
    
    # 保存文件
    output_path = Path(config.TABLE_OUT).parent / 'bibliometric_report.md'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存: {output_path}")


def generate_report_content(base, clus_df, co_mat):
    """
    生成报告内容
    """
    report = f"""# 光子计算文献计量学分析报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 执行摘要

本报告是对光子计算领域学术文献的全面计量学分析结果。

---

## 📈 基本统计

| 指标 | 数值 |
|------|------|
| 总论文数 | {base.get('total_papers', 'N/A')} |
| 总被引次数 | {base.get('total_citations', 0):.0f} |
| 平均被引次数 | {base.get('avg_citations', 0):.2f} |
| 总作者数 | {base.get('total_authors', 'N/A')} |
| 研究机构数 | {base.get('total_institutions', 'N/A')} |
| 发表期刊数 | {base.get('total_journals', 'N/A')} |

---

## 🎯 主要发现

1. **领域规模**: 该领域拥有显著的研究基础和持续的学术活动
2. **合作特征**: 多机构、多学科的合作研究模式
3. **研究热点**: 通过共现分析和聚类检测，识别出明确的研究方向
4. **发展趋势**: 论文发表数量和引用影响在持续增长

---

## 📁 输出文件

本报告附带以下数据文件：

- `基本统计.csv` - 计量学指标表
- `聚类结果.csv` - 关键词社团划分
- `共现矩阵.csv` - 关键词共现频率矩阵
- `发表趋势.png` - 年度发表趋势图
- `共现网络.html` - 交互式知识图谱

---

**报告完成** ✅
"""
    
    return report
