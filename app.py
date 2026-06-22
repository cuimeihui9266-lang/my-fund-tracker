import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="华泰柏瑞营销净值跟踪", layout="wide")
st.title("📊 华泰柏瑞近期重大营销项目净值跟踪")

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "净值跟踪整体.xlsx")

try:
    # 1. 自动寻找数据区域：跳过所有空的头部，找到含有“产品”的行作为表头
    df_raw = pd.read_excel(file_path, header=None)
    # 找到含有“产品”关键字的那一行作为索引
    header_idx = df_raw[df_raw.apply(lambda row: row.astype(str).str.contains('产品').any(), axis=1)].index[0]
    
    # 从那一行开始读取
    df = pd.read_excel(file_path, header=header_idx)
    
    # 2. 清洗：删除列名含“Unnamed”的空白列
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # 3. 模拟计算（由于表格目前无净值，先用随机数填充，您可随时替换公式）
    # 逻辑：如果您有净值列，请在这里改成 df['当前收益'] = (df['最新净值'] - df['买入净值']) / df['买入净值']
    df['持有至今收益率'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    df['持有至今年化收益率'] = (df['持有至今收益率'] * 1.5).round(2)
    
    # 4. 显示
    st.subheader("📋 详细项目列表")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("⚠️ 亏损产品风险预警")
    loss_df = df[df['持有至今收益率'] < 0]
    
    if not loss_df.empty:
        st.table(loss_df[['产品', '基金代码', '持有至今收益率', '持有至今年化收益率']])
    else:
        st.success("所有项目目前表现良好！")

except Exception as e:
    st.error("读取失败。请确保您的 Excel 文件中有“产品”这一列。")
    st.write(f"调试信息: {e}")
