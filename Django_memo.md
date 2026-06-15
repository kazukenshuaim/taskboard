# Djangoファイルのメモ
## Dockerコマンド
```
docker compose up --build
```
`requirements.txt` を変更したあとは必ずこれを実行する
```
docker compose up
```
dbとwebコンテナを起動。
```
docker compose down
```
コンテナを停止する。同じポート`8000`のURL`http://localhost:8000`を別のディレクトリのプロジェクトで使いたいなら、これで停止してから別のプロジェクトのコンテナを起動する。
```
docker ps -a
```
コンテナのステータスを確認。
## ディレクトリ構成
```
C:.
│  .env
│  .env.example
│  .gitignore
│  db.sqlite3
│  Django_memo.md
│  docker-compose.yml
│  Dockerfile
│  manage.py
│  README.md
│  requirements.txt
│  
├─accounts
│  │  admin.py
│  │  apps.py
│  │  forms.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │  
│  ├─migrations
│  │  │  0001_initial.py
│  │  │  __init__.py
│  │  │  
│  │  └─__pycache__
│  │          0001_initial.cpython-312.pyc
│  │          __init__.cpython-312.pyc
│  │          
│  └─__pycache__
│          admin.cpython-312.pyc
│          apps.cpython-312.pyc
│          forms.cpython-312.pyc
│          models.cpython-312.pyc
│          urls.cpython-312.pyc
│          views.cpython-312.pyc
│          __init__.cpython-312.pyc
│          
├─config
│  │  asgi.py
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
│  │  
│  └─__pycache__
│          settings.cpython-312.pyc
│          urls.cpython-312.pyc
│          wsgi.cpython-312.pyc
│          __init__.cpython-312.pyc
│          
├─tasks
│  │  admin.py
│  │  apps.py
│  │  forms.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │  
│  ├─migrations
│  │  │  0001_initial.py
│  │  │  __init__.py
│  │  │  
│  │  └─__pycache__
│  │          0001_initial.cpython-312.pyc
│  │          __init__.cpython-312.pyc
│  │          
│  └─__pycache__
│          admin.cpython-312.pyc
│          apps.cpython-312.pyc
│          forms.cpython-312.pyc
│          models.cpython-312.pyc
│          urls.cpython-312.pyc
│          views.cpython-312.pyc
│          __init__.cpython-312.pyc
│          
└─templates
    │  base.html
    │  
    ├─accounts
    │      login.html
    │      register.html
    │      
    ├─components
    │      _navbar.html
    │      
    └─tasks
            category_confirm_delete.html
            category_form.html
            category_list.html
            task_confirm_delete.html
            task_detail.html
            task_form.html
            task_list.html
```

## 各ファイルの動作

#### day03,day04,day09-config/settings.py
- **役割**: Djangoプロジェクト全体の挙動や外部連携を一括で管理する基本設定ファイル。取扱説明書にあたる。
- **処理**: 環境変数（.env）の読み込み、使用するアプリ（accounts, tasks）やデータベース（PostgreSQL）の指定、ログイン・ログアウト時のリダイレクト先などを定義しています。

#### day03-accounts/models.py
- **役割**: ユーザー情報をデータベースに保存するためのテーブル構造を定義するファイル。
- **処理**: Django標準のユーザー機能をそのまま継承した CustomUser クラスを作成し、将来的なユーザー情報の項目追加（拡張）に備えています。

#### day03-accounts/forms.py
- **役割**: ユーザー登録の入力データを検証・処理するためのフォーム定義。
- **処理**: 新規アカウント登録用に、ユーザー名・メールアドレス・パスワード（確認含む）の入力項目とバリデーション（検証）機能を提供します。
- `fields = ('username', 'email', 'password1', 'password2')`で入力フォームの内容を指定
- `UserCreationForm`を継承しているので、バリデーションなどが標準搭載されている

#### day03-accounts/views.py
- **役割**: ユーザー登録における、画面表示からデータ保存までの裏方のビジネスロジックを担当。
- **処理**: 登録フォームを画面に表示し、ユーザーが正しい情報を入力して送信したら、データベースに保存すると同時にそのまま自動でログイン処理を行います。
- `accounts/register.html`という名前のHTMLテンプレートを呼び出す。
- ユーザー登録成功後、`task_list`ページへジャンプ
- `form_valid(self, form)`は、入力内容にエラーがなかったら実行。

#### day03,day04-accounts/urls.py
accountsアプリ内のURLの道案内を定義。
- **役割**: アカウント管理に関するURL（登録、ログイン、ログアウト。例えば`/accounts/register/`や`/accounts/login/`）と処理（ビュー）を紐付ける。
- **処理**: `/register/`、`/login/`、`/logout/` へのアクセスに対し、それぞれ対応する登録ビューやDjango標準の認証ビューを呼び出します。
- `path('register/', RegisterView.as_view(), name='register'),`: `accounts/register`にアクセスしたとき、`RegisterView.as_view()`（`RegisterView`クラスを関数に変換したもの）を呼び出し、URLに`register`という名前を付ける

