# Djangoファイルのメモ

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

#### ① ユーザー登録とその情報のDB保存
1. `accounts/urls.py` が `/register/` へのアクセスを検知し、`RegisterView` を呼び出す。
2. `RegisterView`（`views.py`）が `CustomUserCreationForm`（`forms.py`）を使って、入力されたユーザー名やパスワードに不備がないか検証する。
3. 問題がなければ `CustomUser` モデル（`models.py`）経由でデータベース（PostgreSQL）に保存され、直後に `login()` 関数で自動ログインしてタスク一覧へリダイレクトする。
```
[ブラウザ] ➔ (URL: /register/) ➔ [accounts/urls.py]
                                       ↓
[accounts/views.py (RegisterView)] 📜画面表示
                                       ↓ (フォーム送信)
[accounts/forms.py (CustomUserCreationForm)] ✔データ検証
                                       ↓
[accounts/models.py (CustomUser)] 💾DB保存 (PostgreSQL)
                                       ↓
[タスク一覧へ自動リダイレクト] ➔ (④の処理へ)
```

#### ② ログイン
1. `accounts/urls.py` が `/login/` へのアクセスを検知し、Django標準の `LoginView` を呼び出す。
2. `LoginView` が `templates/accounts/login.html` を表示し、ユーザーが入力した認証情報を検証する。
3. 認証が成功すると、`config/settings.py` の `LOGIN_REDIRECT_URL` の設定に従って `/tasks/`（タスク一覧）へリダイレクトする。
```
[ブラウザ] ➔ (URL: /login/) ➔ [accounts/urls.py]
                                     ↓
[Django標準: LoginView] ➔ 🎨[templates/accounts/login.html] 📜画面表示
                                     ↓ (ユーザー認証成功)
[config/settings.py (LOGIN_REDIRECT_URL)] ⚙転送先確認 (/tasks/)
                                     ↓
[タスク一覧へリダイレクト] ➔ (④の処理へ)
```

#### ③ ログアウト
1. `templates/base.html` のログアウトボタン（POST送信）から `/accounts/logout/` へリクエストが送られる。
2. `accounts/urls.py` がこれを受け取り、Django標準の `LogoutView` を呼び出す。
3. `LogoutView` がセッションを破棄し、`config/settings.py` の `LOGOUT_REDIRECT_URL` の設定に従ってログイン画面へリダイレクトする。
```
[ブラウザ (ログアウトボタン)] ➔ (POST送信) ➔ [accounts/urls.py]
                                                    ↓
[Django標準: LogoutView] 🔐セッション破棄
                                                    ↓
[config/settings.py (LOGOUT_REDIRECT_URL)] ⚙転送先確認 (/accounts/login/)
                                                    ↓
[ログイン画面へリダイレクト] ➔ (②の処理へ)
```

#### ⑥ 未ログインユーザーの制限（※④⑤の前に連動）
1. ログインしていないユーザーが `/tasks/` などに直接アクセスする。
2. 各ビュー（`TaskListView` など）に設定された `LoginRequiredMixin`（`views.py`）が、未ログイン状態であることを検知して処理をブロックする。
3. `config/settings.py` の `LOGIN_URL` の設定に従って、ユーザーを自動的に `/accounts/login/` へ強制リダイレクトする。
```
[ブラウザ (未ログイン)] ➔ (直接アクセス: /tasks/) ➔ [tasks/urls.py]
                                                            ↓
[tasks/views.py (TaskListView 等)] 🛑 [LoginRequiredMixin] が未ログインを検知
                                                            ↓
[config/settings.py (LOGIN_URL)] ⚙転送先確認 (/accounts/login/)
                                                            ↓
[ログイン画面へ強制リダイレクト] ➔ (②の処理へ)
```

#### ④ タスク一覧表示
1. `tasks/urls.py` が URL（`/tasks/`）を検知し、`TaskListView`（`views.py`）を呼び出す。
2. `TaskListView` の `get_queryset()` メソッドが、`Task` モデル（`models.py`）を使って「現在ログインしているユーザーが作ったタスク（`created_by=self.request.user`）」だけをDBから取得する。
3. 取得したデータが `templates/tasks/task_list.html` に送られ、`{% for task in tasks %}` ループによって表形式で画面に表示される。
```
[ブラウザ] ➔ (URL: /tasks/) ➔ [tasks/urls.py]
                                     ↓
[tasks/views.py (TaskListView)] 🧠 get_queryset(): 「自分のタスク」を要求
                                     ↓
[tasks/models.py (Task)] 💾 DBからログインユーザーのタスク一覧を取得
                                     ↓
[tasks/views.py (TaskListView)] 📦 データをテンプレートへ渡す
                                     ↓
🎨[templates/tasks/task_list.html] 📋 {% for task in tasks %} で表を組み立てて描画
```

