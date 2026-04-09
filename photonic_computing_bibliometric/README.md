# homework
# Photonic Computing Bibliometric Analysis
光子计算与人工智能交叉领域文献计量分析项目

## 📋 项目简介
本项目基于Web of Science核心合集，对2020-2025年间**光子计算加速神经网络/深度学习**的研究进行系统性文献计量分析，旨在挖掘领域研究热点、作者合作网络、演化趋势与前沿方向，为综述写作、课题申报提供数据支撑。

## 🎯 检索策略
```yaml
# config/query.yaml
query:
  database: "科学网络核心合集"
  time_window: [2020, 2025]
  boolean_expression: (TS=("光子计算"或"光学计算")) AND TS=("神经网络"或"深度学习") AND TS=("人工智能")