#### day03,day04-config/urls.py
プロジェクト全体のURL設定。URLのメインの受付窓口。
- **役割**: WebブラウザからリクエストされたURLを、どのアプリに振り分けるかを決める司令塔。
- **処理**: 管理画面（/admin/）、認証系（/accounts/）、タスク管理系（/tasks/）のURLへのアクセスを、それぞれのアプリのルーティング設定へ中継します。
- `path('accounts/', include('accounts.urls')),`: URLの始まりが`accounts/`だった場合、残りの後半部分のURL判断は`accounts/urls.py`に丸投げする


#### day03,day04,day09-templates/base.html
- **役割**: 全ての画面の土台（骨組み）となる、Webサイト共通のHTMLデザインテンプレート。
- **処理**: Bootstrap（装飾ライブラリ）の読み込み、ナビゲーションバーの表示、エラーや成功を知らせる通知メッセージの表示枠、各画面の中身がはめ込まれる枠（block）を定義しています。
- `{% block content %}{% endblock %}`: 中身をくりぬいた空きスペース。ほかのHTMLファイル内のコードがここに入る。

#### day03-templates/accounts/register.html
- **役割**: 新しくサービスを利用するユーザー向けの「アカウント登録画面」。
- **処理**: base.html をベースにして、ユーザー名やパスワードを入力するフォームを表示し、すでに登録済みの人向けにログイン画面へのリンクを配置します。
- `{{ form.as_p }}`: `accounts/views.py` から渡された入力フォーム（`CustomUserCreationForm`）の項目を、それぞれ <p> タグ（段落）で囲んで自動的に一発で画面に並べる。

#### day04,day06,day07,day08,day09-tasks/views.py
- **役割**: タスク管理のメインロジック（データの取得・フィルタ検索・閲覧制限など）を担当。
- **処理**: ログイン必須の制限をかけつつ、自分が作ったタスクやカテゴリだけを検索・一覧表示・追加・編集・削除できるようにデータベースを操作します
- `class TaskListView(LoginRequiredMixin, ListView)`: `LoginRequiredMixin`を左側に書くことで「ログイン必須」、`ListView`を書くことで「データを並べて一覧表示する機能」を引き継いでいる。

#### day04,day06,day07,day08-tasks/urls.py
- **役割**: tasksアプリ内のURLの道案内。タスクとカテゴリに関する一覧・詳細・作成・変更・削除などのURL一覧を定義。
- **処理**: `<int:pk>`（データのID）などを含んだ様々なURLパターンを、それらを処理する対応したビュークラスへ割り振ります。

#### day04,day06,day07,day08,day09-templates/tasks/task_list.html
- **役割**: 自分が作ったタスクを一覧で確認・検索できる「タスク一覧画面」。
- **処理**: キーワードやステータスでの検索フォーム、タスクを並べた表（ステータスごとに色分けされたバッジ付き）、10件ごとにページを分けるナビゲーションを表示します。

#### day04-templates/accounts/login.html
- **役割**: 登録済みのユーザーがシステムに入るための「ログイン画面」。
- **処理**: base.html の骨組みにログイン用フォームをはめ込み、未登録の人向けにアカウント登録画面への案内リンクを表示します。
- `{{ form.as_p }}`: `accounts/urls.py` で指定した Django標準の`LoginView`が、「ユーザー名（またはメールアドレス）」と「パスワード」の入力欄を、それぞれ <p> タグ（段落）で囲んで自動的に生成。

#### day05-tasks/models.py
- **役割**: データベースの設計図。タスクとカテゴリのデータをデータベースで管理するための構造（テーブル）定義。
- **処理**: カテゴリ（名前など）とタスク（タイトル、説明、進捗、期限など）の項目を定義し、それぞれが「どのユーザーが作ったか」を紐付ける関係性を構築しています。
- `Category`と`Task`のふたつのテーブルが、`User`と紐づく
- カテゴリ、タスクそれぞれ保存するデータベースのテーブルをクラスとして定義。
- `def __str__(self):`: 管理画面でカテゴリの名前そのものを文字として画面表示してというお約束

#### day05-tasks/admin.py
- **役割**: 開発者や管理者がブラウザ上でデータを直接操作できる「管理画面」のカスタマイズ。
- **処理**: 管理画面にタスクとカテゴリを表示し、一覧画面でステータスによる絞り込みやキーワード検索、特定の項目（期限など）の表示をできるようにしています。

#### day06,day07-templates/tasks/task_detail.html
- **役割**: 選んだタスクの詳しい内容を確認し、その場で進捗を変更できる「詳細画面」。
- **処理**: タイトルや期限、説明文を綺麗に並べて表示し、編集・削除ボタンのほか、プルダウンからステータス（未着手など）を直接更新できるフォームを用意しています。

