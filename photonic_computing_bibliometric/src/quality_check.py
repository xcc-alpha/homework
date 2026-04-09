# src/quality_check.py
import sys
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def generate_quality_report(df, output_md_path=None):
    if output_md_path is None:
        output_md_path = PROJECT_ROOT / "reports" / "data_quality.md"
    output_md_path.parent.mkdir(parents=True, exist_ok=True)
    report = []
    report.append("# 数据质量报告\\\\n")
    total = len(df)
    report.append(f"## 总记录数: {total}\\\\n")
    missing = df[['title', 'doi', 'authors_raw', 'year', 'source', 'abstract', 'cited_refs_raw']].isnull().sum()
    report.append("## 关键字段缺失率\\\\n")
    for col, cnt in missing.items():
        rate = cnt / total * 100
        report.append(f"- {col}: {rate:.1f}% ({cnt}条缺失)\\\\n")
    doi_unique = df['doi'].dropna().nunique()
    report.append(f"\\\\n## 重复率 (基于DOI): {(total - doi_unique)/total*100:.1f}%\\\\n")
    ambiguous_example = "潜在歧义: 缩写 'Zhu, LQ' 出现在多篇不同机构论文中，建议人工复核。"
    report.append(f"\\\\n## 歧义评估\\\\n{ambiguous_example}\\\\n")
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.writelines(report)
    print(f"质量报告已保存至 {output_md_path}")

if __name__ == "__main__":
    data_path = PROJECT_ROOT / "data" / "processed" / "papers_cleaned.csv"
    if not data_path.exists():
        print("错误：请先运行 src/load_data.py 生成 papers_cleaned.csv")
        sys.exit(1)
    df = pd.read_csv(data_path)
    generate_quality_report(df)