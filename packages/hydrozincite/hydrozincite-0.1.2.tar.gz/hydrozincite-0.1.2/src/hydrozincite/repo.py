import logging
import re
from pathlib import Path

from git import Repo

from .config.config import conf

bare_path = Path(conf["repositories"])


def get_all_bare(dir_bare):
    b = [x for x in dir_bare.glob("**/*.git") if x.is_dir() and x.suffix == ".git"]
    repositories = [r for r in [repo(bare) for bare in b] if is_name(r)]
    return sorted(
        repositories,
        key=lambda r: f"{r.parent}/{r.name}".lower()
        if r.parent.as_posix() != "."
        else r.name.lower(),
    )


def is_name(repo):
    if repo.name is not None:
        return True
    else:
        logging.warning(
            "%s is not add because hydrozincite.name is not define" % repo.path
        )
        logging.warning(
            """You can set hydrozincite.name with
            « git -C %s config --local hydrozincite.name '<name>' »"""
            % repo.path
        )


class repo:
    def __init__(self, path):
        self.git = Repo(path)
        self.config = self.git.config_writer("repository")
        self.head = self.git.head.ref
        self.hooks = {
            "post-receive": path / "hooks" / "post-receive",
            "post-update": path / "hooks" / "post-update",
        }
        self.path = path
        self.parent = (
            parent
            if (parent := self.path.relative_to(bare_path).parent) != Path(".")
            else Path()
        )
        self.tags = self.git.tags
        self.last_tag = (
            max(self.tags, key=lambda t: t.commit.committed_datetime)
            if self.tags
            else None
        )

    def __str__(self):
        return "repo(%s/%s, %s)" % (self.parent, self.name, self.path)

    def __repr__(self):
        return self.__str__()

    @property
    def readme(self):
        def list_paths(root_tree, path=Path(".")):
            for blob in root_tree.blobs:
                yield path / blob.name
            for tree in root_tree.trees:
                yield from list_paths(tree, path / tree.name)

        commit = self.git.head.commit
        pattern = re.compile(r"^readme\.?[a-zA-Z]*$", flags=re.IGNORECASE)
        for path in list_paths(commit.tree):
            if pattern.match(path.name):
                readme = self.git.git.show("%s:%s" % (commit, path.name))
                break
            else:
                readme = None
        return readme

    @property
    def last_modif(self):
        all_last_datetime = []
        for branche in self.git.branches:
            all_last_datetime.append(branche.commit.committed_datetime)

        last_modif = max(all_last_datetime)
        return last_modif.isoformat()

    @property
    def heads(self):
        heads = []
        for head in self.git.heads:
            if not head == self.git.head.ref:
                heads.append(
                    {
                        "name": head.name,
                        "last_message": head.commit.message,
                        "datetime": head.commit.committed_datetime.isoformat(),
                    }
                )

        heads.sort(key=lambda k: k["name"].lower())

        return heads

    def _get_option(self, option):
        if self.config.has_option("hydrozincite", option):
            value = self.config.get("hydrozincite", option)
        else:
            value = None
        return value

    def _set_option(self, option, value):
        self.config.set("hydrozincite", option, value)

    def _del_option(self, option):
        self.config.remove_option("hydrozincite", option)

    @property
    def name(self):
        return self._get_option("name")

    @name.setter
    def name(self, value):
        self._set_option("name", value)

    @name.deleter
    def name(self):
        self._del_option("name")

    @property
    def description(self):
        return self._get_option("description")

    @description.setter
    def description(self, value):
        self._set_option("description", value)

    @description.deleter
    def description(self):
        self._del_option("description")

    @property
    def url(self):
        return self._get_option("url")

    @url.setter
    def url(self, value):
        self._set_option("url", value)

    @url.deleter
    def url(self):
        self._del_option("url")