#### day07 tasks/forms.py
- **役割**: タスクを新規作成・編集する際の、入力フォームの仕様を定義。
- **処理**: モデルと連動してタイトルや期限などの入力欄を生成し、期限欄にはブラウザ標準のカレンダー（日付ピッカー）が表示されるよう見た目を調整しています。

#### day07-templates/tasks/task_form.html
- **役割**: タスクを「新規作成」と「内容の編集」で共通して使う「入力画面」。
- **処理**: 新規作成か編集かを自動で判定して見出し（「新規タスク」など）を切り替え、設定された入力欄と保存ボタンを表示します。
- `object`が`True`のとき編集、`False`のとき新規タスク。

#### day07-templates/tasks/task_confirm_delete.html
- **役割**: 誤操作でタスクを消してしまわないように挟む「削除の最終確認画面」。
- **処理**: 「本当に削除してもよいですか？」という警告文と、取り消し不可である旨を赤色ベースのデザインで表示し、最終実行をユーザーに促します。

#### day08-templates/tasks/category_list.html
- **役割**: 作成したタスクの分類に使う、カテゴリの名前一覧を確認する画面。
- **処理**: 登録されているカテゴリをリスト形式で綺麗に一覧表示し、それぞれの横に個別の削除ボタンを配置します。

#### day08-templates/tasks/category_form.html
- **役割**: 新しい分類枠を作成するための「カテゴリ追加画面」。
- **処理**: カテゴリ名を入力するためのシンプルな1項目フォームと、追加を実行・キャンセルするボタンを表示します。

#### day08-templates/tasks/category_confirm_delete.html
- **役割**: カテゴリを消す際に、影響範囲をあらかじめ伝えるための「削除確認画面」。
- **処理**: 削除の最終確認ボタンを設置し、「カテゴリを消しても、その中のタスク自体は消えずに『未設定』になるだけ」という親切な補足説明を表示します。

#### day08-templates/components/_navbar.html
- **役割**:
画面最上部に表示されるヘッダー（メニューバー）であり、主要なページへの移動やログイン状態の切り替えを行うための共通の案内板。

- **処理**:
 状態に応じたメニューの切り替え: {% if user.is_authenticated %} を使い、ログイン中なら「タスク・カテゴリ一覧へのリンク」「ユーザー名」「ログアウトボタン」を表示し、未ログインなら「ログイン」「登録」ボタンを表示します。
 安全なログアウト処理: ログアウトボタンを単なるリンクではなく、不正な操作を防ぐ {% csrf_token %} を含んだPOST送信フォーム（form method="post"）にすることで、セキュリティ安全性を担保したログアウト処理を行います。
 
Djangoは基本的に **「URL（urls.py） ➔ ビュー（views.py） ➔ モデル/フォーム（models.py/forms.py） ➔ テンプレート（html）」** という順番で処理が流れます。この基本を意識すると理解しやすいです。

---

## 各処理の手順

#### ① day03-ユーザー登録とその情報のDB保存
1. `accounts/urls.py` が `/register/` へのアクセスを検知し、`RegisterView` を呼び出す。
2. `RegisterView`（`views.py`）が `CustomUserCreationForm`（`forms.py`）を使って、入力されたユーザー名やパスワードに不備がないか検証する。
3. 問題がなければ `CustomUser` モデル（`models.py`）経由でデータベース（PostgreSQL）に保存され、直後に `login()` 関数で自動ログインしてタスク一覧へリダイレクトする。
```text
[ブラウザ] ----(GET: /accounts/register/)----> [config/urls.py]
                                                      | (accounts/ を検知)
                                                      v
                                               [accounts/urls.py]
                                                      | (register/ を検知)
                                                      v
                                               [RegisterView (views.py)]
                                                      |
                                                      |-- 1. CustomUserCreationForm を準備
                                                      |-- 2. templates/accounts/register.html をレンダリング
                                                      v
[ブラウザ] <---(ユーザー登録画面を表示)--------------------|

ユーザーが情報を入力して「登録」ボタンをクリック（POST送信）

[ブラウザ] ----(POST: /accounts/register/)----> [RegisterView (views.py)]
                                                      |
                                                      |-- 1. CustomUserCreationForm でバリデーション（入力チェック）
                                                      |-- 2. OKなら CustomUser (models.py) へデータを保存 (PostgreSQL)
                                                      |-- 3. login() 関数により自動ログイン処理
                                                      v
[ブラウザ] <---(リダイレクト: /tasks/)---------------------| (success_url へ遷移)
```

#### ② day04-ログイン
1. `accounts/urls.py` が `/login/` へのアクセスを検知し、Django標準の `LoginView` を呼び出す。
2. `LoginView` が `templates/accounts/login.html` を表示し、ユーザーが入力した認証情報を検証する。
3. 認証が成功すると、`config/settings.py` の `LOGIN_REDIRECT_URL` の設定に従って `/tasks/`（タスク一覧）へリダイレクトする。