#### ⑤ タスク詳細表示
1. 一覧画面のリンクから `/tasks/1/` のようなID付きのURLが送られ、`tasks/urls.py` が `TaskDetailView`（`views.py`）へ繋ぐ。
2. `TaskDetailView` は他人のタスクを覗き見られないよう、自分のタスクの中から該当するID（`pk`）のデータをDBから1件だけ取得する。
3. 取得した1件のタスクデータが `templates/tasks/task_detail.html` に渡され、タイトルや期限、説明文が詳しく表示される。
```
[ブラウザ] ➔ (URL: /tasks/1/) ➔ [tasks/urls.py]
                                      ↓
[tasks/views.py (TaskDetailView)] 🧠 get_queryset(): 「自分のID:1のタスク」を要求
                                      ↓
[tasks/models.py (Task)] 💾 DBから該当タスクを1件取得
                                      ↓
🎨[templates/tasks/task_detail.html] 📜 タスクの詳細情報を画面に描画
```

#### ⑦ タスク作成
1. `/tasks/create/` へのアクセスで `TaskCreateView`（`views.py`）が起動し、`TaskForm`（`forms.py`）を使って入力画面を表示する。
2. ユーザーがフォームを入力して送信すると、`form_valid()` メソッドが動き、データに「作成者＝ログインユーザー（`created_by`）」の情報を裏側で自動追加する。
3. `Task` モデルを通じてDBにデータが新規保存され、一覧画面へ戻る。
```
[ブラウザ] ➔ (URL: /tasks/create/) ➔ [tasks/urls.py]
                                            ↓
[tasks/views.py (TaskCreateView)] ➔ [tasks/forms.py (TaskForm)] 📜カレンダー付きフォーム生成
                                            ↓
🎨[templates/tasks/task_form.html] ✍ユーザー入力・送信
                                            ↓
[tasks/views.py (TaskCreateView)] 🧠 form_valid(): 「作成者＝自分」を裏でセット
                                            ↓
[tasks/models.py (Task)] 💾 DBへ新規保存
                                            ↓
[タスク一覧へリダイレクト] ➔ (④の処理へ)
```

#### ⑧ タスク編集
1. `/tasks/1/update/` のようにID付きでアクセスすると、`TaskUpdateView`（`views.py`）が起動する。
2. `TaskForm` にDBから取得した現在のタスク内容があらかじめ書き込まれた状態で、`templates/tasks/task_form.html` に表示される。
3. ユーザーが内容を書き換えて保存すると、`form_valid()` が変更内容を検知し、DBの既存データを更新（SQLのUPDATE）して詳細画面へ戻る。
```
[ブラウザ] ➔ (URL: /tasks/1/update/) ➔ [tasks/urls.py]
                                             ↓
[tasks/views.py (TaskUpdateView)] 💾 DBから現在のデータを取得
                                             ↓
[tasks/forms.py (TaskForm)] ✍現在のデータをフォームに初期値として注入
                                             ↓
🎨[templates/tasks/task_form.html] 📜画面表示 ➔ ユーザー修正・送信
                                             ↓
[tasks/views.py (TaskUpdateView)] 🧠 form_valid(): 変更内容を確定
                                             ↓
[tasks/models.py (Task)] 💾 DBの既存データを更新 (UPDATE)
                                             ↓
[タスク詳細画面へリダイレクト] ➔ (⑤の処理へ)
```

#### ⑨ タスク削除
1. `/tasks/1/delete/` へアクセスすると、`TaskDeleteView`（`views.py`）が起動し、`templates/tasks/task_confirm_delete.html` を表示する。
2. ユーザーが画面で「削除する」ボタン（POST送信）を押すと、ビューが対象のタスクデータをDBから完全に削除（SQLのDELETE）する。
3. 削除完了後、`success_url` に指定されたタスク一覧画面へリダイレクトする。
```
[ブラウザ] ➔ (URL: /tasks/1/delete/) ➔ [tasks/urls.py]
                                             ↓
[tasks/views.py (TaskDeleteView)] ➔ 🎨[templates/tasks/task_confirm_delete.html] ⚠️確認画面
                                             ↓ (「削除する」を送信)
[tasks/views.py (TaskDeleteView)] 🧠 削除処理を実行
                                             ↓
[tasks/models.py (Task)] 🗑️ DBからデータを完全に消去 (DELETE)
                                             ↓
[タスク一覧へリダイレクト] ➔ (④の処理へ)
```

