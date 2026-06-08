# Djangoファイルのメモ

## ディレクトリ構成
```
C:.
│  .env
│  .env.example
│  .gitignore
│  db.sqlite3
│  docker-compose.yml
│  Dockerfile
│  manage.py
│  README.md
│  requirements.txt
│  
├─accounts
│  │  admin.py
│  │  apps.py
│  │  forms.py    # ユーザー登録の入力フォームを定義
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
│  │  settings.py   # 取扱説明書
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
    └─tasks
            task_confirm_delete.html
            task_detail.html
            task_form.html
            task_list.html
```

## 各ファイルの動作

### day03-settings.py
取扱説明書にあたるもの

### day03-accounts/forms.py
ユーザー登録の入力フォームを定義している。
- `fields = ('username', 'email', 'password1', 'password2')`で入力フォームの内容を指定
- `UserCreationForm`を継承しているので、バリデーションなどが標準搭載されている

### day03-accounts/views.py
ユーザー登録の画面と処理を担当する。クラスベースビュー（CBV）を用いている。
- `accounts/register.html`という名前のHTMLテンプレートを呼び出す。
- ユーザー登録成功後、task_listページへジャンプ
- `form_valid(self, form)`は、入力内容にエラーがなかったら実行。

### day03-accounts/urls.py
accountsアプリ内のURLの道案内を定義。`/accounts/register/`や`/accounts/login/`というURLのとき、どの画面を表示するかをここで紐づける。
- `path('register/', RegisterView.as_view(), name='register'),`：`accounts/register`にアクセスしたとき、`RegisterView.as_view()`（`RegisterView`クラスを関数に変換したもの）を呼び出し、URLに`register`という名前を付ける

### day03-config/urls.py
プロジェクト全体のURL設定。URLのメインの受付窓口。
- `path('accounts/', include('accounts.urls')),`：URLの始まりが`accounts/`だった場合、残りの後半部分のURL判断は`accounts/urls.py`に丸投げする

### day03-templates/base.html
画面の共通デザインの骨組み。画面上部の黒い横長バーの部分。
- `{% block content %}{% endblock %}`：中身をくりぬいた空きスペース。ほかのHTMLファイル内のコードがここに入る。

### day03-templates/accounts/register.html
ユーザー登録画面のデザイン。
- `{{ form.as_p }}`：`accounts/views.py` から渡された入力フォーム（`CustomUserCreationForm`）の項目を、それぞれ <p> タグ（段落）で囲んで自動的に一発で画面に並べる。

### day04~07-tasks/views.py
タスク管理機能の核。CRUD：作成・読取・更新・削除がフルセットでそろっている。
- `class TaskListView(LoginRequiredMixin, ListView)`：`LoginRequiredMixin`を左側に書くことで「ログイン必須」、`ListView`を書くことで「データを並べて一覧表示する機能」を引き継いでいる。

### day04-tasks/urls.py
tasksアプリ内のURLの道案内を定義。

### day04-06-templates/tasks/task_list.html
タスクの一覧画面のデザイン。

### day04-templates/accounts/login.html
ログイン画面のデザイン。
- `{{ form.as_p }}`：`accounts/urls.py` で指定した Django標準の`LoginView`が、「ユーザー名（またはメールアドレス）」と「パスワード」の入力欄を、それぞれ <p> タグ（段落）で囲んで自動的に生成。

### day05-tasks/models.py
データベースの設計図。
- `Category`と`Task`のふたつのテーブルが、`User`と紐づく
- カテゴリ、タスクそれぞれ保存するデータベースのテーブルをクラスとして定義。
- `def __str__(self):`：管理画面でカテゴリの名前そのものを文字として画面表示してというお約束

### day05-tasks/admin.py
管理画面をカスタマイズするためのもの

### day06-templates/tasks/task_detail.html
タスク詳細画面

### day07-templates/tasks/task_form.html
タスクの新規作成と編集に用いる。`object`が`True`のとき編集、`False`のとき新規タスク。

### day07-templates/tasks/task_confirm_delete.html
タスクを削除するときに「本当に消してもいいですか？」とユーザーに最終確認を求める。

### day?? tasks/forms
- 自動生成

### day?? accounts/models
- 自動生成

