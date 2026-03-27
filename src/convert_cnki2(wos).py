import pandas as pd

# 路径自己改
txt_path = "web of science.txt"    # 你的WOS文件
csv_path = "raw_data.csv"          # 输出CSV

records = []
current = {}

with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()

    # 标题 TI
    if line.startswith("TI "):
        current["title"] = line[2:].strip()

    # 作者 AU
    elif line.startswith("AU "):
        current["author"] = line[2:].strip()

    # 摘要 AB
    elif line.startswith("AB "):
        current["abstract"] = line[2:].strip()

    # 发表年份 PY
    elif line.startswith("PY "):
        current["year"] = line[2:].strip()

    # DOI
    elif line.startswith("DI "):
        current["doi"] = line[2:].strip()

    # 一篇结束 ER
    elif line.startswith("ER"):
        if current:
            records.append(current)
            current = {}

# 最后一篇
if current:
    records.append(current)

# 转DataFrame
df = pd.DataFrame(records)

# 补全你筛选代码需要的列
df["fulltext"] = ""
df["language"] = "english"

# 保存CSV
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"✅ 转换完成！共 {len(df)} 篇文献 → {csv_path}")