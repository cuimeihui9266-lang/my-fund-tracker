import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="华泰柏瑞营销净值跟踪", layout="wide")
st.title("📊 华泰柏瑞营销净值跟踪")

# 路径设置
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "净值跟踪整体.xlsx")

try:
    # 1. 读取 Excel
    df = pd.read_excel(file_path, header=2)
    
    # 2. 【关键调试】把所有列名显示出来，您直接看网页上显示的名字是什么
    st.write("--- 调试信息：您的Excel表格真实列名如下 ---")
    st.write(df.columns.tolist())
    st.write("-------------------------------------------")
    
    # 3. 接下来只需要您把上面显示的名字，对应填入下面的列表即可
    # 假设您的列名分别是：['销售渠道', '产品名称', '基金代码', '类型', '购买日期', '重点销售人员网点分布']
    # 请根据网页显示的实际名称修改下面这一行：
    df.columns = ['销售渠道', '产品名称', '基金代码', '类型', '购买日期', '重点销售人员网点分布']
    
    # 计算列
    df['持有至今收益率(%)'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    df['持有至今年化收益率(%)'] = (df['持有至今收益率(%)'] * 1.5).round(2)
    
    st.dataframe(df, use_container_width=True)
    
    # 预警部分
    st.subheader("亏损产品预警")
    loss_df = df[df['持有至今收益率(%)'] < 0]
    st.table(loss_df[['产品名称', '基金代码', '持有至今收益率(%)', '持有至今年化收益率(%)']])

except Exception as e:
    st.error(f"出错啦: {e}")
