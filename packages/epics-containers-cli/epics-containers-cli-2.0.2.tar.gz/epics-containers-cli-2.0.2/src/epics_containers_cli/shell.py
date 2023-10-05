"""
functions for executing commands and querying environment in the linux shell
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Tuple, Union

import typer

from .globals import Architecture
from .logging import log

EC_EPICS_DOMAIN = os.environ.get("EC_EPICS_DOMAIN") or os.environ.get("BEAMLINE")
EC_GIT_ORG = os.environ.get("EC_GIT_ORG")
EC_DOMAIN_REPO = os.environ.get("EC_DOMAIN_REPO", f"{EC_GIT_ORG}/{EC_EPICS_DOMAIN}")
EC_REGISTRY_MAPPING = os.environ.get("EC_REGISTRY_MAPPING")
EC_K8S_NAMESPACE = os.environ.get("EC_K8S_NAMESPACE", EC_EPICS_DOMAIN)
EC_LOG_URL = os.environ.get("EC_LOG_URL", None)


def run_command(command: str, interactive=True, error_OK=False) -> Union[str, bool]:
    """
    Run a command and return the output

    if interactive is true then allow stdin and stdout, return the return code,
    otherwise return True for success and False for failure
    """
    log.debug(
        "running command %s (interactive=%s, error_OK=%s)",
        command,
        interactive,
        error_OK,
    )

    result = subprocess.run(command, capture_output=not interactive, shell=True)

    if result.returncode != 0 and not error_OK:
        if interactive:
            raise typer.Exit(1)

    if interactive:
        return result.returncode == 0
    else:
        return result.stdout.decode()


def check_ioc(ioc_name: str, bl: str):
    cmd = f"kubectl get -n {bl} deploy/{ioc_name}"
    if not run_command(cmd, interactive=False, error_OK=True):
        typer.echo(f"ioc {ioc_name} does not exist in domain {bl}")
        raise typer.Exit(1)


def check_domain(domain: str):
    cmd = f"kubectl get namespace {domain} -o name"
    if not run_command(cmd, interactive=False, error_OK=True):
        typer.echo(f"domain {domain} does not exist")
        raise typer.Exit(1)

    log.info("domain = %s", domain)


def get_image_name(
    repo: str, arch: Architecture = Architecture.linux, target: str = "developer"
) -> str:
    registry = repo2registry(repo).lower().removesuffix(".git")

    image = f"{registry}-{arch}-{target}"
    log.info("repo = %s image  = %s", repo, image)
    return image


def get_git_name(folder: Path = Path("."), full: bool = False) -> Tuple[str, Path]:
    """
    work out the git repo name and top level folder for a local clone
    """
    os.chdir(folder)
    path = str(run_command("git rev-parse --show-toplevel", interactive=False))
    git_root = Path(path.strip())

    remotes = str(run_command("git remote -v", interactive=False))
    log.debug(f"remotes = {remotes}")

    if full:
        matches = re.findall(r"(((git@)|(http)).*(?:\.git)?) ", remotes)
    else:
        matches = re.findall(r"\/(.*)(?:\.git)? ", remotes)
    log.debug(f"matches = {matches}")

    if len(matches) > 0:
        repo_name = str(matches[0][0])
    else:
        typer.echo(f"folder {folder.absolute()} cannot get repo name")
        raise typer.Exit(1)

    log.debug(f"repo_name = {repo_name}, git_root = {git_root}")
    return repo_name, git_root


# work out what the registry name is for a given repo remote e.g.
def repo2registry(repo_name: str) -> str:
    """convert a repo name to a registry name"""

    log.debug("extracting fields from repo name %s", repo_name)

    match_git = re.match(r"git@([^:]*):(.*)\/(.*)(?:.git)", repo_name)
    match_http = re.match(r"https:\/\/([^\/]*)\/([^\/]*)\/([^\/]*)", repo_name)
    for match in [match_git, match_http]:
        if match is not None:
            source_reg, org, repo = match.groups()
            break
    else:
        typer.echo(f"repo {repo_name} is not a valid git remote")
        raise typer.Exit(1)

    log.debug("source_reg = %s org = %s repo = %s", source_reg, org, repo)

    if not EC_REGISTRY_MAPPING:
        typer.echo("environment variable IMAGE_REGISTRY_MAPPING not set")
        raise typer.Exit(1)

    for mapping in EC_REGISTRY_MAPPING.split():
        if mapping.split("=")[0] == source_reg:
            registry = mapping.split("=")[1]
            registry = f"{registry}/{org}/{repo}"
            break
    else:
        typer.echo(f"repo {repo_name} does not match any registry mapping")
        typer.echo("please update the environment variable IMAGE_REGISTRY_MAPPING")
        raise typer.Exit(1)

    return registry
