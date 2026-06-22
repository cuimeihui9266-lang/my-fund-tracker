import streamlit as st
import pandas as pd
import numpy as np

# 1. 设置页面
st.set_page_config(page_title="销售业绩跟踪小程序", layout="wide")
st.title("📊 销售基金产品业绩追踪")

# 2. 读取数据
@st.cache_data
def load_data():
    df = pd.read_excel("净值跟踪整体.xlsx", skiprows=2)
    df.columns = ['销售渠道', '产品名称', '基金代码', '类型', '购买日期', '重点销售网点']
    # 模拟净值计算 (实际中需接入基金净值API)
    df['购买日期'] = pd.to_datetime(df['购买日期'], format='%Y%m%d')
    df['当前收益率(%)'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    df['年化收益率(%)'] = (df['当前收益率(%)'] / 1.5).round(2) # 模拟计算
    return df

data = load_data()

# 3. 筛选面板
st.sidebar.header("筛选器")
channel = st.sidebar.multiselect("选择销售渠道", data['销售渠道'].unique())
if channel:
    data = data[data['销售渠道'].isin(channel)]

# 4. 展示表格
st.subheader("当前持仓产品业绩")
st.dataframe(data.style.background_gradient(subset=['当前收益率(%)'], cmap='RdYlGn'), use_container_width=True)

# 5. 售后提醒：红色高亮亏损产品
st.subheader("⚠️ 需重点关注 (亏损产品)")
loss_df = data[data['当前收益率(%)'] < 0]
st.table(loss_df[['产品名称', '基金代码', '当前收益率(%)', '重点销售网点']])