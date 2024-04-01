from datetime import datetime, timezone

from github import Github, Auth as GithubAuth

from config import Config
from secrets import Secrets
from post import Post


class Repo:
    @staticmethod
    def get_post_file_path(post: Post):
        return f"{Config.REPO_BLOG_POST_PATH}/{post.file_name}"

    @staticmethod
    def generate_default_title_name():
        now = datetime.now(timezone.utc)
        return f"draft-"

    @staticmethod
    def get_commit_message():
        now = datetime.now(timezone.utc)
        return f"Altair-automated-commit-{now:%Y-%m-%dT%H:%M}"

    def __init__(self, config: Config, secrets: Secrets):
        self.config = config
        self._secrets = Secrets

        self._client = None

    @property
    def client(self):
        if not self._client:
            auth = GithubAuth.Token(self._secrets.GITHUB_FINEGRAINED_TOKEN)
            self._client = Github(auth=auth)
        return self._client

    @property
    def repo(self):
        return self.client.get_repo(self.config.GITHUB_REPO)

    @property
    def default_branch(self):
        return self.repo.get_branch(self.repo.default_branch)

    def create_branch(self, branch_name: str):
        self.repo.create_git_ref(
            ref=f"refs/heads/{branch_name}", sha=self.default_branch.commit.sha
        )

    def update_post(self, post: Post):
        post_file_path = self.get_post_file_path(post)
        contents = self.repo.get_contents(post_file_path, ref=post.branch_name)
        self.repo.update_file(
            post_file_path,
            "message",
            post.file_contents(),
            contents.sha,
            branch=post.branch_name,
        )
