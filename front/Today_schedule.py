import streamlit as st
from datetime import datetime

from Timer import Timer

if "page" not in st.session_state:
    st.session_state.page="Today_schedule"

def Today_schedule():
    # ページ設定
    #st.set_page_config(layout="wide")

    if st.session_state.page=="Today_schedule":
        # --- サンプルタスクの初期化 ---
        if "tasks" not in st.session_state:
            st.session_state.tasks = [ #機能追加予定ポイント：辞書データ又はネストごとデータベースから受け取る
                {"name": "Task1", "start": "00:00", "end": "10:00"},
                {"name": "Task2", "start": "10:05", "end": "11:30"},
                {"name": "Task3", "start": "11:35", "end": "14:00"},
                {"name": "Task4", "start": "14:10", "end": "23:59"},
            ]
            st.session_state.checked = [False] * len(st.session_state.tasks)

        # --- 共通CSS ---
        st.markdown("""
        <style>
        .divider { border-top: 2px solid #777; margin: 0 -16px; }
        .task-label { font-size: 1.5em; font-weight: bold; }
        .task-time  { font-size: 1.5em; }
        div.stButton > button { font-size: 1.5em !important; }
        /* ハイライト用 */
        .highlight {
            background-color: #fff8b3;  /* 薄い黄色 */
            border-left: 5px solid #ffd33d;
            padding-left: 10px;
            border-radius: 4px;
        }
        </style>
        """, unsafe_allow_html=True)

        # --- 現在時刻取得 ---
        now = datetime.now().time()

        # --- タスク一覧描画 ---
        st.markdown('<div style="max-height:300px; overflow-y:auto">', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        for i, task in enumerate(st.session_state.tasks):
            # チェックボックス
            checked = st.checkbox("", value=st.session_state.checked[i], key=f"chk_{i}")
            st.session_state.checked[i] = checked

            # 取り消し線スタイル
            strike = "text-decoration: line-through; color:#888;" if checked else ""

            # 時刻文字列を time オブジェクトに変換
            start_h, start_m = map(int, task["start"].split(":"))
            end_h,   end_m   = map(int, task["end"].split(":"))
            start_time = datetime.strptime(task["start"], "%H:%M").time()
            end_time   = datetime.strptime(task["end"],   "%H:%M").time()

            # 今ならハイライト
            highlight_cls = "highlight" if start_time <= now <= end_time else ""

            # レイアウト：[チェック, 名前, 時刻, メニュー]
            cols = st.columns([0.5, 3, 4, 1, 1]) 
            cols[0].write("")  # チェック位置合わせ

            # タスク名
            cols[1].markdown(
                f"<div class='{highlight_cls}'><span class='task-label' style='{strike}'>{task['name']}</span></div>",
                unsafe_allow_html=True
            )

            # 時刻表示
            time_text = f"{task['start']} → {task['end']}"
            cols[2].markdown(
                f"<div class='{highlight_cls}'><span class='task-time' style='{strike}'>{time_text}</span></div>",
                unsafe_allow_html=True
            )

            # タイマーボタン
            if cols[3].button("⏲", key=f"timer_{i}", help='タイマー画面へ移動'):
                st.session_state.page="Timer"
                st.rerun()
                pass
            
            # メニューボタン
            cols[4].button("…", key=f"menu_{i}", help='タスク編集画面へ移動') #機能追加予定ポイント：タスク編集画面へ移動する機能の追加

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    elif st.session_state.page=="Timer":
        Timer()

    st.markdown('</div>', unsafe_allow_html=True)

    # --- 下部の追加ボタン ---
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.button("＋", key="add_task", help='タスク作成画面へ') #機能追加予定ポイント：タスク作成画面へ移動する機能の追加



#ページ呼び出し
if __name__ == '__main__':
    Today_schedule()