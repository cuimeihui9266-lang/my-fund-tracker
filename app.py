import streamlit as st
import pandas as pd
import numpy as np
import os

# 页面设置
st.set_page_config(page_title="销售业绩跟踪小程序", layout="wide")
st.title("📊 销售基金产品业绩追踪")

# --- 核心数据读取 ---
# 获取当前代码所在的绝对路径，确保能找到 Excel
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "净值跟踪整体.xlsx")

# 调试显示：如果报错，这一行能帮我们看到系统到底在找哪个文件
# st.write(f"正在读取路径: {file_path}")

try:
    # 读取 Excel，header=2 表示第三行是标题行
    df = pd.read_excel(file_path, header=2)
    
    # 强制清理列名中的空格
    df.columns = df.columns.str.strip()
    
    # 为了防止报错，直接强制显示前几列数据
    # 如果系统依然报错找不到列，这能帮你排查
    st.write("文件读取成功，以下是表格数据：")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"读取失败！请检查文件名是否完全正确。错误信息: {e}")
    st.write("当前文件夹下的文件列表:", os.listdir(current_dir))
