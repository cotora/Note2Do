# Note2Do

## アプリの概要
マルチタスクを行っている方を対象とし，
* 予定管理が難しい
* タスク登録作業が面倒
* タスク登録の時点で，他人が絡むタスクは登録し忘れてしまう
といった悩みを解決する，タスク管理アプリケーション
### アプリの機能
* カレンダー形式で日ごとのタスクを管理できるようにすることで，予定管理の難しさを緩和
* 会話のテキストデータから，AIを用いた登録タスクの提案機能により，登録作業のハードルを低くし，登録し忘れを防ぐ
* タスク毎にタイマー機能を実装し，タスクに取り組んだ時間計測が可能
### 今後の展望
* 音声認識機能の実装により，登録作業のハードルをさらに下げる
* タイマーの計測機能をデータベースに追加する
    * 各タスクにかかった時間の記録をグラフなどを用いてビジュアル化
* 日にち部分にアイコン表示など，カレンダーをパッと見てその日のタスクを簡単に確認できるようにする機能の実装

## 実行方法

### ライブラリのインストール
以下のコマンドを打つと実行に必要なライブラリがインストールされます
```shell
pip install -r requirements.txt
```

### gemini APIキーの設定
取得したAPIキーを`.env`ファイルに以下の形式で設定します
```
GEMINI_API_KEY=<APIキー>
```

### データベースの作成
以下のコマンドを実行するとアプリで利用するデータベースが作成されます
```shell
python backend/create_db.py
```

### アプリのローカル実行
以下のコマンドでアプリをローカルで開くことができます
```shell
streamlit run front/MainMenu.py
```

## 技術スタック
開発で使用した技術スタックは以下のようになっています
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/tech_stach_note2do.png?raw=true)

## デモ画像
タスク一覧
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/01_Home.png?raw=true)
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/10_Today_schedule.png?raw=true)

カレンダー
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/02_Main_Menu.png?raw=true)
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/03_date_changed.png?raw=true)
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/04_date_task.png?raw=true)

タスク作成
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/04_date_task.png?raw=true)
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/05_create_task.png?raw=true)
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/06_task_created.png?raw=true)

文章認識タスク生成機能
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/07_task_detect.png?raw=true)
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/08_task_detected.png?raw=true)
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/09_task_registered.png?raw=true)
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/10_Today_schedule.png?raw=true)

タイマー機能
![技術スタック](https://github.com/cotora/trachjob_team_p/blob/main/public/Captures/11_Timer.png?raw=true)