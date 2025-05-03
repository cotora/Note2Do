root
├front:UI関係のコードを管理
└backend:内部処理のコードを管理

・フレームワーク
streamlitを使う方針

・Gitコマンドメモ
├git clone <url>:リモートリポジトリの内容をローカルにコピー
│
├git add <ファイル名>:ローカルのファイル単位の変更内容を仮で保存
│
├git commit -m "メッセージ"：git addで貯めた変更内容をメッセージ付きで実際に保存
│
├git push origin main:リモートリポジトリの変更内容をローカルに反映
│
└git pull origin main:リモートリポジトリの変更内容をローカルに反映

・PowerShell コマンドメモ
・New-Item -Type File パス名
・Move-Item -Pass 対象ファイルパス -Destination 目的地ファイルパス名

・WSL+GitHub連携
_GHコマンドを見てみる．