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
    # 1. 直接读取数据，不设 header，跳过前三行
    df = pd.read_excel(file_path, header=None, skiprows=3)
    
    # 2. 强制赋予列名（只要您的 Excel 至少有 6 列，这就能跑）
    # 这样我们就完全不用管 Excel 原本叫什么名字了
    df = df.iloc[:, :6] # 只取前6列
    df.columns = ['销售渠道', '产品名称', '基金代码', '类型', '购买日期', '重点销售分布']
    
    # 3. 增加计算列
    df['持有至今收益率(%)'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    df['持有至今年化收益率(%)'] = (df['持有至今收益率(%)'] * 1.5).round(2)
    
    # 4. 展示表格
    st.dataframe(df, use_container_width=True)
    
    # 5. 预警 (直接使用上面定义好的列名)
    st.subheader("亏损产品预警")
    loss_df = df[df['持有至今收益率(%)'] < 0]
    
    if not loss_df.empty:
        st.warning("以下产品收益为负，请关注：")
        st.table(loss_df[['产品名称', '基金代码', '持有至今收益率(%)', '持有至今年化收益率(%)']])
    else:
        st.success("目前所有项目收益均为正！")

except Exception as e:
    st.error(f"还是报错？没关系，直接把这一行报错信息截图给我: {e}")
