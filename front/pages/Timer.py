import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

def Timer():
    #st.set_page_config(page_title="タイマー", layout="wide")
    # ── セッションステートの初期化 ──
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'elapsed' not in st.session_state:
        st.session_state.elapsed = 0
    if 'completed_time' not in st.session_state:
        st.session_state.completed_time = None

    # ── 1秒ごとに自動リフレッシュ ──
    st_autorefresh(interval=1000, limit=None, key="refresh")

    # ── 上段：Task_name と 完了ボタン ──
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        st.write("")  # スペーサー
    with col2:
        st.markdown(
            """
            <div style="
            margin: 60px auto 20px;
            padding: 12px;
            border:1px solid #333;
            width:300px;
            text-align:center;
            font-size:30px;
            ">Task_name</div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        if st.button("完了"):
            h = st.session_state.elapsed // 3600
            m = (st.session_state.elapsed % 3600) // 60
            st.session_state.completed_time = (h, m)
            st.success(f"完了時刻を保存 → {h:02d}:{m:02d}")

    # ── 中段：タイマー表示 ──
    total = st.session_state.elapsed
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    timer_str = f"{h:02d}:{m:02d}:{s:02d}"
    st.markdown(
        f"""
        <div style="
        font-size:120px;
        text-align:center;
        color:#444;
        margin:40px 0 20px;
        ">{timer_str}</div>
        """,
        unsafe_allow_html=True
    )

    # ── 下段：START／STOP ボタン ──
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        st.write("")
    with col2:
        btn_start, btn_stop = st.columns(2)
        with btn_start:
            if st.button("START"):
                st.session_state.running = True
        with btn_stop:
            if st.button("STOP"):
                st.session_state.running = False
    with col3:
        st.write("")

    # ── 経過時間の更新 ──
    if st.session_state.running:
        st.session_state.elapsed += 1


if __name__ == '__main__':
    Timer()