# 安装指南

## 系统要求

- Python 3.8 及以上
- pip 或 conda 包管理器

## 安装步骤

### 1. 克隆或下载项目

```bash
cd photonic_computing_bibliometric
```

### 2. 创建虚拟环境（推荐）

**使用 conda:**
```bash
conda create -n photonic-bib python=3.9
conda activate photonic-bib
```

**使用 venv:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

如果需要 Louvain 社团检测的完整支持：
```bash
pip install python-louvain
```

### 4. 验证安装

```bash
python -c "import pandas, networkx, matplotlib; print('✅ 依赖安装成功')"
```

## 数据准备

### 获取 WOS 数据

1. 访问 [Web of Science](https://webofknowledge.com/)
2. 搜索相关论文（例如: "photonic computing"）
3. 导出数据为 txt 或 xlsx 格式

### 放置数据文件

1. 创建数据目录（如果不存在）：
   ```bash
   mkdir -p data/sample-wos
   ```

2. 将导出的数据文件放入 `data/sample-wos/` 目录

3. 确保文件列表：
   ```
   data/sample-wos/
   ├── data1.txt (或 .csv/.xlsx)
   ├── data2.txt
   └── ...
   ```

## 运行项目

### 快速运行

```bash
python run.py
```

### 查看帮助信息

```bash
python run.py --help
```

## 故障排除

### Issue: ModuleNotFoundError: No module named 'xxx'

**解决方案:**
```bash
# 重新安装依赖
pip install -r requirements.txt --upgrade
```

### Issue: 数据加载失败

**检查清单:**
- [ ] WOS 数据文件是否在 `data/sample-wos/` 目录
- [ ] 文件格式是否正确（支持 .txt, .csv, .xlsx）
- [ ] 文件编码是否为 UTF-8

### Issue: 网络图无法显示

**解决方案:**
- 确保 vis.js 库可以正常访问（需要网络连接）
- 或者在本地下载 vis.js 库

### Issue: 内存不足

**解决方案:**
- 在 `config.py` 中减少 `TOP_KEY` 值
- 使用更小的数据集进行测试

## 下一步

安装完成后，请参考 [README.md](README.md) 了解项目的详细使用说明。

有问题？提交 Issue 或查看文档！
