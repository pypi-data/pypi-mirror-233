import json
import logging
import shlex
import subprocess
import sys
import time
from typeguard import typechecked
from typing import Dict, List, Union


@typechecked
def fatal_error(msg: str):
    logging.error(msg)
    sys.stderr.write("{0}\n".format(msg))
    sys.stderr.flush()
    sys.exit(-1)


@typechecked
def log_cmd(cmd, dry_run: bool = False, duration: float = None, timeout: float = None):
    pref = "Executing command"
    if dry_run:
        pref = "Dry run command"
    elif duration is not None:
        pref = "Completed in {0:.3f}s".format(duration)
    elif timeout is not None:
        pref = "Timeout out after {0}s".format(timeout)
    logging.info("===> {0}: {1}".format(pref, cmd))


@typechecked
class CommandOutcome:
    def __init__(
        self, stdout: str, stderr: str, exit_code: int, timed_out: bool, dry_run: bool
    ):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code
        self.timed_out = timed_out
        self.dry_run = dry_run
        self._json_result = None

    @staticmethod
    def new(dry_run: bool):
        return CommandOutcome("", "", 0, False, dry_run)

    @property
    def json_result(self) -> Union[Dict, List]:
        if self.dry_run:
            return {}
        else:
            return json.loads(self.stdout)

    @property
    def is_successful(self) -> bool:
        return self.exit_code == 0 and not self.timed_out

    def log_stdout_stderr(self):
        log_func = (
            lambda s: logging.warning(s)
            if (self.exit_code != 0 or self.timed_out)
            else logging.info(s)
        )
        if self.stdout.strip(" \t\n\r") != "":
            for line in self.stdout.splitlines():
                log_func("STDOUT: {0}".format(line))
        if self.stderr.strip(" \t\n\r") != "":
            for line in self.stderr.splitlines():
                log_func("STDERR: {0}".format(line))
        log_func("EXIT CODE: {0}".format(self.exit_code))


@typechecked
def run(
    cmd: str,
    timeout_sec: int = None,
    throw_on_error: bool = True,
    retries: int = 1,
    dry_run: bool = False,
) -> CommandOutcome:
    cmd = shlex.split(cmd)
    log_cmd(cmd, dry_run=dry_run)
    if dry_run:
        return CommandOutcome.new(dry_run)
    start_time = time.time()
    attempt_num = 0
    while attempt_num <= retries:
        if attempt_num > 0:
            retry_delay = 2**attempt_num  # Minimum delay = 1 second.
            logging.warning(
                f"Attempt {attempt_num}: Command {'timed out' if outcome.timed_out else f'failed with exit code {outcome.exit_code}'}. Retrying in {retry_delay}s ..."
            )
            time.sleep(retry_delay)

        outcome = CommandOutcome.new(dry_run)
        attempt_start_time = time.time()
        p = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        try:
            stdout, stderr = p.communicate(timeout=timeout_sec)
            outcome.exit_code = p.returncode
            outcome.stdout = stdout.decode("utf-8")
            outcome.stderr = stderr.decode("utf-8")
        except subprocess.TimeoutExpired:
            p.terminate()
            outcome.stderr += "\nERROR: TIMEOUT"
            outcome.timed_out = True
        log_cmd(cmd, dry_run=dry_run, duration=time.time() - attempt_start_time)
        outcome.log_stdout_stderr()

        attempt_num += 1
        if outcome.is_successful:
            break
    log_cmd(cmd, dry_run=dry_run, duration=time.time() - start_time)
    if not outcome.is_successful:
        logging.warning(
            f"Final attempt {attempt_num}: Command {'timed out' if outcome.timed_out else f'failed with exit code {outcome.exit_code}'}."
        )
        if throw_on_error:
            if outcome.exit_code != 0:
                err_msg = f"Unexpected exit code {outcome.exit_code} from child process: {cmd}"
            if outcome.timed_out:
                err_msg = f"Child process timed out after {timeout_sec} seconds: {cmd}"
            fatal_error(err_msg)
    return outcome
