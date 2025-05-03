import streamlit as st

# 録音状態の管理
if "is_recording" not in st.session_state:
    st.session_state["is_recording"] = False

# 入力テキスト管理
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

# 送信状態の管理
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False


# トグル関数の定義
def toggle_recording():
    st.session_state["is_recording"] = not st.session_state["is_recording"]


# 送信関数の定義
def submit_task():
    st.session_state["submitted"] = True


# ページ全体のレイアウトを中央寄せに
st.set_page_config(layout="centered")

# タイトル
st.title("タスクを自動で認識")

# テキストエリア
input_text = st.text_area(
    label="文章を入力してください...",
    value=st.session_state["input_text"],
    key="input_text",
    height=150,
)

# マイクボタンを中央寄せ
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    # 録音状態に応じてボタン表示を切り替え
    if st.session_state["is_recording"]:
        # 録音中は赤色のボタン
        st.button(
            "録音を終了",
            key="mic_button_recording",
            type="primary",
            on_click=toggle_recording,
        )
    else:
        # 通常時は青色のボタン
        st.button(
            "音声で入力🎤",
            key="mic_button_idle",
            type="primary",
            on_click=toggle_recording,
        )

# スペースを追加
st.write("")
st.write("")

# 完了ボタンを目立たせる
st.subheader("✅ 入力が完了したら下のボタンをクリック")

# 完了ボタン（大きめに表示）
submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
with submit_col2:
    st.button(
        "📝 タスクを認識する 📝",
        key="submit_button",
        use_container_width=True,
        on_click=submit_task,
    )
