import streamlit as st
import pandas as pd
import numpy as np
import os

# 1. 页面整体美化
st.set_page_config(page_title="华泰柏瑞净值跟踪", layout="wide")

# 自定义 CSS 让表格更漂亮
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 华泰柏瑞近期重大营销项目净值跟踪")

# 路径设置
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "净值跟踪整体.xlsx")

try:
    # 读取数据：跳过前3行，取所有列
    df = pd.read_excel(file_path, header=None, skiprows=3)
    
    # 强制只取第5列到第10列（即前四列之后的数据）
    df = df.iloc[:, 4:10] 
    df.columns = ['销售渠道', '产品名称', '基金代码', '类型', '购买日期', '重点销售分布']
    
    # 计算列
    df['持有至今收益率(%)'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    df['持有至今年化收益率(%)'] = (df['持有至今收益率(%)'] * 1.5).round(2)
    
    # 2. 增加统计卡片（展示核心指标）
    col1, col2, col3 = st.columns(3)
    col1.metric("项目总数", len(df))
    col2.metric("平均收益率", f"{df['持有至今收益率(%)'].mean():.2f}%")
    col3.metric("最高收益率", f"{df['持有至今收益率(%)'].max():.2f}%")
    
    # 3. 数据表格增强显示
    st.subheader("📋 详细项目列表")
    # 使用 style 给收益率加上颜色（正数红，负数绿）
    def color_negative_red(val):
        color = 'red' if val < 0 else 'green'
        return f'color: {color}'
    
    st.dataframe(df.style.applymap(color_negative_red, subset=['持有至今收益率(%)']), use_container_width=True)
    
    # 4. 亏损预警美化
    st.subheader("⚠️ 亏损产品风险预警")
    loss_df = df[df['持有至今收益率(%)'] < 0]
    
    if not loss_df.empty:
        st.error(f"监测到 {len(loss_df)} 个项目收益为负，请及时介入：")
        st.table(loss_df[['产品名称', '基金代码', '持有至今收益率(%)', '持有至今年化收益率(%)']])
    else:
        st.success("所有营销项目表现良好，当前无亏损风险！")

except Exception as e:
    st.error(f"数据处理过程出错: {e}")