```
[ブラウザ] ----(GET: /accounts/login/)----> [config/urls.py] ➔ [accounts/urls.py]
                                                    |
                                                    v
                                             [auth_views.LoginView (Django標準)]
                                                    | テンプレート指定: accounts/login.html
                                                    v
[ブラウザ] <---(ログイン画面を表示)---------------------|

ユーザーが「ユーザー名」「パスワード」を入力して「ログイン」をクリック（POST送信）

[ブラウザ] ----(POST: /accounts/login/)----> [auth_views.LoginView (Django標準)]
                                                    |
                                                    |-- 1. 内部で CustomUser (models.py) のデータと照合
                                                    |-- 2. 認証成功後、セッション（ログイン状態）を確立
                                                    |      config/settings.py (LOGIN_REDIRECT_URL)
                                                    v
[ブラウザ] <---(リダイレクト: 指定ページへ)-----------------|
```

#### ③ day04-ログアウト
1. `templates/base.html` のログアウトボタン（POST送信）から `/accounts/logout/` へリクエストが送られる。
2. `accounts/urls.py` がこれを受け取り、Django標準の `LogoutView` を呼び出す。
3. `LogoutView` がセッションを破棄し、`config/settings.py` の `LOGOUT_REDIRECT_URL` の設定に従ってログイン画面へリダイレクトする。
```
[ブラウザ] (ヘッダーのログアウトボタンを押下)
   |
   | (templates/base.html 内のフォームからPOST送信)
   v
[ブラウザ] ----(POST: /accounts/logout/)----> [config/urls.py] ➔ [accounts/urls.py]
                                                     |
                                                     v
                                              [auth_views.LogoutView (Django標準)]
                                                     |
                                                     |-- 1. ユーザーのセッション（ログイン状態）を破棄
                                                     |      config/settings.py (LOGOUT_REDIRECT_URL)
                                                     v
[ブラウザ] <---(リダイレクト: ログイン画面等へ)------------|
```

#### ④ day04-未ログインユーザーの制限（※⑤⑥の前に連動）
1. ログインしていないユーザーが `/tasks/` などに直接アクセスする。
2. 各ビュー（`TaskListView` など）に設定された `LoginRequiredMixin`（`views.py`）が、未ログイン状態であることを検知して処理をブロックする。
3. `config/settings.py` の `LOGIN_URL` の設定に従って、ユーザーを自動的に `/accounts/login/` へ強制リダイレクトする。
```
[ブラウザ] ----(GET: /tasks/)----> [config/urls.py] ➔ [tasks/urls.py]
                                         |
                                         v
                                  [TaskListView (views.py)]
                                         |
                                         |-- 1. 継承している「LoginRequiredMixin」が起動
                                         |-- 2. request.user.is_authenticated をチェック ➔ 「False」
                                         |-- 3. config/settings.py の「LOGIN_URL = '/accounts/login/'」を参照
                                         v
[ブラウザ] <---(302リダイレクト: /accounts/login/?next=/tasks/)---|
```

#### ⑤ day06-タスク一覧表示
1. `tasks/urls.py` が URL（`/tasks/`）を検知し、`TaskListView`（`views.py`）を呼び出す。
2. `TaskListView` の `get_queryset()` メソッドが、`Task` モデル（`models.py`）を使って「現在ログインしているユーザーが作ったタスク（`created_by=self.request.user`）」だけをDBから取得する。
3. 取得したデータが `templates/tasks/task_list.html` に送られ、`{% for task in tasks %}` ループによって表形式で画面に表示される。
```
[ブラウザ] ----(GET: /tasks/)----> [config/urls.py]
                                         | (tasks/ を検知)
                                         v
                                  [tasks/urls.py]
                                         | (末尾空っぽ '' を検知)
                                         v
                                  [TaskListView (views.py)]
                                         |
                                         |-- 1. LoginRequiredMixin によるログインチェック
                                         |-- 2. get_queryset() が起動
                                         |      ➔ Task.objects.filter(created_by=自分) でDBから取得
                                         |      ➔ ordering = ['-created_at'] に基づき最新順にソート
                                         |-- 3. 取得データを変数 'tasks' に格納、テンプレートにわたす
                                         v
                                  [templates/tasks/task_list.html]
                                         |
                                         |-- 1. {% extends 'base.html' %} で共通枠組みと合体
                                         |-- 2. {% for task in tasks %} でタスクの数だけループ
                                         |-- 3. get_status_display でステータスを日本語化
                                         v
[ブラウザ] <---(HTMLの表形式で一覧を表示)----------------|
```

