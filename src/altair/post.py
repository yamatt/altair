from datetime import datetime, timezone

from slugify import slugify


class Paragraph:
    pass


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

    def __init__(self, title: str):
        self._title: str = title
        self._paragraphs: dict = {}
        self._paragraph_order: list = []

    @property
    def title(self) -> str:
        return self._title

    @property
    def _branch_slug(self) -> str:
        return slugify(self.title)

    @property
    def branch_name(self) -> str:
        return f"blog-post/{self._branch_slug}"

    def add_paragraph(self, paragraph: Paragraph) -> None:

        if paragraph.id not in self._paragraph_order:
            self._paragraph_order.append(paragraph.id)
        self._paragraphs[paragraph.id] = paragraph
            

        self.update()

    def update(self):
        """
        Creates branch and adds paragraphs to it in GitHub
        """
    
    def text(self):
        text: str = ""

        for paragraph_id in self._paragraph_order:
            text+=self._paragraphs[paragraph_id]
            text+="\n\n"

        return text

class Paragraph:
    @classmethod
    def from_update(cls, update):
        return cls(update.message.message_id, update.message.text)

    def __init__(self, id, text):
        self.id = id
        self.text = text