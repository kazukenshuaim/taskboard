# TaskBoard

Django + PostgreSQL + Docker で構築したタスク管理アプリです。

## 機能一覧

- ユーザー登録・ログイン・ログアウト
- タスクの作成・編集・削除・ステータス管理
- カテゴリによる分類・フィルタリング
- キーワード検索・ステータス絞り込み
- ページネーション（10件/ページ）
- 操作完了後のフラッシュメッセージ

## 使用技術

| 技術 | バージョン |
|------|-----------|
| Python | 3.12 |
| Django | 5.0.6 |
| PostgreSQL | 16 |
| Docker | - |
| Bootstrap | 5.3 |

## 前提条件

以下がインストール済みであること：
- Docker Desktop

## 起動方法

**1. リポジトリをクローン**

```bash
git clone git@github.com:<username>/taskboard.git
cd taskboard
```

**2. 環境変数ファイルを作成**

```bash
cp .env.example .env
```

**3. コンテナを起動**

```bash
docker compose up --build
```

**4. マイグレーションを実行**

```bash
docker compose exec web python manage.py migrate
```

**5. 管理画面用スーパーユーザーを作成**

```bash
docker compose exec web python manage.py createsuperuser
```

**6. ブラウザで開く**

http://localhost:8000

## テストの実行

```bash
docker compose exec web python manage.py test
```

## 環境変数

`.env.example` を参照してください。

## 開発フロー

GitHub Flow を採用しています。機能ごとに `feature/xxx` ブランチを作成し、PR を経由して main にマージしています。