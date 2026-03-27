# CNKI 格式 TXT 转 CSV（适配你的文件）
import csv
import logging

# 日志配置
logging.basicConfig(level=logging.WARNING,
                    filename='./log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

def convert_cnki_txt_to_csv(txtpath, csvfile):
    # 定义要提取的字段顺序（对应你的 CNKI 格式）
    fieldnames = [
        "SrcDatabase", "Title", "Author", "Organ", "Source",
        "Summary", "PubTime", "Fund", "Year", "DOI"
    ]

    current = {}
    try:
        with open(txtpath, 'r', encoding='utf-8') as f_in:
            lines = f_in.readlines()

        with open(csvfile, 'w', newline='', encoding='utf-8-sig') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # 按前缀匹配字段
                if line.startswith("SrcDatabase-来源库:"):
                    current["SrcDatabase"] = line.split(":", 1)[1].strip()
                elif line.startswith("Title-题名:"):
                    current["Title"] = line.split(":", 1)[1].strip()
                elif line.startswith("Author-作者:"):
                    current["Author"] = line.split(":", 1)[1].strip()
                elif line.startswith("Organ-单位:"):
                    current["Organ"] = line.split(":", 1)[1].strip()
                elif line.startswith("Source-文献来源:"):
                    current["Source"] = line.split(":", 1)[1].strip()
                elif line.startswith("Summary-摘要:"):
                    current["Summary"] = line.split(":", 1)[1].strip()
                elif line.startswith("PubTime-发表时间:"):
                    current["PubTime"] = line.split(":", 1)[1].strip()
                elif line.startswith("Fund-基金:"):
                    current["Fund"] = line.split(":", 1)[1].strip()
                elif line.startswith("Year-年:"):
                    current["Year"] = line.split(":", 1)[1].strip()
                elif line.startswith("DOI-DOI:"):
                    current["DOI"] = line.split(":", 1)[1].strip()

                # 遇到新一篇 SrcDatabase 时写入上一篇
                if line.startswith("SrcDatabase-来源库:") and current:
                    if len(current) > 1:  # 确保不是空记录
                        writer.writerow(current)
                        current = {}

            # 写入最后一篇
            if current:
                writer.writerow(current)

        print(f"✅ 转换完成！文件已保存到：{csvfile}")

    except Exception as e:
        logging.error(f"转换失败：{str(e)}")
        print("❌ 出错了，请查看 log.txt")

# ====================== 在这里改你的文件名 ======================
txtpath = "CNKI.txt"        # 你的 CNKI 导出文件
csvfile = "raw_data.csv"     # 输出 CSV
# ==============================================================

convert_cnki_txt_to_csv(txtpath, csvfile)