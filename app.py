import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="华泰柏瑞营销净值跟踪", layout="wide")
st.title("📊 华泰柏瑞全渠道近期重大营销项目净值跟踪")

# 路径设置
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "净值跟踪整体.xlsx")

try:
    # 1. 读取数据，假设前两行是介绍，第三行是实际列名
    df = pd.read_excel(file_path, header=2)
    
    # 2. 强制重新命名列，确保代码逻辑绝对准确（请确保您的Excel列顺序与此一致）
    df.columns = ['销售渠道', '产品', '基金代码', '类型', '购买日期', '重点销售人员网点分布']
    
    # 3. 核心计算逻辑
    # 假设当前收益率为随机数（您可以替换为您真实的计算公式）
    df['持有至今收益率(%)'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    # 假设年化收益率计算：持有至今收益率 * 1.5 (示例公式，您可按需调整)
    df['持有至今年化收益率(%)'] = (df['持有至今收益率(%)'] * 1.5).round(2)
    
    # 4. 展示表格
    st.subheader("项目净值详情")
    st.dataframe(df, use_container_width=True)
    
    # 5. 亏损预警优化
    st.subheader("亏损产品预警")
    loss_df = df[df['持有至今收益率(%)'] < 0]
    if not loss_df.empty:
        st.warning("以下产品收益为负，请关注：")
        st.table(loss_df[['产品', '基金代码', '持有至今收益率(%)', '持有至今年化收益率(%)']])
    else:
        st.success("目前所有营销项目收益均为正！")

except Exception as e:
    st.error(f"代码运行错误，请检查 Excel 列名是否与代码对应: {e}")