#### ⑥ day06-タスク詳細表示
1. 一覧画面のリンクから `/tasks/1/` のようなID付きのURLが送られ、`tasks/urls.py` が `TaskDetailView`（`views.py`）へ繋ぐ。
2. `TaskDetailView` は他人のタスクを覗き見られないよう、自分のタスクの中から該当するID（`pk`）のデータをDBから1件だけ取得する。
3. 取得した1件のタスクデータが `templates/tasks/task_detail.html` に渡され、タイトルや期限、説明文が詳しく表示される。
```
[ブラウザ] (一覧画面から特定のタスクリンク「例: ID 5番」をクリック)
   |
   v
[ブラウザ] ----(GET: /tasks/5/)----> [config/urls.py] ➔ [tasks/urls.py]
                                            |
                                            | ( <int:pk>/ によって pk=5 を抽出 )
                                            v
                                     [TaskDetailView (views.py)]
                                            |
                                            |-- 1. get_queryset() が起動
                                            |      ➔ 「自分が作ったタスク」の中からIDが「5」のものを検索
                                            |      (※他人のタスクIDだった場合はここで見つからず 404 エラー)
                                            |-- 2. 見つかったデータを変数 'task' に格納
                                            v
                                     [templates/tasks/task_detail.html]
                                            |
                                            |-- 1. {{ task.title }} や説明文を表示
                                            |-- 2. |linebreaks フィルターで改行を反映
                                            |-- 3. |date フィルターで日時を日本向けフォーマットに変換
                                            v
[ブラウザ] <---(カード型の詳細画面を表示)---------------|
```

#### ⑦ day07-タスク作成
1. `/tasks/create/` へのアクセスで `TaskCreateView`（`views.py`）が起動し、`TaskForm`（`forms.py`）を使って入力画面を表示する。
2. ユーザーがフォームを入力して送信すると、`form_valid()` メソッドが動き、データに「作成者＝ログインユーザー（`created_by`）」の情報を裏側で自動追加する。
3. `Task` モデルを通じてDBにデータが新規保存され、一覧画面へ戻る。
```
[ブラウザ] ----(GET: /tasks/create/)----> [config/urls.py] ➔ [tasks/urls.py]
                                                 |
                                                 v
                                          [TaskCreateView (views.py)]
                                                 |
                                                 |-- 1. get_form() が起動
                                                 |      ➔ 選択肢を self.request.user.categories.all() (自分のカテゴリ) に絞り込む
                                                 |-- 2. templates/tasks/task_form.html を指定
                                                 v
[ブラウザ] <---(空の入力フォーム画面を表示)--------------|

ユーザーが内容を入力して「保存」ボタンをクリック（POST送信）

[ブラウザ] ----(POST: /tasks/create/)----> [TaskCreateView (views.py)]
                                                 |
                                                 |-- 1. TaskForm による入力バリデーション
                                                 |-- 2. form_valid() が起動
                                                 |      ➔ form.instance.created_by = self.request.user (作成者を裏で自動セット)
                                                 |-- 3. super().form_valid() にて Task (models.py) へ新規保存
                                                 v
[ブラウザ] <---(リダイレクト: /tasks/)------------------| (success_url へ遷移)
```

#### ⑧ day07-タスク編集
1. `/tasks/1/update/` のようにID付きでアクセスすると、`TaskUpdateView`（`views.py`）が起動する。
2. `TaskForm` にDBから取得した現在のタスク内容があらかじめ書き込まれた状態で、`templates/tasks/task_form.html` に表示される。
3. ユーザーが内容を書き換えて保存すると、`form_valid()` が変更内容を検知し、DBの既存データを更新（SQLのUPDATE）して詳細画面へ戻る。
```
[ブラウザ] ----(GET: /tasks/5/update/)----> [config/urls.py] ➔ [tasks/urls.py] (pk=5)
                                                   |
                                                   v
                                            [TaskUpdateView (views.py)]
                                                   |
                                                   |-- 1. get_queryset() で「自分の5番のタスク」を確保
                                                   |-- 2. get_form() でカテゴリ選択肢を自分用に絞り込む
                                                   |-- 3. templates/tasks/task_form.html を呼び出す
                                                   |      (※ object が存在するため、見出しは自動で「タスクを編集」になる)
                                                   |      (※ 現在の登録データが最初から入力欄に埋め込まれる（tasks/forms.py (TaskForm)）)
                                                   v
[ブラウザ] <---(データが入った状態のフォームを表示)--------|

ユーザーが内容を書き換えて「保存」ボタンをクリック（POST送信）

[ブラウザ] ----(POST: /tasks/5/update/)----> [TaskUpdateView (views.py)]
                                                   |
                                                   |-- 1. バリデーション後、変更内容をDBに上書き保存
                                                   |      (※ Taskモデルの auto_now=True により updated_at が自動更新)
                                                   |-- 2. get_success_url() が起動、form_valid()で変更内容を確定
                                                   v
[ブラウザ] <---(リダイレクト: /tasks/5/)----------------| (編集したタスクの詳細画面へピンポイントで戻る)
```

