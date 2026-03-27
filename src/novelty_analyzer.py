import pandas as pd
import numpy as np

# --------------------------
# 1. 读取数据（确保文件在同一路径下）
# --------------------------
# 筛选前原始数据
df_raw = pd.read_csv('merged_with_citations.csv', encoding='gbk')  # 原始数据编码为gbk
# 初筛后数据
df_stage1 = pd.read_csv('screened_stage1.csv', encoding='utf-8')
# 复筛后最终数据
df_final = pd.read_csv('screened_final.csv', encoding='utf-8')

# --------------------------
# 2. 定义对比维度（对应你查新报告的 方法/数据/应用/指标/局限）
# --------------------------
comparison_dimensions = {
    '数据规模': ['总记录数', '唯一引用文献数', '唯一被引文献数', '数据保留率(%)'],
    '文献结构': ['期刊占比(%)', '硕士论文占比(%)', '外文期刊占比(%)', '中文文献占比(%)', '英文文献占比(%)'],
    '时间特征': ['最早年份', '最新年份', '2024年占比(%)', '2025年占比(%)', '2026年占比(%)'],
    '数据质量': ['题名完整率(%)', '作者完整率(%)', '年份完整率(%)', 'DOI完整率(%)', '摘要完整率(%)'],
    '引用网络': ['平均引用次数/篇', '引用网络密度', '核心被引节点数'],
    '筛选特征': ['初筛排除率(%)', '复筛排除率(%)', '最终保留率(%)']
}

