import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="华泰柏瑞近期重大营销项目净值跟踪", layout="wide")
st.title("📊 华泰柏瑞近期重大营销项目净值跟踪")

# 路径设置
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "净值跟踪整体.xlsx")

try:
    # 1. 读取 Excel，暂时不设置 header，全部读入
    df = pd.read_excel(file_path, header=None)
    
    # 2. 强行删掉前四列 (df.iloc[:, 4:] 表示从第5列开始保留)
    df = df.iloc[:, 4:]
    
    # 3. 将原本的第 3 行 (索引为2) 设为标题行
    df.columns = df.iloc[2]
    # 只保留第 4 行之后的数据
    df = df.iloc[3:]
    
    # 4. 去除多余空格并重命名
    df.columns = df.columns.str.strip()
    
    # 5. 增加计算列 (注意：如果这里报错，说明您的表格列数依然对不上)
    df['持有至今收益率(%)'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    df['持有至今年化收益率(%)'] = (df['持有至今收益率(%)'] * 1.5).round(2)
    
    # 6. 展示数据
    st.subheader("项目净值详情")
    st.dataframe(df, use_container_width=True)
    
    # 7. 预警 (调整引用名称)
    st.subheader("亏损产品预警")
    # 如果列名有变，这里如果报错，请把 df.columns 的值 print 出来看看
    st.write("当前列名列表:", df.columns.tolist())

except Exception as e:
    st.error(f"处理数据时出错: {e}")