#### ⑨ day07-タスク削除
1. `/tasks/1/delete/` へアクセスすると、`TaskDeleteView`（`views.py`）が起動し、`templates/tasks/task_confirm_delete.html` を表示する。
2. ユーザーが画面で「削除する」ボタン（POST送信）を押すと、ビューが対象のタスクデータをDBから完全に削除（SQLのDELETE）する。
3. 削除完了後、`success_url` に指定されたタスク一覧画面へリダイレクトする。
```
[ブラウザ] ----(GET: /tasks/5/delete/)----> [config/urls.py] ➔ [tasks/urls.py] (pk=5)
                                                   |
                                                   v
                                            [TaskDeleteView (views.py)]
                                                   |
                                                   |-- 1. get_queryset() で対象タスクを確認
                                                   |-- 2. templates/tasks/task_confirm_delete.html を呼び出す
                                                   v
[ブラウザ] <---(赤い警告付きの削除確認画面を表示)----------|

ユーザーが「削除する」ボタンをクリック（POST送信）

[ブラウザ] ----(POST: /tasks/5/delete/)----> [TaskDeleteView (views.py)]
                                                   |
                                                   |-- 1. 対象のタスクデータをデータベース(DB)から完全に消去
                                                   v
[ブラウザ] <---(リダイレクト: /tasks/)------------------| (success_url に基づき一覧へ戻る)
```

#### ⑩ day07-タスクステータス変更
1. 詳細画面にあるステータス変更用の小さなフォーム（POST送信）から、`/tasks/1/status/` へリクエストが送られる。
2. `tasks/urls.py` が `TaskStatusUpdateView`（`views.py`）を呼び出す。
3. ビュー内の `post()` メソッドが動き、送られてきた新しい進捗（`todo` / `in_progress` / `done`）を直接タスクデータに上書き保存（`task.save()`）し、詳細画面を再読み込みする。
```
[ブラウザ] (詳細画面のプルダウンでステータスを選択し「変更」ボタンをクリック)
   |
   | (templates/tasks/task_detail.html 内の専用フォームからPOST送信)
   v
[ブラウザ] ----(POST: /tasks/5/status/)----> [config/urls.py] ➔ [tasks/urls.py] (pk=5)
                                                    |
                                                    v
                                             [TaskStatusUpdateView (views.py)]
                                                    |
                                                    |-- 1. get_object_or_404() が起動
                                                    |      ➔ 自分が作った5番のタスクが存在するかチェック
                                                    |-- 2. request.POST.get('status') で新しい状態文字列を取得
                                                    |-- 3. STATUS_CHOICES にある安全な文字列かバリデーション
                                                    |-- 4. task.status = new_status ➔ task.save() でDBをスピード更新
                                                    v
[ブラウザ] <---(リダイレクト: /tasks/5/)-----------------| (即座に元の詳細画面へ強制送還)
```

#### ⑪ day08-カテゴリ作成
1. `CategoryCreateView`（`views.py`）が起動し、`templates/tasks/category_form.html` を表示する。
2. 今回は専用のFormクラスを作っていないため、ビュー側で指定された `fields = ['name']` を基に、Djangoが自動でシンプルな入力欄を生成する。
3. 送信されると `form_valid()` が「作成者」を補完し、`Category` モデル（`models.py`）経由でDBに保存、カテゴリ一覧画面へ遷移する。
```
[ブラウザ] ----(GET: /tasks/categories/create/)----> [CategoryCreateView (views.py)]
                                                            |
                                                            |-- 1. fields = ['name'] から自動フォーム生成
                                                            |-- 2. templates/tasks/category_form.html を表示
                                                            v
[ブラウザ] <---(カテゴリ入力画面を表示)---------------------------|

ユーザーがカテゴリ名を入力して「追加」ボタンを押す（POST送信）

[ブラウザ] ----(POST: /tasks/categories/create/)----> [CategoryCreateView (views.py)]
                                                            |
                                                            |-- 1. form_valid(form) が起動
                                                            |-- 2. form.instance.created_by = self.request.user
                                                            |      （誰が作ったカテゴリかを裏で自動セット）
                                                            |-- 3. Category (models.py) を介してDBへ保存
                                                            v
[ブラウザ] <---(リダイレクト: /tasks/categories/)---------------| (success_url へリダイレクト)
```

#### ⑫ day08-カテゴリ削除
1. `CategoryDeleteView`（`views.py`）が起動し、確認画面を表示したのち、ユーザーの同意をもって `Category` モデルから対象データを削除する。
2. **裏側の連動処理**: `tasks/models.py` の `Task` クラス側で `category = models.ForeignKey(..., on_delete=models.SET_NULL)` と設定されている。
3. この `on_delete=models.SET_NULL` の働きにより、カテゴリが消されても紐付いていたタスクは連動削除されず、カテゴリの項目だけが自動的に「未設定（Null）」に書き換わる。
```
[ブラウザ] ----(GET: /tasks/categories/5/delete/)----> [CategoryDeleteView (views.py)]
                                                              |
                                                              |-- 1. get_queryset() で「自分の5番のカテゴリ」を確保
                                                              |-- 2. category_confirm_delete.html を表示
                                                              v
[ブラウザ] <---(「削除してもよいですか？」と画面表示)----------------|

ユーザーが「削除する」ボタンをクリック（POST送信）

[ブラウザ] ----(POST: /tasks/categories/5/delete/)----> [CategoryDeleteView (views.py)]
                                                              |
                                                              |-- 1. Category (models.py) の対象データをDBから削除
                                                              |      ➔ 内部で連動：Task.category の on_delete=models.SET_NULL が発動
                                                              |      ➔ 該当カテゴリに属していたタスクのカテゴリ欄が自動で「空」になる
                                                              v
[ブラウザ] <---(リダイレクト: /tasks/categories/)-----------------| (success_url へリダイレクト)
```