#### ⑩ タスクステータス変更
1. 詳細画面にあるステータス変更用の小さなフォーム（POST送信）から、`/tasks/1/status/` へリクエストが送られる。
2. `tasks/urls.py` が `TaskStatusUpdateView`（`views.py`）を呼び出す。
3. ビュー内の `post()` メソッドが動き、送られてきた新しい進捗（`todo` / `in_progress` / `done`）を直接タスクデータに上書き保存（`task.save()`）し、詳細画面を再読み込みする。
```
🎨[templates/tasks/task_detail.html] 🔄 プルダウン変更・送信 ➔ (URL: /tasks/1/status/)
                                                                      ↓
                                                             [tasks/urls.py]
                                                                      ↓
[tasks/views.py (TaskStatusUpdateView)] 🧠 post(): 送られたステータス（例:done）を取得
                                             ↓
[tasks/models.py (Task)] 💾 task.save(): 進捗項目だけをピンポイントで上書き保存
                                             ↓
[タスク詳細画面へリダイレクト] ➔ (⑤の処理へ)
```

#### ⑪ カテゴリ作成
1. `CategoryCreateView`（`views.py`）が起動し、`templates/tasks/category_form.html` を表示する。
2. 今回は専用のFormクラスを作っていないため、ビュー側で指定された `fields = ['name']` を基に、Djangoが自動でシンプルな入力欄を生成する。
3. 送信されると `form_valid()` が「作成者」を補完し、`Category` モデル（`models.py`）経由でDBに保存、カテゴリ一覧画面へ遷移する。
```
[ブラウザ] ➔ (URL: /tasks/categories/create/) ➔ [tasks/urls.py]
                                                       ↓
[tasks/views.py (CategoryCreateView)] ⚙ fields=['name'] から簡易フォームを自動生成
                                                       ↓
🎨[templates/tasks/category_form.html] ✍入力・送信
                                                       ↓
[tasks/views.py (CategoryCreateView)] 🧠 form_valid(): 「作成者＝自分」を裏でセット
                                                       ↓
[tasks/models.py (Category)] 💾 DBへ新規カテゴリを保存
                                                       ↓
[カテゴリ一覧へリダイレクト] ➔ (⑫の確認元へ)
```

#### ⑫ カテゴリ削除
1. `CategoryDeleteView`（`views.py`）が起動し、確認画面を表示したのち、ユーザーの同意をもって `Category` モデルから対象データを削除する。
2. **裏側の連動処理**: `tasks/models.py` の `Task` クラス側で `category = models.ForeignKey(..., on_delete=models.SET_NULL)` と設定されている。
3. この `on_delete=models.SET_NULL` の働きにより、カテゴリが消されても紐付いていたタスクは連動削除されず、カテゴリの項目だけが自動的に「未設定（Null）」に書き換わる。
```
[ブラウザ] ➔ (URL: /tasks/categories/1/delete/) ➔ [tasks/urls.py]
                                                         ↓
[tasks/views.py (CategoryDeleteView)] ➔ 🎨[templates/tasks/category_confirm_delete.html] 📋注意書き表示
                                                         ↓ (「削除する」を送信)
[tasks/models.py (Category)] 🗑️ DBから指定カテゴリを削除
       ⚡ (連動処理)
[tasks/models.py (Task)] ⚙ ForeignKeyの `on_delete=models.SET_NULL` が発動！
                         🔗 消えたカテゴリ紐づいていたタスクを自動で「未設定(Null)」に更新
```

