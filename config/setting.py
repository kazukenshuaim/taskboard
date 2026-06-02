
import os
from pathlib import Path
from dotenv import load_dotenv

# 1. パスの設定
# プロジェクトのルートディレクトリ（.env や manage.py がある場所）
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. .env ファイルの読み込み
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 3. セキュリティ設定
# .env から取得し、なければデフォルト値を使用
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-fallback-key-change-this-in-production")

# 重要: 環境変数から文字列として取得し、正しく Boolean（True/False）に変換する
DEBUG = os.environ.get("DEBUG", "False") == "True"

# デバッグが False（本番モード）の時でもエラーにならないようローカルホストを許可
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "web"]


# 4. アプリケーション定義
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 自作のアプリ（例: 'tasks' など）があればここに追加します
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'], # 必要に応じてテンプレートフォルダを指定
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# 5. データベース設定（ご提示いただいた PostgreSQL の設定）
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "taskboard",          # docker-compose の POSTGRES_DB
        "USER": "taskboard_user",     # docker-compose の POSTGRES_USER
        "PASSWORD": "password",       # docker-compose の POSTGRES_PASSWORD
        "HOST": "db",                 # docker-compose のサービス名
        "PORT": "5432",
    }
}


# 6. パスワードバリデーション
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# 7. 国際化（日本向けの設定）
LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# 8. 静的ファイル（CSS/JavaScriptなど）の設定
STATIC_URL = "static/"
STATIC_FILES_DIRS = [BASE_DIR / "static"]

# 9. プライマリキーの自動フィールド定義
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"