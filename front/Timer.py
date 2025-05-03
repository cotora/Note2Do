import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="タイマー", layout="wide")

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



# サイドバー関連
## 関数定義
def logDebug(msg:str):
    st.session_state.log_count+=1
    st.session_state.debug_message+=f"{st.session_state.log_count}:{msg}\n" #ユーザー入力記録

## 初期化
### デバッグ用メッセージ関連変数宣言
if "debug_message" not in st.session_state:
    st.session_state.debug_message=""
if "log_count" not in st.session_state:
    st.session_state.log_count=0

if "side_bar_id" not in st.session_state:
    st.session_state.side_bar_id=1 # サイドバーのどのタブを表示するか_初期はメインメニューで    
    # 0: デバッグログ確認
    # 1: メインメニューサイドバー

## メイン部分
with st.sidebar:
    #サイドバーの表示タブ選択ボタン
    option=st.selectbox(
        "Select the menu in this side bar."
        ,["Main","Debug Log"]
    )
    if option=="Debug Log":
        st.session_state.side_bar_id=0
    elif option=="Main":
        st.session_state.side_bar_id=1

    if st.session_state.side_bar_id==0:#デバッグ用サイドバー表示
        st.markdown("### Debug Log")
        debug_str="" #デバッグ記録出力用文字列
        for id,msg in enumerate(st.session_state.debug_message):
            debug_str+=f"number:{id}:{msg}\n"
        st.text_area("content",st.session_state.debug_message)
    elif st.session_state.side_bar_id==1:#メインサイドバー表示
        st.markdown("### メニュー")
        if st.button("① カレンダー"):
            logDebug("カレンダーボタン押下")#ユーザー入力記録
            #カレンダー画面の呼び出し
            pass
        if st.button("② 今日のタスク"):
            logDebug("今日のタスクボタン押下")#ユーザー入力記録
            #今日のタスク画面の呼び出し
            pass
        if st.button("③ 音声認識タスク登録"):
            logDebug("音声認識タスク登録")#ユーザー入力記録
            #音声認識画面の呼び出し
            pass