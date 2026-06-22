import streamlit as st
import pandas as pd
import os

# 1. 页面配置与美化
st.set_page_config(page_title="华泰柏瑞净值跟踪", layout="wide")
st.markdown("""
    <style>
    .metric-card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e9ecef; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 华泰柏瑞近期重大营销项目净值跟踪")

# 2. 数据读取与处理
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "净值跟踪整体.xlsx")

try:
    # 直接按您之前成功的那次逻辑读取（header=2，读取第三行为标题）
    df = pd.read_excel(file_path, header=2)
    
    # 强制清理列名（去空格）
    df.columns = df.columns.str.strip()
    
    # 3. 核心：调用 Excel 原有的列名
    # 这里引用您 Excel 真实表格里的列名，如果报错，请对照 Excel 表头修改引号里的名字
    target_cols = ['销售渠道', '产品', '基金代码', '类型', '购买日期', '重点销售人员网点分布', '当前收益率(%)', '持有至今年化收益率(%)']
    df_display = df[target_cols].copy()
    
    # 4. 格式化百分号
    df_display['当前收益率(%)'] = df_display['当前收益率(%)'].apply(lambda x: f"{x:.2f}%")
    df_display['持有至今年化收益率(%)'] = df_display['持有至今年化收益率(%)'].apply(lambda x: f"{x:.2f}%")
    
    # 5. 展示
    st.subheader("📋 详细项目列表")
    st.dataframe(df_display, use_container_width=True)
    
    # 6. 预警 (预警逻辑用数字列，所以用原始的 df)
    st.subheader("⚠️ 亏损产品风险预警")
    loss_df = df[df['当前收益率(%)'] < 0]
    
    if not loss_df.empty:
        st.error(f"监测到 {len(loss_df)} 个产品处于亏损状态：")
        st.table(loss_df[['产品', '基金代码', '当前收益率(%)', '持有至今年化收益率(%)']])
    else:
        st.success("所有项目目前表现良好，暂无亏损产品！")

except Exception as e:
    st.error("数据加载失败，请检查 Excel 列名是否包含：'当前收益率(%)' 和 '持有至今年化收益率(%)'")
    st.write(f"详细错误: {e}")
