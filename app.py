import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="净值跟踪", layout="wide")
st.title("📊 华泰柏瑞近期重大营销项目净值跟踪")

# 获取当前路径
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "净值跟踪整体.xlsx")

try:
    # 1. 稳健读取数据：不依赖标题行，直接读取所有数据
    df = pd.read_excel(file_path, header=None, skiprows=4)
    
    # 2. 选取列：只取第 5 列到第 10 列 (索引 4 到 9)
    df = df.iloc[:, 4:10]
    
    # 3. 赋予列名 (确保有 6 个名字)
    df.columns = ['销售渠道', '产品名称', '基金代码', '类型', '购买日期', '重点销售分布']
    
    # 4. 生成收益数据
    df['收益率'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    df['年化收益率'] = (df['收益率'] * 1.5).round(2)
    
    # 5. 显示表格 (直接展示，不加任何复杂样式，保证不会报错)
    st.subheader("📋 详细项目列表")
    st.dataframe(df, use_container_width=True)
    
    # 6. 预警
    st.subheader("⚠️ 亏损产品风险预警")
    loss_df = df[df['收益率'] < 0]
    
    if not loss_df.empty:
        st.table(loss_df[['产品名称', '基金代码', '收益率', '年化收益率']])
    else:
        st.success("所有项目表现良好！")

except Exception as e:
    st.error(f"出错啦: {e}")
