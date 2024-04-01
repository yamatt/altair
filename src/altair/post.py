from datetime import datetime, timezone

from slugify import slugify


class Post:
    @staticmethod
    def generate_default_title_name():
        now = datetime.now(timezone.utc)
        return f"draft-{now:%Y-%m-%dT%H:%M}"

    @classmethod
    def from_telegram(cls, context):
        title = " ".join(context.args)
        return cls.from_new(title)

    @classmethod
    def from_new(cls, title):
        if not title:
            title = cls.generate_default_title_name()
        return cls(title)

    def __init__(self, title):
        self._title = title

    @property
    def title(self) -> str:
        return self._title

    @property
    def _branch_slug(self) -> str:
        return slugify(self.title)

    @property
    def branch_name(self) -> str:
        return f"blog-post/{self._branch_slug}"
