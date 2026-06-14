import config
from src.bib_read import load_wos
from src.data_clean import clean_data, extract_keywords, get_data_summary
from src.index_calc import calc_index
from src.co_occur import build_co
from src.cluster_ana import louvain_cluster
from src.static_draw import draw_year_pic
from src.inter_draw import draw_html_net
from src.report_build import make_md_report
import traceback


def main():
    print("=" * 60)
    print("🔬 光子计算文献计量学分析")
    print("=" * 60)
    print()
    
    try:
        print("📚 Step 1: 加载 WOS 数据...")
        print("-" * 40)
        df_raw = load_wos(config.DATA_PATH)
        print()
        
        print("🧹 Step 2: 数据清洗...")
        print("-" * 40)
        df_cl = clean_data(df_raw)
        df_cl = extract_keywords(df_cl)
        print()
        
        print("📊 数据摘要:")
        summary = get_data_summary(df_cl)
        for key, value in summary.items():
            print(f"  • {key}: {value}")
        print()
        
        print("📈 Step 3: 计算文献计量指标...")
        print("-" * 40)
        base = calc_index(df_cl)
        print(base['summary_df'])
        print()
        
        print("🔗 Step 4: 关键词共现分析...")
        print("-" * 40)
        co_mat, keywords = build_co(df_cl, config.TOP_KEY)
        co_mat.to_csv(f\"{config.TABLE_OUT}/共现矩阵.csv\")
        print(f\"✅ 共现矩阵已保存\")
        print()
        
        print("🔀 Step 5: Louvain 聚类...")
        print("-" * 40)
        G, part, clus_df = louvain_cluster(co_mat, config.EDGE_THRESH)
        clus_df.to_csv(f\"{config.TABLE_OUT}/聚类结果.csv\", index=False)
        print(f\"✅ 聚类结果已保存\")
        print()
        
        print("📊 Step 6: 保存统计表...")
        print("-" * 40)
        base['summary_df'].to_csv(f\"{config.TABLE_OUT}/基本统计.csv\", index=False)
        print(f\"✅ 基本统计已保存\")
        print()
        
        print("🖼️  Step 7: 生成静态图表...")
        print("-" * 40)
        draw_year_pic(df_cl)
        print()
        
        print("🌐 Step 8: 生成交互式网络...")
        print("-" * 40)
        draw_html_net(G, part)
        print()
        
        print("📝 Step 9: 生成分析报告...")
        print("-" * 40)
        make_md_report(base, clus_df, co_mat)
        print()
        
        print("=" * 60)
        print("✅ 光子计算文献计量全部完成！")
        print("=" * 60)
        print()
        print("📁 输出文件位置:")
        print(f"   • 表格: {config.TABLE_OUT}/")
        print(f"   • 图表: {config.FIG_OUT}/")
        print(f"   • 网络: {config.HTML_OUT}/")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ 分析过程出错!")
        print("=" * 60)
        print(f"错误信息: {str(e)}")
        print()
        print("详细错误追踪:")
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == \"__main__\":
    exit(main())
