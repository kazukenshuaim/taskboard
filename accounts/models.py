from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass  # 今は何も追加しない。後から拡張できるように継承しておく