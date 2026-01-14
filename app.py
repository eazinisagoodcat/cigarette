import streamlit as st
import pandas as pd

st.set_page_config(page_title="数据对比工具", layout="wide")

st.title("📊 参数对比系统")

# 1. 上传文件
uploaded_file = st.file_uploader("请上传 Excel 文件", type=["xlsx", "xls"])

if uploaded_file:
    # 读取数据
    df = pd.read_excel(uploaded_file)
    id_column = df.columns[0]  # 假设第一列是代号
    
    # 2. 选择对比代号
    st.sidebar.header("对比设置")
    selected_ids = st.sidebar.multiselect(
        "选择要对比的代号（限2个）",
        options=df[id_column].unique(),
        max_selections=2
    )
    
    if len(selected_ids) == 2:
        # 筛选数据
        comparison_df = df[df[id_column].isin(selected_ids)]
        
        # 3. 数据转置以便垂直对比（更清晰）
        comparison_df = comparison_df.set_index(id_column).T
        
        st.subheader(f"🔍 {selected_ids[0]} vs {selected_ids[1]}")
        
        # 增加高亮显示不同之处的逻辑
        def highlight_diff(data):
            attr = 'background-color: #ffcccc' # 差异高亮颜色
            is_diff = data[selected_ids[0]] != data[selected_ids[1]]
            return [attr if is_diff.any() else '' for _ in data]

        st.table(comparison_df.style.highlight_max(axis=1, color='lightgreen')) 
        
    else:
        st.info("请在左侧边栏选择 2 个代号进行对比。")