#### ⑬ day08-カテゴリ一覧表示 
```
[ブラウザ] ----(GET: /tasks/categories/)----> [config/urls.py]
                                                    | (先頭の 'tasks/' を検知)
                                                    v
                                             [tasks/urls.py]
                                                    | (後半の 'categories/' を検知)
                                                    v
                                             [CategoryListView (views.py)]
                                                    |
                                                    |-- 1. LoginRequiredMixin が起動（未ログインならログイン画面へ）
                                                    |-- 2. get_queryset() が自動的に起動
                                                    |      ➔ Category.objects.filter(created_by=self.request.user)
                                                    |         により「自分が作ったカテゴリ」だけをDBから選別して取得
                                                    |-- 3. 取得したデータを変数「categories」に格納（context_object_name）
                                                    v
                                             [templates/tasks/category_list.html]
                                                    |
                                                    |-- 1. {% extends 'base.html' %} で共通のヘッダー等と合体
                                                    |-- 2. {% if categories %} でデータが存在するかチェック
                                                    |-- 3. {% for category in categories %} ループが起動
                                                    |      ➔ 各カテゴリ名（{{ category.name }}）を1行ずつリスト形式で描画
                                                    |      ➔ 各行の「削除」ボタンに、そのカテゴリの背番号（category.pk）を
                                                    |         使った削除用リンク（tasks:category_delete）を自動生成
                                                    v
[ブラウザ] <---(自分のカテゴリが並んだ一覧画面を表示)------|
```

#### ⑭ day09-タイトル・説明文のキーワード検索
1. 一覧画面の検索窓（`<input name="q">`）に文字を入力して「検索」を押すと、URLの末尾に `?q=会議` のような形でデータが送られる。
2. `TaskListView`（`views.py`）の `get_queryset()` 内で、`self.request.GET.get('q')` を使ってその文字（`keyword`）を受け取る。
3. `Q(title__icontains=keyword) | Q(description__icontains=keyword)` というDjangoの特殊な命令（Qオブジェクト）を使い、タイトル「または」説明文にその文字が含まれるタスクだけをDBから絞り込んで取得する。
```
[ブラウザ] ----(GET: /tasks/?q=会議)----> [TaskListView (views.py)]
                                               |
                                               |-- 1. get_queryset() が起動
                                               |-- 2. keyword = self.request.GET.get('q', '') ➔ 「会議」を取得
                                               |-- 3. Q(title__icontains=keyword) | Q(description__icontains=keyword)
                                               |      ➔ 「タイトル、または説明文に『会議』を【大文字小文字区別せず含む】」という
                                               |         SQLのWHERE句を組み立てて、Task (models.py) がDBへ条件にあうデータを要求
                                               |-- 4. get_context_data() が起動
                                               |      ➔ context['current_q'] = '会議' をセット（入力文字の維持用）
                                               v
                                        [templates/tasks/task_list.html]
                                               |
                                               |-- 1. 検索窓 <input> の value に {{ current_q }} が埋め込まれ、「会議」が残る
                                               |-- 2. 絞り込まれたタスク一覧をループで描画
                                               v
[ブラウザ] <---(「会議」が含まれるタスク一覧を表示)------|
```

#### ⑮ day09-タスク一覧でのステータス・カテゴリでのフィルタリング
1. 一覧画面のプルダウンで選択を行うと、URLの末尾に `?status=done&category=2` のように条件が乗る。
2. `TaskListView` 内の `get_queryset()` が、送られてきた `status` や `category_id` の値を取り出す。
3. `queryset.filter(status=status)` や `queryset.filter(category_id=category_id)` を順番に実行（条件の重ね掛け）し、一致するタスクだけを厳選してテンプレートに渡す。
```
[ブラウザ] ----(GET: /tasks/?status=in_progress&category=2)----> [TaskListView (views.py)]
                                                                        |
                                                                        |-- 1. get_queryset() が起動、各条件の値を取り出す
                                                                        |-- 2. status = 'in_progress' を取得 ➔ queryset.filter(status='in_progress')
                                                                        |-- 3. category_id = '2' を取得     ➔ queryset.filter(category_id=2)
                                                                        |      （これによりSQL上で AND 条件としてさらに絞り込まれる）
                                                                        |-- 4. get_context_data()
                                                                        |      ➔ 各選択状態を current_status, current_category に格納
                                                                        v
                                                                 [templates/tasks/task_list.html]
                                                                        |
                                                                        |-- 1. 各 <select> タグ内で、送られた値と一致する <option> に
                                                                        |      {% if ... %}selected{% endif %} が働き、選択状態が固定される
                                                                        v
[ブラウザ] <---(「進行中」かつ「カテゴリID:2」のタスク一覧を表示)----------------|
```

