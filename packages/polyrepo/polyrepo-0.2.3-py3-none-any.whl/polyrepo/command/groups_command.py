from dataclasses import dataclass
from argparse import ArgumentParser
import os

from polyrepo.command import PolyRepoCommand
from polyrepo.gitlab import GitLab


@dataclass
class GroupsCommand(PolyRepoCommand):
    """"""

    path: str = ''
    traverse: bool = False
    name = 'groups'

    @classmethod
    def add_args(self, parser):
        parser.add_argument('path', nargs='?')

    @PolyRepoCommand.wrap
    def execute(self):
        from pathlib import Path
        host = self.config_get('gitlab-host')
        token = self.config_get('gitlab-token')
        if host and token:
            subgroups = GitLab(host, token).groups(self.path)
            self.status = f"Listed {len(subgroups)} subgroups"
            return "\n".join(subgroups)
        else:
            raise RuntimeError("Missing host or token for GitLab API call")
