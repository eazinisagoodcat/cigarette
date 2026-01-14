import streamlit as st
import pandas as pd

st.set_page_config(page_title="数据对比工具", layout="wide")

st.title("📊 参数对比系统")

uploaded_file = st.file_uploader("请上传 Excel 文件", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    id_column = df.columns[0] 
    
    st.sidebar.header("对比设置")
    selected_ids = st.sidebar.multiselect(
        "选择要对比的代号（限2个）",
        options=df[id_column].unique(),
        max_selections=2
    )
    
    if len(selected_ids) == 2:
        # 1. 提取选中的两行数据
        comparison_df = df[df[id_column].isin(selected_ids)]
        
        # 2. 为了方便对比，将其转置（行变列，参数变成纵向排列）
        # 确保顺序按照用户选择的顺序排列
        comparison_df = comparison_df.set_index(id_column).reindex(selected_ids).T
        
        st.subheader(f"🔍 {selected_ids[0]} vs {selected_ids[1]}")

        # --- 核心修改部分：定义高亮函数 ---
        def highlight_diff(row):
            # 如果这一行的两个单元格数值不相等
            if row.iloc[0] != row.iloc[1]:
                return ['background-color: #FFCCCC', 'background-color: #FFCCCC'] # 红色背景
            else:
                return ['', ''] # 保持原色

        # 应用样式并显示
        st.table(comparison_df.style.apply(highlight_diff, axis=1))
        # ------------------------------

    else:
        st.info("请在左侧边栏选择 2 个代号进行对比。")
