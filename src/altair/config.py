import os


class Config:
    TELEGRAM_WEBHOOK_URL: str = os.environ.get("TELEGRAM_WEBHOOK_URL")
    APPROVED_USER: str = os.environ.get("APPROVED_USER", str(444943133))
    GITHUB_REPO: str = os.environ.get("GITHUB_REPO")
    GITHUB_DEFAULT_BRANCH: str = "main"
    REPO_BLOG_POST_PATH: str = "content/blog"
