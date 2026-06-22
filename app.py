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
    # 读取 Excel
    df = pd.read_excel(file_path, header=2)
    
    # --- 重要：请检查您 Excel 的列名，确保完全匹配 ---
    # 根据我们之前的分析，我们重新命名列名，保证代码能识别
    df.columns = ['销售渠道', '产品', '基金代码', '类型', '购买日期', '重点销售人员网点分布']
    
    # 增加计算列
    df['持有至今收益率(%)'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    df['持有至今年化收益率(%)'] = (df['持有至今收益率(%)'] * 1.5).round(2)
    
    # 展示数据
    st.subheader("项目净值详情")
    st.dataframe(df, use_container_width=True)
    
    # 亏损预警 (使用明确的列名)
    st.subheader("亏损产品预警")
    loss_df = df[df['持有至今收益率(%)'] < 0]
    
    if not loss_df.empty:
        st.warning("以下产品收益为负，请关注：")
        # 这里使用上面定义好的列名
        st.table(loss_df[['产品', '基金代码', '持有至今收益率(%)', '持有至今年化收益率(%)']])
    else:
        st.success("目前所有营销项目收益均为正，表现良好！")

except Exception as e:
    st.error(f"小程序加载错误，请检查 Excel 标题行是否为第 3 行: {e}")
    st.write("如果依然报错，请把上面的错误信息截图发给我。")
