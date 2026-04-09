# 光子计算（Photonic Computing）研究前沿趋势追踪

## 项目简介

本项目基于文献计量学方法，系统分析光子计算（Photonic Computing）领域的研究热点、前沿趋势、核心作者与机构分布，揭示光计算技术在 AI 加速与高性能计算领域的发展脉络。研究时间跨度为 **2020–2025 年**，数据来源为 **Web of Science 核心合集**。

## 核心研究领域

- 光子计算（Photonic Computing）
- 光学神经网络（Optical Neural Networks）
- 光计算与 AI 加速
- 高性能光互连与计算架构

## 检索策略与数据来源

### 检索数据源

- **Web of Science 核心合集**（Web of Science Core Collection）
- 检索字段：标题（Title）、摘要（Abstract）、作者关键词（Author Keywords）
- 文献类型：Article + Review
- 时间范围：2020–2025

### 布尔检索式

("photonic computing" OR "optical computing" OR "photonics AI") 
AND ("neural network" OR "deep learning" OR "machine learning") 
AND ("AI acceleration" OR "optical neural network") 
NOT ("quantum computing" OR "silicon photonics only" OR "free-space optics")

### 项目核心里程碑 (Milestones)
## M1阶段：数据与检索方案验证（第4周末前）
阶段目标：完成从数据获取到初步清洗和验证。
核心步骤：
验证配置文件准确性。
定期检查数据质量报告。
## M2阶段：计量分析与图谱产出（第10周末前）
阶段目标：构建完整的文献计量网络图谱。
核心步骤：
完成图谱分析，并输出详细结果。
## M3阶段：终稿与项目归档（第15周末前）
阶段目标：编制详细的项目报告和学术论文。
核心步骤：
完成论文撰写与代码库的整理。

### 小组分工
辛成诚 202314010225：制定检索策略与布尔表达式；设计项目目录结构与版本控制方案；编写核心代码；基于 wos_export.xlsx 完成数据统计与分析
                  ：辅助数据检索：协助核对 WOS 导出字段，维护 data/raw/ 目录，撰写最终分析报告
                  ：数据清洗与预处理：运行去重与标准化脚本，输出 data/processed/；记录清洗规则。
                  ：计量分析辅助：基于 CiteSpace 进行共被引与聚类验证；提供 Python 分析结果对比。
                  ：可视化与文档辅助：生成部分图表（发文量趋势、关键词共现网络）；整理参考文献与提交。

### 项目结构
```text
photonic_computing_bibliometric/
├── data/
│   ├── raw/               # 原始文献数据（wos_export.xlsx）
│   └── processed/         # 清洗后的数据（CSV）
├── src/
│   ├── load_data.py       # 数据导入脚本（读取 xlsx）
│   ├── clean_data.py      # 数据清洗与消歧
│   ├── networks/
│   │   ├── co_citation.py      # 共被引矩阵构建
│   │   └── coupling_or_collab.py # 文献耦合与合作网络
│   └── metrics/
│       └── indicators.py       # 指标计算（h-index、篇均被引等）
├── outputs/
│   ├── figures/           # 图表（PNG/SVG）
│   └── tables/            # 统计表格（CSV）
├── reports/
│   ├── query_rationale.md # 检索策略说明与变更日志
│   ├── data_quality.md    # 数据质量报告（缺失率、重复率）
│   ├── metrics_spec.md    # 指标规范
│   └── threshold_sensitivity.md # 阈值敏感性对照
├── paper/
│   └── analysis_report.md # 最终分析报告
├── run_pipeline.py        # 一键运行脚本
├── requirements.txt       # Python 依赖清单
└── README.md              # 项目说明文档
```

### 环境依赖
```text
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
networkx>=3.0
scikit-learn>=1.2.0
openpyxl>=3.1.0   
```
