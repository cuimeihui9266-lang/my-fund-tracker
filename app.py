import streamlit as st
import pandas as pd
import numpy as np

# 页面设置
st.set_page_config(page_title="销售业绩跟踪小程序", layout="wide")
st.title("📊 销售基金产品业绩追踪")

# 1. 尝试读取数据
try:
    # 这一行就是 load_data 的核心逻辑
    df = pd.read_excel("净值跟踪整体.xlsx", header=2)
    
    # 强制将列名重命名为简单的 A, B, C... 以防止任何列名不匹配报错
    df.columns = ['A', 'B', 'C', 'D', 'E', 'F']
    
    # 模拟计算数据
    df['收益率'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    
    st.success("数据加载成功！")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"读取 Excel 出错了，错误信息是: {e}")
    st.info("请检查 Excel 文件是否在 GitHub 根目录，且文件名是否完全一致。")