# --------------------------
# 3. 定义统计函数
# --------------------------
def calculate_metrics(df, df_raw_total=None, stage_name='raw'):
    """计算单份数据的对比指标"""
    metrics = {}
    total = len(df)
    
    # 1. 数据规模
    metrics['总记录数'] = total
    metrics['唯一引用文献数'] = df['citing_paper'].nunique() if 'citing_paper' in df.columns else 0
    metrics['唯一被引文献数'] = df['cited_paper'].nunique() if 'cited_paper' in df.columns else 0
    if df_raw_total is not None and stage_name != 'raw':
        metrics['数据保留率(%)'] = round((total / df_raw_total) * 100, 2)
    else:
        metrics['数据保留率(%)'] = 100.00  # 原始数据保留率100%
    
    # 2. 文献结构
    if '来源库' in df.columns:
        source_dist = df['来源库'].value_counts(normalize=True) * 100
        metrics['期刊占比(%)'] = round(source_dist.get('期刊', 0), 2)
        metrics['硕士论文占比(%)'] = round(source_dist.get('硕士', 0), 2)
        metrics['外文期刊占比(%)'] = round(source_dist.get('外文期刊', 0), 2)
    else:
        metrics['期刊占比(%)'] = metrics['硕士论文占比(%)'] = metrics['外文期刊占比(%)'] = 0.00
    
    if '语言' in df.columns:
        lang_dist = df['语言'].value_counts(normalize=True) * 100
        metrics['中文文献占比(%)'] = round(lang_dist.get('chinese', 0), 2)
        metrics['英文文献占比(%)'] = round(lang_dist.get('english', 0), 2)
    else:
        metrics['中文文献占比(%)'] = metrics['英文文献占比(%)'] = 0.00
    
    # 3. 时间特征
    if '年份' in df.columns:
        valid_years = df['年份'].dropna()
        if len(valid_years) > 0:
            metrics['最早年份'] = int(valid_years.min())
            metrics['最新年份'] = int(valid_years.max())
            year_dist = valid_years.astype(int).value_counts(normalize=True) * 100
            metrics['2024年占比(%)'] = round(year_dist.get(2024, 0), 2)
            metrics['2025年占比(%)'] = round(year_dist.get(2025, 0), 2)
            metrics['2026年占比(%)'] = round(year_dist.get(2026, 0), 2)
        else:
            metrics['最早年份'] = metrics['最新年份'] = metrics['2024年占比(%)'] = metrics['2025年占比(%)'] = metrics['2026年占比(%)'] = 0
    else:
        metrics['最早年份'] = metrics['最新年份'] = metrics['2024年占比(%)'] = metrics['2025年占比(%)'] = metrics['2026年占比(%)'] = 0
    
    # 4. 数据质量
    core_fields = ['题名', '作者', '年份', 'DOI', '摘要']
    for field in core_fields:
        if field in df.columns:
            complete_rate = (1 - df[field].isnull().sum() / total) * 100
            metrics[f'{field}完整率(%)'] = round(complete_rate, 2)
        else:
            metrics[f'{field}完整率(%)'] = 0.00
    
    # 5. 引用网络
    if 'citing_paper' in df.columns and 'cited_paper' in df.columns:
        unique_citing = df['citing_paper'].nunique()
        unique_cited = df['cited_paper'].nunique()
        total_edges = len(df)
        metrics['平均引用次数/篇'] = round(total_edges / unique_citing, 2) if unique_citing > 0 else 0.00
        metrics['引用网络密度'] = round(total_edges / (unique_citing * unique_cited), 4) if unique_citing > 0 and unique_cited > 0 else 0.00
        metrics['核心被引节点数'] = unique_cited
    else:
        metrics['平均引用次数/篇'] = metrics['引用网络密度'] = metrics['核心被引节点数'] = 0.00
    
    # 6. 筛选特征（仅适用于初筛/复筛）
    if stage_name == 'stage1' and 'stage1_status' in df.columns:
        exclude_rate = (df['stage1_status'] == 'exclude').sum() / total * 100
        metrics['初筛排除率(%)'] = round(exclude_rate, 2)
        metrics['复筛排除率(%)'] = None  # 初筛阶段无复筛排除率
    elif stage_name == 'final' and 'stage2_status' in df.columns:
        if 'stage1_status' in df.columns:
            stage1_exclude = (df['stage1_status'] == 'exclude').sum() / total * 100
            metrics['初筛排除率(%)'] = round(stage1_exclude, 2)
        stage2_exclude = (df['stage2_status'] == 'exclude').sum() / total * 100
        metrics['复筛排除率(%)'] = round(stage2_exclude, 2)
    else:
        metrics['初筛排除率(%)'] = metrics['复筛排除率(%)'] = 0.00
    
    if stage_name == 'final':
        metrics['最终保留率(%)'] = round((total / len(df_raw)) * 100, 2)
    else:
        metrics['最终保留率(%)'] = None
    
    return metrics

# --------------------------
# 4. 计算各阶段指标
# --------------------------
raw_total = len(df_raw)
metrics_raw = calculate_metrics(df_raw, stage_name='raw')
metrics_stage1 = calculate_metrics(df_stage1, df_raw_total=raw_total, stage_name='stage1')
metrics_final = calculate_metrics(df_final, df_raw_total=raw_total, stage_name='final')

# --------------------------
# 5. 构建对比表 DataFrame
# --------------------------
# 合并所有指标
all_metrics = []
for dim, fields in comparison_dimensions.items():
    for field in fields:
        row = {
            '对比维度': dim,
            '指标名称': field,
            '筛选前(原始数据)': metrics_raw.get(field, None),
            '初筛后数据': metrics_stage1.get(field, None),
            '复筛后(最终数据)': metrics_final.get(field, None)
        }
        all_metrics.append(row)

df_comparison = pd.DataFrame(all_metrics)

# --------------------------
# 6. 输出为 CSV（用于查新报告）
# --------------------------
output_file = 'literature_screening_comparison.csv'
df_comparison.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"✅ 对比表已生成并保存为: {output_file}")
print(f"📊 共包含 {len(df_comparison)} 个对比指标，覆盖 5 大维度")
print("📋 可直接用于 novelty_search_v0.md 的「对比表」章节")