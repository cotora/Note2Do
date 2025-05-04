import streamlit as st
import datetime
from datetime import date,timedelta
from create_task_ui import create_task_ui
from detect_task_ui import detect_task_ui
from Today_schedule import Today_schedule

# 最初の1回だけ呼び出す
if "page" not in st.session_state:
    st.session_state.page="MainMenu"
    # ページ設定
    st.set_page_config(
        page_title="Team P Application",
        layout="centered"
    )

print(f"{st.session_state.page=}")

# メインメニュー定義
def mainMenu():
    # 定数宣言
    NIL=-1
    MAX_MONTH=12
    DAYS_ON_WEEK=7
    MIN_SELECTED_YEAR=1990
    MAX_SELECTED_YEAR=date.today().year+10

    # 日時設定関連
    ## ユーザーが指定している年，月の設定
    if "selected_year" not in st.session_state:
        st.session_state["selected_year"]=date.today().year
    if "selected_month" not in st.session_state:
        st.session_state["selected_month"]=date.today().month
    ## ユーザーが操作しているページ関連情報
    if "selected_day" not in st.session_state:
        st.session_state["selected_day"]=date.today().day
    if st.session_state.page=="MainMenu":
        ## 年，月，日を選んでもらう
        st.session_state["selected_year"]=st.selectbox(
            "Select the year",
            [i for i in range(MIN_SELECTED_YEAR,MAX_SELECTED_YEAR+1)])

        st.session_state["selected_month"]=st.selectbox(
            "Select the year",
            [i for i in range(1,MAX_MONTH+1)])
        
        st.session_state["selected_day"]=NIL
        # 初期化部分

        ## 選択された月の1日を取得
        first_day=date(st.session_state["selected_year"],st.session_state["selected_month"],1)

        ## 選択されたの1日の曜日を，日曜：0，月曜：1，...として取得
        now_weekday=(first_day.weekday()+1)%DAYS_ON_WEEK

        ## 選択された月の最終日取得
        next_month_first_day=date(
            first_day.year+(1 if first_day.month==MAX_MONTH else 0),
            (first_day.month%MAX_MONTH)+1,
            1
        )
        current_month_last_day=next_month_first_day-timedelta(days=1)

        ## 各日の日付をlistで保持
        month_info=[[NIL for _ in range(DAYS_ON_WEEK)] for _ in range((current_month_last_day.day+now_weekday+DAYS_ON_WEEK-1)//DAYS_ON_WEEK)]

        count=1  #現在の日
        now_row=0 #現在何週目か(0-indexed)

        while count<current_month_last_day.day:
            #現在のマスに日を記録
            month_info[now_row][now_weekday]=count
            #次のマス位置に更新
            now_weekday=(now_weekday+1)%DAYS_ON_WEEK
            if now_weekday==0:
                now_row+=1
            count+=1
        month_info[now_row][now_weekday]=count

        # メイン部分

        ## 月をタイトルとして表示
        st.title(f"{st.session_state["selected_year"]}年 {st.session_state["selected_month"]} 月")

        ## 今日がカレンダーに描画されているか否か
        today_existed=(st.session_state["selected_year"]==date.today().year and st.session_state["selected_month"]==date.today().month)

        # CSS（1回だけ）: ボタンにクラスを追加するための仕込み
        st.markdown("""
        <style>
        div[data-testid="column"] > div:has(button.today-button) > button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: bold;
            border: 2px solid #0f0 !important;
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

        clicked=NIL
        ## カレンダー形式でボタン表示
        for i in range(len(month_info)):
            button_col=st.columns(DAYS_ON_WEEK)
            for j in range(DAYS_ON_WEEK):
                if month_info[i][j]!=NIL:
                    button_id=first_day.year*10000+first_day.month*100+month_info[i][j] #ボタンIDは年月日をそのまま並べたもので
                    if today_existed and month_info[i][j]==date.today().day:
                        html = f"""
                            <script>
                            var btn = window.parent.document.querySelectorAll('button[data-testid="{button_id}"]');
                            if (btn.length > 0) btn[0].classList.add("today-button");
                            </script>
                        """
                        if button_col[j].button(str(month_info[i][j]),key=button_id):
                            clicked=button_id
                        st.markdown(html, unsafe_allow_html=True)
                    else:
                        if button_col[j].button(str(month_info[i][j]),key=button_id):
                            clicked=button_id

        if clicked!=NIL:
            logDebug(str(clicked)) #ユーザー入力記録
            st.session_state.page="Today_schedule"
            st.session_state["selected_day"]=clicked%100
            st.rerun()
    elif st.session_state.page=="Today_schedule" or st.session_state.page=="Timer" or st.session_state.page=="create_task_ui":
        print(f"{st.session_state['selected_year']=}")
        print(f"{st.session_state['selected_month']=}")
        print(f"{st.session_state['selected_day']=}")
        Today_schedule(date(st.session_state["selected_year"],st.session_state["selected_month"],st.session_state["selected_day"]))
        #create_task_ui(datetime.datetime(st.session_state["selected_year"],st.session_state["selected_month"],st.session_state["selected_day"]))
    elif st.session_state.page=="input" or st.session_state.page=="result":
        detect_task_ui()

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
            st.session_state.page="MainMenu"#カレンダー画面の呼び出し
            #st.switch_page("MainMenu.py")
            pass
        if st.button("② 今日のタスク"):
            logDebug("今日のタスクボタン押下")#ユーザー入力記録
            st.session_state.page="Today_schedule"#今日のタスク画面の呼び出し
            today=date.today()
            st.session_state["selected_year"]=today.year
            st.session_state["selected_month"]=today.month
            st.session_state["selected_day"]=today.day
            #st.switch_page("Today_schedule.py")
            pass
        if st.button("③ 音声認識タスク登録"):
            logDebug("音声認識タスク登録")#ユーザー入力記録
            st.session_state.page="input"#音声認識画面の呼び出し
            #st.switch_page("detect_task_ui.py")
            pass

if __name__=="__main__":
    mainMenu()