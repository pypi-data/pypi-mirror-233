from __future__ import annotations
import os
from pathlib import Path, PosixPath
import re
from tempfile import mkdtemp, NamedTemporaryFile
from typeguard import typechecked
from typing import List

from .processtools import run

@typechecked
class GitDownloader:
    def __init__(self, commit: str, dry_run: bool):
        self.commit = commit
        self.dry_run = dry_run

    @staticmethod
    def make_for_prev_commit(dry_run: bool) -> GitDownloader:
        commits_behind_master = 1
        if os.environ.get("BUILD_REASON") == "PullRequest":
            commits_behind_master = 0
        stdout = run(
            f"git rev-parse origin/master~{commits_behind_master}", dry_run=dry_run
        ).stdout
        if dry_run:
            prev_commit = "0123456789abcdef0123456789abcdef01234567"
        else:
            prev_commit = stdout.replace("\n", "")
        assert re.match(
            r"^[A-Fa-f0-9]{40}$", prev_commit
        ), f"Value '{prev_commit}' does not match Git commit hash format."
        return GitDownloader(prev_commit, dry_run)

    @staticmethod
    def make_for_diverge_commit(dry_run: bool) -> GitDownloader:
        if dry_run:
            diverge_original_commit = "0123456789abcdef0123456789abcdef01234567"
        else:
            # This is returnning the last commit in the master branch before diverging.
            # input:
            # A -> B -> C -> D -> E    (master)
            #        -> C1 -> D1       (current)
            # output: B
            find_diverge_commit = "\"diverge_head_commit=$(git cherry origin/master | head -n 1 | awk '{print $2}') && git rev-parse $diverge_head_commit^\""
            # throw_on_error = True calls sys.exit(1) if the command fails. We don't want that.
            outcome = run(
                f"bash -c {find_diverge_commit}", throw_on_error=False, dry_run=dry_run
            )
            diverge_original_commit = None
            if outcome.is_successful:
                diverge_original_commit = outcome.stdout.removesuffix("\n")
            else:
                raise Exception(
                    f"Failed to get diverge commit. Error: {outcome.stderr}"
                )
        return GitDownloader(diverge_original_commit, dry_run)

    def get_changelist(self, regex_filter: str = r".*") -> List[str]:
        if self.dry_run:
            return []

        find_changelist = f'"current_commit=$(git rev-parse HEAD) && git diff {self.commit}..$current_commit --name-only"'
        changelist = run(
            f"bash -c {find_changelist}", dry_run=self.dry_run
        ).stdout
        return re.findall(regex_filter, changelist)

    def download_file(
        self,
        orch_repo_root_path: Path,
        file_path: PosixPath,
        output_dir: PosixPath = None,
        throw_on_error: bool = True,
    ) -> PosixPath:
        stdout = run(
            f"git show {self.commit}:{file_path}",
            dry_run=self.dry_run,
            throw_on_error=throw_on_error,
        ).stdout
        # If dry run, return local version of file.
        if self.dry_run:
            with open(orch_repo_root_path.joinpath(file_path), "r") as f:
                stdout = f.read()
        with NamedTemporaryFile(delete=False, dir=output_dir) as tmp:
            tmp.write(stdout.encode())
        return Path(tmp.name)

    # Tested assuming each subdirectory contains either all directories or all
    # files.
    def download_dir(
        self, orch_repo_root_path: Path, dir_path: PosixPath, temp_dir_root: PosixPath = Path("/tmp")
    ) -> PosixPath:
        stdout = run(
            f"git show {self.commit}:{dir_path}", dry_run=self.dry_run
        ).stdout
        temp_dir_path = Path(mkdtemp(dir=temp_dir_root))
        if self.dry_run:
            paths = orch_repo_root_path.joinpath(dir_path).iterdir()
        else:
            paths = (
                dir_path.joinpath(file_path) for file_path in stdout.splitlines()[2:]
            )
        for path in paths:
            if path.suffix != "":
                self.download_file(path, temp_dir_path)
            else:
                self.download_dir(path, temp_dir_path)
        return temp_dir_path


@typechecked
def get_latest_git_commit_ts() -> int:
    stdout = run(
        f"git show -s --format=%ct",
    ).stdout
    return int(stdout)