#### ⑬ タイトル・説明文のキーワード検索
1. 一覧画面の検索窓（`<input name="q">`）に文字を入力して「検索」を押すと、URLの末尾に `?q=会議` のような形でデータが送られる。
2. `TaskListView`（`views.py`）の `get_queryset()` 内で、`self.request.GET.get('q')` を使ってその文字（`keyword`）を受け取る。
3. `Q(title__icontains=keyword) | Q(description__icontains=keyword)` というDjangoの特殊な命令（Qオブジェクト）を使い、タイトル「または」説明文にその文字が含まれるタスクだけをDBから絞り込んで取得する。
```
🎨[templates/tasks/task_list.html] ✍検索窓に「会議」と入力して送信 (?q=会議)
                                           ↓
[tasks/views.py (TaskListView)] 🧠 get_queryset(): self.request.GET.get('q') で「会議」をキャッチ
                                           ↓
[Django内包: Qオブジェクト] 🔀 「タイトルに会議を含む」 OR 「説明文に会議を含む」 の条件を作成
                                           ↓
[tasks/models.py (Task)] 💾 DBへ条件に合うタスクだけを要求
                                           ↓
[tasks/views.py (TaskListView)] 📦 ヒットしたタスクだけを載せて一覧画面を再描画
```

#### ⑭ タスク一覧でのステータス・カテゴリでの絞り込み
1. 一覧画面のプルダウンで選択を行うと、URLの末尾に `?status=done&category=2` のように条件が乗る。
2. `TaskListView` 内の `get_queryset()` が、送られてきた `status` や `category_id` の値を取り出す。
3. `queryset.filter(status=status)` や `queryset.filter(category_id=category_id)` を順番に実行（条件の重ね掛け）し、一致するタスクだけを厳選してテンプレートに渡す。
```
🎨[templates/tasks/task_list.html] 🎛️ プルダウン選択（例: ステータス=完了, カテゴリ=仕事）➔ 送信
                                           ↓ (?status=done&category=2)
[tasks/views.py (TaskListView)] 🧠 get_queryset(): 各条件の値を取り出す
                                           ↓
[Django ORM (フィルターの重ね掛け)] ⚙ .filter(status='done').filter(category_id=2) を実行
                                           ↓
[tasks/models.py (Task)] 💾 2つの条件が両方とも一致するタスクだけをDBから厳選取得
                                           ↓
[tasks/views.py (TaskListView)] 📦 絞り込まれた結果を載せて一覧画面を再描画
```

#### ⑮ タスクが10件を超えたらページ分割（ページネーション）
1. `TaskListView`（`views.py`）のクラス内に `paginate_by = 10` という設定が記述されている。
2. Djangoがこの数値を読み取り、DBからタスク全件を取ってくるのではなく、自動的に「1〜10件目」のようにデータを切り分けて取得する（SQLのLIMIT/OFFSET処理）。
3. `templates/tasks/task_list.html` 側の `{% if is_paginated %}` 以降のコードが動き、現在のページ番号や「前へ」「次へ」のリンクボタンを自動計算して画面下部に描画する。
```
[tasks/views.py (TaskListView)] ⚙ `paginate_by = 10` の設定を読み込む
                                     ↓
[tasks/models.py (Task)] 💾 DBへ「全件」ではなく「指定ページの10件だけ」を要求 (LIMIT/OFFSET)
                                     ↓
[tasks/views.py (TaskListView)] 📦 10件のデータ ＋ ページ情報（前後ページの有無など）をテンプレートに送る
                                     ↓
🎨[templates/tasks/task_list.html] 📋 `{% if is_paginated %}` が反応、下部に「前へ」「次へ」ボタンを描画
```

#### ⑯ 操作完了後にフラッシュメッセージ表示
1. 各種ビュー（例：`TaskCreateView`）の `form_valid()` などの処理が成功したタイミングで、`messages.success(self.request, 'タスクを作成しました。')` を実行する。
2. Djangoがこのメッセージ内容を「セッション（ブラウザの一時的な記憶）」に一度保存し、リダイレクト先の画面へ引き継ぐ。
3. 移動先の画面の土台である `templates/base.html` の中の `{% for message in messages %}` というパーツが自動的にそのメッセージを検知し、Bootstrapの警告枠（`alert-danger` や `alert-success`）を使って画面上部に1回だけ表示する。
```
[各追加/編集/削除ビュー] 🧠 処理成功時に `messages.success(request, '〜しました')` を呼び出す
                                     ↓
[Djangoメッセージフレームワーク] 🔐 内容をブラウザの「セッション（一時記憶）」にパッと保存
                                     ↓ (自動リダイレクト移動)
🎨[templates/base.html] ➔ 📥 `{% for message in messages %}` がセッション内のメッセージを自動検知
                                     ↓
[ブラウザ画面最上部] 🟢 Bootstrapの綺麗な緑枠（alert-success）の中にメッセージを1回だけ表示
```