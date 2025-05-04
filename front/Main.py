import streamlit as st

# ページ設定
st.set_page_config(
    page_title="Team P Application",
    layout="centered"
)

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

if "page" not in st.session_state:
    st.session_state.page="MainMenu"

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
            st.session_state.page="MainMenu"#カレンダー画面の呼び出し
            st.switch_page("./pages/MainMenu.py")
            pass
        if st.button("② 今日のタスク"):
            logDebug("今日のタスクボタン押下")#ユーザー入力記録
            st.session_state.page="Today_schedule"#今日のタスク画面の呼び出し
            st.switch_page("./pages/Today_schedule.py")
            pass
        if st.button("③ 音声認識タスク登録"):
            logDebug("音声認識タスク登録")#ユーザー入力記録
            st.session_state.page="input"#音声認識画面の呼び出し
            st.switch_page("./pages/detect_task_ui.py")
            pass

