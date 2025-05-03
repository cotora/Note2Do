import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date

#ページ設定
st.set_page_config(
    page_title="カレンダー",
    layout="wide"
)

#サイドバーを作成（番号付きの部分）
with st.sidebar:
    st.markdown("### メニュー")
    if st.button("① カレンダー"):
        #カレンダー画面の呼び出し
        pass
    if st.button("② 今日のタスク"):
        #今日のタスク画面の呼び出し
        pass
    if st.button("③ 音声認識タスク登録"):
        #音声認識画面の呼び出し
        pass

#今日の日付を取得
today = date.today()
current_year = today.year
current_month = today.month
current_day = today.day

#メイン部分
st.title(f"{today.month} 月")