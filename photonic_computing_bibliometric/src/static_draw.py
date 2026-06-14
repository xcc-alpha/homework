"""
静态图表绘制模块
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
import config

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


def draw_year_pic(df):
    """
    绘制按年份统计的论文发表趋势图
    
    Parameters
    ----------
    df : pd.DataFrame
        数据框（必须包含 'PY' 列）
    """
    print("📊 绘制发表趋势图...")
    
    if 'PY' not in df.columns:
        print("⚠️ 数据框中无 'PY' 列")
        return
    
    # 按年份统计
    papers_per_year = df['PY'].value_counts().sort_index()
    
    # 绘制
    fig, ax = plt.subplots(figsize=(12, 6))
    
    papers_per_year.plot(kind='bar', ax=ax, color='steelblue', alpha=0.8)
    
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Papers', fontsize=12)
    ax.set_title('Publication Trend - Photonic Computing', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 保存
    output_path = Path(config.FIG_OUT) / '发表趋势.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ 图表已保存: {output_path}")
    plt.close()
