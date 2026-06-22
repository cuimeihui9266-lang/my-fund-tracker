import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="华泰柏瑞营销净值跟踪", layout="wide")
st.title("📊 华泰柏瑞近期重大营销项目净值跟踪")

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "净值跟踪整体.xlsx")

try:
    # 直接读取整个文件，不设定标题行
    df = pd.read_excel(file_path, header=None)
    
    # --- 核心逻辑 ---
    # 根据您之前成功的截图，我们确定：
    # 销售渠道在第 5 列 (索引 4)
    # 产品在第 6 列 (索引 5)
    # 基金代码在第 7 列 (索引 6)
    # 类型在第 8 列 (索引 7)
    # 购买日期在第 9 列 (索引 8)
    # 重点销售分布在第 10 列 (索引 9)
    # 当前收益率在第 11 列 (索引 10)
    # 年化收益率在第 12 列 (索引 11)
    
    # 取出这 8 列数据
    data = df.iloc[3:, [4, 5, 6, 7, 8, 9, 10, 11]].copy()
    data.columns = ['销售渠道', '产品', '基金代码', '类型', '购买日期', '网点分布', '当前收益', '年化收益']
    
    # 确保收益率是数字格式
    data['当前收益'] = pd.to_numeric(data['当前收益'], errors='coerce')
    data['年化收益'] = pd.to_numeric(data['年化收益'], errors='coerce')
    
    st.subheader("📋 详细项目列表")
    st.dataframe(data, use_container_width=True)
    
    st.subheader("⚠️ 亏损产品风险预警")
    loss_df = data[data['当前收益'] < 0]
    
    if not loss_df.empty:
        st.table(loss_df)
    else:
        st.success("所有项目目前表现良好！")

except Exception as e:
    st.error("无法读取数据，请检查 Excel 文件是否正确上传。")
    st.write(f"技术错误代码: {e}")
