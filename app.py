import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="华泰柏瑞营销净值跟踪", layout="wide")
st.title("📊 华泰柏瑞近期重大营销项目净值跟踪")

# 路径设置
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "净值跟踪整体.xlsx")

try:
    # 1. 跳过前 3 行读取数据 (根据之前的截图，这能正确跳过标题行)
    df = pd.read_excel(file_path, header=None, skiprows=3)
    
    # 2. 强制取前 8 列并直接重命名，彻底抹平 Excel 原本列名的干扰
    # 确保您的表格至少有 8 列数据
    df = df.iloc[:, :8]
    df.columns = ['销售渠道', '产品', '基金代码', '类型', '购买日期', '网点分布', '当前收益', '年化收益']
    
    # 3. 数据清洗：确保收益列为数字，非数字转为 0
    df['当前收益'] = pd.to_numeric(df['当前收益'], errors='coerce').fillna(0)
    df['年化收益'] = pd.to_numeric(df['年化收益'], errors='coerce').fillna(0)
    
    # 4. 显示表格（加上百分号格式）
    display_df = df.copy()
    display_df['当前收益'] = display_df['当前收益'].apply(lambda x: f"{x:.2f}%")
    display_df['年化收益'] = display_df['年化收益'].apply(lambda x: f"{x:.2f}%")
    
    st.subheader("📋 详细项目列表")
    st.dataframe(display_df, use_container_width=True)
    
    # 5. 预警
    st.subheader("⚠️ 亏损产品风险预警")
    loss_df = df[df['当前收益'] < 0]
    
    if not loss_df.empty:
        st.error(f"监测到 {len(loss_df)} 个产品处于亏损状态：")
        st.table(loss_df[['产品', '基金代码', '当前收益', '年化收益']])
    else:
        st.success("所有项目目前表现良好，暂无亏损产品！")

except Exception as e:
    st.error("数据加载错误，请确认 Excel 文件在根目录且至少有 8 列数据。")
    st.write(f"调试信息: {e}")
