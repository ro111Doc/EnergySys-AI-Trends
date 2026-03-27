# CNKI文献TXT转CSV标准格式
# 完美适配：SrcDatabase/Title/Author/Organ/Source/PubTime/Fund/DOI
import pandas as pd
import re

# ====================== 配置项（只需改这里）======================
input_txt = "CNKI-20260327180524663.txt"  # 你的输入文件名
output_csv = "CNKI_literature.csv"         # 输出CSV文件名
# ==============================================================

records = []
current = {}

# 精准匹配你的字段格式
pattern_map = {
    "来源库": r"SrcDatabase-来源库:\s*(.+)",
    "题名": r"Title-题名:\s*(.+)",
    "作者": r"Author-作者:\s*(.+)",
    "单位": r"Organ-单位:\s*(.+)",
    "文献来源": r"Source-文献来源:\s*(.+)",
    "发表时间": r"PubTime-发表时间:\s*(.+)",
    "基金": r"Fund-基金:\s*(.+)",
    "DOI": r"DOI-DOI:\s*(.+)"
}

# 读取解析
with open(input_txt, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            if current:
                records.append(current)
                current = {}
            continue
        
        for key, pat in pattern_map.items():
            m = re.match(pat, line)
            if m:
                current[key] = m.group(1).strip()
                break

if current:
    records.append(current)

# 保存CSV
df = pd.DataFrame(records)
df.to_csv(output_csv, index=False, encoding="utf-8-sig")

print(f"✅ 转换完成！共 {len(df)} 条文献")
print(f"📄 已输出：{output_csv}")
print("\n预览前3行：")
print(df.head(3))