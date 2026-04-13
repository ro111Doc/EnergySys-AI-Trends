import pandas as pd
from pathlib import Path

# ================= 路径自动化配置 =================
current_script_path = Path(__file__).resolve()
project_root = current_script_path.parent.parent

# 文件夹定义：统一使用 data 目录
data_dir = project_root / "data"
src_dir = current_script_path.parent

# 确保 data 文件夹存在
if not data_dir.exists():
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"已自动创建目录: {data_dir}")

# 查找原始文件
input_file_name = "wos_literature.csv"
search_locations = [src_dir / input_file_name, project_root / input_file_name, data_dir / input_file_name]

INPUT_PATH = None
for p in search_locations:
    if p.exists():
        INPUT_PATH = p
        break

# 输出文件定义（全部指向 data 文件夹，文件名已优化）
OUTPUT_INCLUDED_PATH = data_dir / "stage1_included_final.csv"
OUTPUT_EXCLUDED_PATH = data_dir / "stage1_excluded_initial_screen.csv"


# ================= 筛选逻辑 (基于规则) =================
def screen_logic(row):
    # WOS字段映射: TI=Title, AB=Abstract, PY=Year
    title = str(row.get('TI', "")).lower()
    abstract = str(row.get('AB', "")).lower()
    content = title + " " + abstract

    try:
        year = int(float(row.get('PY', 0)))
    except:
        year = 0

    # 1. 时间过滤 (E4: 2015-2025)
    if not (2015 <= year <= 2025):
        return "exclude", "E4 - 时间不符"

    # 2. 关键词定义
    lstm_keywords = ["lstm", "long short-term memory", "bi-lstm", "gru", "rnn", "attention"]
    task_keywords = ["load forecasting", "load prediction", "electric load", "power load", "负荷预测"]

    # 3. 排除逻辑 (E1 & E3)
    if not any(k in content for k in task_keywords):
        return "exclude", "E1 - 非负荷预测领域"

    if not any(k in content for k in lstm_keywords):
        return "exclude", "E3 - 方法不符 (非LSTM/DL)"

    return "include", ""


def main():
    if not INPUT_PATH:
        print("错误: 找不到 wos_literature.csv 文件")
        return

    print(f"读取文件: {INPUT_PATH}")

    # 读取数据
    df = pd.read_csv(INPUT_PATH, encoding='utf-8-sig')
    original_count = len(df)
    print(f"原始数据量: {original_count} 条")

    # 执行筛选
    results = df.apply(screen_logic, axis=1)
    df['decision'] = [r[0] for r in results]
    df['reason_code'] = [r[1] for r in results]

    # --- 数据拆分 ---
    # 1. 初筛剔除的文献
    df_excluded = df[df['decision'] == 'exclude'].copy()

    # 2. 初筛通过的文献
    df_included = df[df['decision'] == 'include'].copy()
    # 移除辅助列
    df_included = df_included.drop(columns=['decision', 'reason_code'])

    # --- 保存结果到 data 文件夹 ---
    df_included.to_csv(OUTPUT_INCLUDED_PATH, index=False, encoding='utf-8-sig')
    df_excluded.to_csv(OUTPUT_EXCLUDED_PATH, index=False, encoding='utf-8-sig')

    print("\n" + "=" * 30)
    print("处理完成")
    print(f"初筛剔除: {len(df_excluded)} 条")
    print(f"初筛通过: {len(df_included)} 条")
    print("-" * 30)
    print(f"通过名单保存至: {OUTPUT_INCLUDED_PATH.name}")
    print(f"剔除名单保存至: {OUTPUT_EXCLUDED_PATH.name}")
    print("=" * 30)


if __name__ == "__main__":
    main()