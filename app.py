import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="华泰柏瑞净值跟踪", layout="wide")
st.title("📊 华泰柏瑞近期重大营销项目净值跟踪")

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "净值跟踪整体.xlsx")

try:
    # 1. 自动寻找标题行：读取前 10 行，自动找到包含“产品”或“销售渠道”的那一行作为标题
    df = pd.read_excel(file_path, header=None)
    header_row = 0
    for i in range(min(10, len(df))):
        if '产品' in df.iloc[i].values or '销售渠道' in df.iloc[i].values:
            header_row = i
            break
    
    df = pd.read_excel(file_path, header=header_row)
    
    # 2. 清洗数据：只保留您需要的列，排除掉所有叫 "Unnamed" 的空白列
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # 3. 核心修正：找到真正的“当前收益率”和“年化收益率”列
    # 程序会根据关键字自动定位，不再依赖位置索引
    gain_col = [c for c in df.columns if '收益' in str(c) and '%' in str(c)][0]
    annual_col = [c for c in df.columns if '年化' in str(c)][0]
    
    # 4. 显示
    st.subheader("📋 详细项目列表")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("⚠️ 亏损产品风险预警")
    loss_df = df[df[gain_col] < 0]
    
    if not loss_df.empty:
        st.table(loss_df[[c for c in df.columns if '产品' in str(c) or '代码' in str(c)] + [gain_col, annual_col]])
    else:
        st.success("所有项目目前表现良好！")

except Exception as e:
    st.error("数据解析失败，请检查 Excel 表头是否包含关键字：'产品'、'收益率(%)'、'年化'")
    st.write(f"详细错误: {e}")
