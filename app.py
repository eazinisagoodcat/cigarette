import streamlit as st
import pandas as pd

# 页面配置
st.set_page_config(page_title="参数对比系统", layout="wide")

st.title("📊 参数对比系统")

# 1. 上传文件
uploaded_file = st.file_uploader("第一步：请上传 Excel 文件", type=["xlsx", "xls"])

if uploaded_file:
    # 读取数据
    df = pd.read_excel(uploaded_file)
    id_column = df.columns[0]  # 默认第一列为代号列
    all_ids = df[id_column].unique().tolist()
    
    # 2. 侧边栏：拆分为两个独立的下拉选择框
    st.sidebar.header("第二步：选择对比项")
    
    # 第一个选项框（默认选第1个）
    id_1 = st.sidebar.selectbox("选择第一个代号", options=all_ids, index=0)
    
    # 第二个选项框（默认选第2个）
    # 为了防止两个框选到同一个，我们可以做个简单的处理，或者让用户自己决定
    id_2 = st.sidebar.selectbox("选择第二个代号", options=all_ids, index=min(1, len(all_ids)-1))
    
    if id_1 == id_2:
        st.warning("⚠️ 你选择了两个相同的代号，对比结果将完全一致。")

    # 3. 提取并处理数据
    # 按照选中的顺序重新排序，确保对比表左侧是 id_1，右侧是 id_2
    selected_df = df[df[id_column].isin([id_1, id_2])]
    comparison_df = selected_df.set_index(id_column).reindex([id_1, id_2]).T
    
    st.subheader(f"🔍 对比详情：{id_1} vs {id_2}")

    # 4. 定义样式函数：仅修改字体颜色
    def highlight_diff_text(row):
        # row.iloc[0] 是第一个代号的值，row.iloc[1] 是第二个
        if row.iloc[0] != row.iloc[1]:
            # 'color: red' 修改字体颜色，'font-weight: bold' 加粗显示更明显
            return ['color: red; font-weight: bold', 'color: red; font-weight: bold']
        else:
            return ['', '']

    # 5. 显示表格
    # 使用 st.dataframe 以获得更好的交互体验，或者 st.table 展示完整静态表格
    st.table(comparison_df.style.apply(highlight_diff_text, axis=1))

    # 补充：差异说明
    st.caption("注：参数值不同的项已自动标记为红色加粗字体。")

else:
    st.info("💡 请先上传 Excel 文件以开始使用。")
