# check_cited.py
import pandas as pd
import ast

df = pd.read_csv("data/processed/papers_cleaned.csv")
# 将字符串转换为列表
df['cited_refs_ids'] = df['cited_refs_ids'].apply(ast.literal_eval)

# 检查有多少行有非空的被引文献
non_empty = df['cited_refs_ids'].apply(len).sum()
print(f"总记录数: {len(df)}")
print(f"非空被引文献列表的行数: {(df['cited_refs_ids'].apply(len) > 0).sum()}")
print(f"总共提取到的被引文献条目数: {non_empty}")
# 打印第一行的 cited_refs_raw 内容作为样例
print("\\n第一条记录的原始引用字段（前200字符）:")
print(df['cited_refs_raw'].iloc[0][:200])