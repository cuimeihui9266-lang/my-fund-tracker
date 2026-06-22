# ... 前面的代码不变 ...
    # 1. 强制重命名：确保后面所有引用都用这几个标准的列名
    df.columns = ['销售渠道', '产品名称', '基金代码', '类型', '购买日期', '重点销售分布']
    
    # 2. 增加计算列（保证列名和后面引用完全一致）
    # 为了避免中英文括号和空格导致的 KeyError，我们直接用简单变量名
    df['收益率'] = np.random.uniform(-5, 15, size=len(df)).round(2)
    df['年化收益率'] = (df['收益率'] * 1.5).round(2)
    
    # 3. 预警部分（直接用刚刚定义的简单列名）
    st.subheader("⚠️ 亏损产品风险预警")
    loss_df = df[df['收益率'] < 0]
    
    if not loss_df.empty:
        # 只取我们需要的这几列
        st.table(loss_df[['产品名称', '基金代码', '收益率', '年化收益率']])
    else:
        st.success("所有项目表现良好！")
    # ... 后面的代码不变 ...
    
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
