import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="销售业绩小程序", layout="wide")
st.title("📊 销售基金产品业绩追踪")

# 读取文件
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "净值跟踪整体.xlsx")

try:
    # 读取 Excel
    df = pd.read_excel(file_path, header=2)
    df.columns = df.columns.str.strip() # 去除列名空格
    
    # 模拟收益率（您可以根据需要修改）
    df['当前收益率(%)'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    
    # 展示主表格
    st.subheader("全部数据列表")
    st.dataframe(df, use_container_width=True)
    
    # 添加一个简单的筛选功能
    st.subheader("亏损产品预警")
    loss_df = df[df['当前收益率(%)'] < 0]
    if not loss_df.empty:
        st.warning("发现以下产品收益为负，请关注：")
        st.table(loss_df[['产品', '基金代码', '当前收益率(%)']])
    else:
        st.success("目前所有产品收益均为正，表现良好！")

except Exception as e:
    st.error(f"小程序加载错误: {e}")
