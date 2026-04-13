import pandas as pd

# ====================== 配置（不用改，直接运行）======================
INPUT_FILE = "stage1_included_final.csv"       # 输入文件
OUTPUT_INCLUDED = "included_final.csv"        # 筛后留下的文件
OUTPUT_EXCLUDED = "excluded_final.csv"        # 被筛掉的文件（带原因）
# ====================================================================

def clean_text(s):
    """统一处理空值、空白字符"""
    if pd.isna(s):
        return ""
    return str(s).strip().lower()

def run_rescreen(df):
    """
    复筛主逻辑：按摘要筛选
    返回：状态 + 剔除原因
    """
    included_list = []
    excluded_list = []

    # 遍历每一行文献
    for idx, row in df.iterrows():
        title = clean_text(row.get("TI", ""))
        abstract = clean_text(row.get("AB", ""))
        doc_type = clean_text(row.get("DT", ""))

        # ==================== 复筛规则（你的原有思路） ====================
        reason = ""

        # 规则1：无摘要 → 剔除
        if abstract == "":
            reason = "E1 - 无摘要"

        # 规则2：非期刊文章/综述 → 剔除（保留 Article, Review）
        elif doc_type not in ["article", "review"]:
            reason = "E2 - 文献类型不符"

        # 规则3：必须包含研究方法关键词（可自己增删）
        elif not any(k in abstract for k in [
            "lstm", "gru", "rnn", "transformer", "cnn",
            "long short-term memory", "attention", "prediction"
        ]):
            reason = "E3 - 方法不符"

        # 规则4：必须包含实验/结果/验证 → 保证质量
        elif not any(k in abstract for k in [
            "experiment", "result", "validation", "test", "accuracy",
            "实验", "结果", "验证", "预测"
        ]):
            reason = "E4 - 无实验/结果/验证"

        # ==================== 筛选结束 ====================
        if reason:
            # 被剔除：添加原因
            row_dict = dict(row)
            row_dict["剔除原因"] = reason
            excluded_list.append(row_dict)
        else:
            # 被保留
            included_list.append(dict(row))

    return included_list, excluded_list

def main():
    print("正在读取文献数据：", INPUT_FILE)
    df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")

    # 执行复筛
    included, excluded = run_rescreen(df)

    # 转DataFrame
    df_included = pd.DataFrame(included)
    df_excluded = pd.DataFrame(excluded)

    # 保存文件
    df_included.to_csv(OUTPUT_INCLUDED, index=False, encoding="utf-8-sig")
    df_excluded.to_csv(OUTPUT_EXCLUDED, index=False, encoding="utf-8-sig")

    # 输出结果
    print("\n===== 复筛完成 =====")
    print(f"✅ 保留文献：{len(df_included)} 条 → {OUTPUT_INCLUDED}")
    print(f"❌ 剔除文献：{len(df_excluded)} 条 → {OUTPUT_EXCLUDED}")

    if len(df_excluded) > 0:
        print("\n剔除原因统计：")
        print(df_excluded["剔除原因"].value_counts())

if __name__ == "__main__":
    main()
