import re

def parse_cited_refs(ref_str):
    """
    从WoS的Cited References字段中提取被引文献的唯一标识。
    优先提取DOI，如果没有DOI则提取“作者名_年份”组合。
    """
    if not isinstance(ref_str, str) or not ref_str.strip():
        return []
    
    # 1. 尝试提取DOI（最可靠）
    dois = re.findall(r'10\\\\.\\\\d{4,9}/[-._;()/:A-Z0-9a-z]+', ref_str)
    if dois:
        return dois
    
    # 2. 如果没有DOI，则尝试提取“作者名_年份”
    # 常见模式： "Author, A, YYYY, ..." 或 "Author A, YYYY"
    # 使用正则提取第一个单词（姓氏）和四位数字年份
    pattern = r'^([A-Z][a-z]+)[,.]?\\\\s+[A-Z]?\\\\.?\\\\s*,?\\\\s*(\\\\d{4})'
    match = re.search(pattern, ref_str)
    if match:
        last_name = match.group(1)
        year = match.group(2)
        return [f"{last_name}_{year}"]
    
    # 3. 如果以上都不匹配，返回整个字符串的哈希（避免完全丢失）
    # 但仅作为最后手段，会降低匹配精度
    return [ref_str[:50]]  # 截取前50字符作为标识

def clean_author_name(author_str, rules=None):
    """作者消歧：统一为 'LastName, FirstInitial' 格式"""
    if not isinstance(author_str, str):
        return ""
    parts = author_str.strip().split(',')
    if len(parts) >= 1:
        last = parts[0].strip()
        first_init = ""
        if len(parts) > 1 and parts[1].strip():
            first_init = parts[1].strip()[0] if parts[1].strip() else ""
        return f"{last}, {first_init}." if first_init else last
    return author_str

def clean_affiliation(aff_str, rules=None):
    """机构消歧：映射别名"""
    if not isinstance(aff_str, str):
        return ""
    mapping = {
        "Beijing Informat Sci & Technol Univ": "Beijing Information S&T University",
        "Beijing Information Science & Technology University": "Beijing Information S&T University",
        "MIT": "Massachusetts Institute of Technology",
        "Mass. Inst. Tech.": "Massachusetts Institute of Technology"
    }
    for alias, std in mapping.items():
        if alias in aff_str:
            return std
    return aff_str