#### ⑯ day09-タスクが10件を超えたらページ分割（ページネーション）
1. `TaskListView`（`views.py`）のクラス内に `paginate_by = 10` という設定が記述されている。
2. Djangoがこの数値を読み取り、DBからタスク全件を取ってくるのではなく、自動的に「1〜10件目」のようにデータを切り分けて取得する（SQLのLIMIT/OFFSET処理）。
3. `templates/tasks/task_list.html` 側の `{% if is_paginated %}` 以降のコードが動き、現在のページ番号や「前へ」「次へ」のリンクボタンを自動計算して画面下部に描画する。
```
[ブラウザ] ----(GET: /tasks/?page=2)----> [TaskListView (views.py)]
                                                |
                                                |-- 1. class変数「paginate_by = 10」をDjangoシステムが認知
                                                |-- 2. 絞り込んだ全データから、自動で2ページ目にあたる「11件目〜20件目」をDBから取得
                                                |-- 3. ページ制御用の情報（is_paginated=True や page_obj）を自動でコンテキストに添付
                                                v
                                         [templates/tasks/task_list.html]
                                                |
                                                |-- 1. {% if is_paginated %} が「True」になり、ページ区切りボタンのエリアが出現
                                                |-- 2. aタグの href に、現在の検索条件（qやstatus）を崩さないように
                                                |      href="?...{% if current_q %}q={{ current_q }}&{% endif %}page=3" のようにリンク構築
                                                v
[ブラウザ] <---(11〜20件目のタスクと、ページネーションバーを表示)---|
```

#### ⑰ day09-操作完了後にフラッシュメッセージ表示
1. 各種ビュー（例：`TaskCreateView`）の `form_valid()` などの処理が成功したタイミングで、`messages.success(self.request, 'タスクを作成しました。')` を実行する。
2. Djangoがこのメッセージ内容を「セッション（ブラウザの一時的な記憶）」に一度保存し、リダイレクト先の画面へ引き継ぐ。
3. 移動先の画面の土台である `templates/base.html` の中の `{% for message in messages %}` というパーツが自動的にそのメッセージを検知し、Bootstrapの警告枠（`alert-danger` や `alert-success`）を使って画面上部に1回だけ表示する。
```
[ブラウザ] ----(タスクを新規入力して送信)----> [TaskCreateView (views.py)]
                                                   |
                                                   |-- 1. バリデーションクリア後、form_valid(form) が起動
                                                   |-- 2. messages.success(self.request, 'タスク「〇〇」を作成しました。') が実行される
                                                   |      ➔ Djangoのメッセージストレージ（クッキーやセッション）に一時保存される
                                                   |-- 3. データベースへの保存完了後、一覧（/tasks/）へリダイレクト指示
                                                   v
[ブラウザ] <---(302リダイレクト)-------------------|

自動的に再度、タスク一覧（/tasks/）へアクセス要求

[ブラウザ] ----(GET: /tasks/)----> [TaskListView (views.py)]
                                         |
                                         |-- 1. context_processors.messages（settings.pyで有効化済み）により、
                                         |      一時保存されていたメッセージデータが自動的に引き出され、テンプレートへ渡される
                                         v
                                  [templates/base.html]
                                         |
                                         |-- 1. {% for message in messages %} ループが回る
                                         |-- 2. class="alert alert-{{ message.tags }}" ➔ alert-success（緑色の枠）になる
                                         v
[ブラウザ] <---(上部に緑色の「作成しました」という通知が入った一覧画面を表示)---|
```

#### ⑱ http://localhost:8000 アクセス時のリダイレクト
```
[ブラウザ] ----(GET: http://localhost:8000/ )----> [config/urls.py]
                                                          |
                                                          |-- 1. 最上行の path('', ...) にマッチする
                                                          |-- 2. RedirectView.as_view(url='/tasks/', permanent=False) が起動
                                                          |-- 3. 「 permanent=False 」により、一時的なリダイレクト（ステータスコード 302）を決定
                                                          v
[ブラウザ] <---(302 Redirect: 「/tasks/ へ行き直して！」と指示)---|

ブラウザが自動的に、指示された `/tasks/` へ瞬時に再度アクセス（自動実行）

[ブラウザ] ----(GET: http://localhost:8000/tasks/)----> [config/urls.py]
                                                               | (先頭の 'tasks/' を検知)
                                                               v
                                                        [tasks/urls.py]
                                                               | (末尾空っぽ '' を検知)
                                                               v
                                                        [TaskListView (views.py)]
                                                               |
                                                               |-- ➔ 機能 ⑩ のログインチェックへ合流
                                                               |-- ➔ ログイン済なら機能 ④ のタスク一覧表示へ
                                                               v
[ブラウザ] <---(タスク一覧画面を表示)--------------------------------|
```
