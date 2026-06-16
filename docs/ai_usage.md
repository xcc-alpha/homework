# AI 使用情况说明 (AI Usage Statement)

根据文献计量学课程教学规范，本项目在开发和撰写过程中合理使用了 AI 工具。以下为详细使用情况说明：

## 1. 使用工具与版本
- AI 助手： Antigravity (Google DeepMind team)
- 底层模型： Gemini 3.5 Flash (Medium)

## 2. 辅助开发范围
- 代码重构与包管理： 辅助排查 Python `sys.path` 与相对导入问题，解决 `src.bmmini` 包中的循环导入（circular import）冲突。

## 3. 人工核验与保证
- 数据真实性： 所有分析数据（5,010 篇文献的各网络节点指标、网络特征、发文分布）均由 Python Pipeline 从原始 WOS text 数据包中进行纯程序化计算生成，无任何 AI 伪造或幻觉产生的数据。
- 代码复现性： 经人工在 Windows 本地环境下运行 `python run.py` 及 `pytest` 测试，确保所有分析流程一键通过，不依赖任何闭源或非本地的 AI 接口。
- 独立思考： 论文中关于光子计算前沿研究方向的讨论（如 Silicon Photonics Neural Network Accelerators, Optical Chaos Reservoir Computing）均基于对真实提取的文献网络中高被引文章的学术分析，非 AI 编造。
