import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date

# 関数定義
def logDebug(msg:str):
    st.session_state.log_count+=1
    st.session_state.debug_message+=f"{st.session_state.log_count}:{msg}\n" #ユーザー入力記録

# 初期化
## ページ設定
st.set_page_config(
    page_title="カレンダー",
    layout="wide"
)

## デバッグ用メッセージ作成
if "debug_message" not in st.session_state:
    st.session_state.debug_message=""
if "log_count" not in st.session_state:
    st.session_state.log_count=0

## サイドバーのどのタブを表示するか
if "side_bar_id" not in st.session_state:
    st.session_state.side_bar_id=1 # 初期はメインメニューで    
    # 0: デバッグログ確認
    # 1: メインメニューサイドバー


## サイドバー関連
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
        st.text_area("Debug Log",st.session_state.debug_message)
    elif st.session_state.side_bar_id==1:
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

# メイン部分

## 今日の日付を取得
today = date.today()
current_year = today.year
current_month = today.month
current_day = today.day

## 月をタイトルとして表示
st.title(f"{today.month} 月")