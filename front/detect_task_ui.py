import streamlit as st

# ページ全体のレイアウトを中央寄せに
st.set_page_config(layout="centered")

# CSS を埋め込んでスタイルを調整
st.markdown(
    """
    <style>
    /* 背景コンテナ */
    .task-container {
        background-color: #f2f2f2;
        padding: 24px;
        border-radius: 8px;
    }
    /* タイトル */
    .task-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    /* テキストエリア */
    .task-textarea textarea {
        width: 100% !important;
        height: 100px !important;
        padding: 12px !important;
        border-radius: 8px !important;
        border: 1px solid #ccc !important;
        font-size: 16px !important;
        resize: none !important;
    }
    /* ボタンを丸く */
    .stButton>button {
        border-radius: 50% !important;
        width: 80px;
        height: 80px;
        font-size: 32px;
        padding: 0;
    }
    /* ボタン下のキャプション */
    .voice-caption {
        text-align: center;
        margin-top: 8px;
        font-size: 16px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# タイトル
st.markdown('<div class="task-title">タスクを自動で認識</div>', unsafe_allow_html=True)

# テキストエリア（プレースホルダー付き）
st.markdown(
    '<div class="task-textarea">'
    '  <textarea placeholder="文章を入力"></textarea>'
    '</div>',
    unsafe_allow_html=True,
)

# マイクボタンを中央寄せ
col1, col2, col3 = st.columns([1, 0.2, 1])
with col2:
    if st.button("🎤"):
        st.write("音声入力を開始します…")  # 実装はお好みで
    st.markdown('<div class="voice-caption">音声で入力</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
