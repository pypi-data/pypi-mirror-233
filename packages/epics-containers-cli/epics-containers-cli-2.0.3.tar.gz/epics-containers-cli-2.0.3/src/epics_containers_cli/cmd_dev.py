import os
import re
import sys
from pathlib import Path
from typing import Optional

import typer

from .globals import Architecture, Targets
from .logging import log
from .shell import get_git_name, get_image_name, run_command

dev = typer.Typer()

IMAGE_TAG = "local"
MOUNTED_FILES = ["/.bashrc", "/.inputrc", "/.bash_eternal_history"]


# parameters for container launches
OPTS = "--security-opt=label=type:container_runtime_t --net=host"


def check_docker():
    """
    Decide if we will use docker or podman cli.

    Prefer docker if it is installed, otherwise use podman
    """
    docker = "podman"

    result = run_command("docker --version", interactive=False, error_OK=True)

    version = int(re.match(r"[^\d]*(\d*)", result).group(1))
    log.debug(f"docker version = {version} extracted from  {result}")
    if version >= 20:
        docker = "docker"

    return docker


# the container management CLI to use
DOCKER = check_docker()


def all_params():
    if os.isatty(sys.stdin.fileno()):
        # interactive
        env = "-e DISPLAY -e SHELL -e TERM -it"
    else:
        env = "-e DISPLAY -e SHELL"

    volumes = ""
    for file in MOUNTED_FILES:
        file_path = Path(file)
        if file_path.exists():
            volumes += f" -v {file}:/root/{file_path.name}"

    return f"{env} {volumes} {OPTS}"


@dev.command()
def launch(
    ctx: typer.Context,
    ioc_folder: Path = typer.Argument(
        ...,
        help="local IOC config folder from domain repo",
        dir_okay=True,
        file_okay=False,
    ),
    generic_ioc_local: Path = typer.Argument(
        None, help="folder for generic IOC project", dir_okay=True, file_okay=False
    ),
    execute: Optional[str] = typer.Option(
        None,
        help="command to execute in the container. Defaults to executing the IOC",
    ),
    target: Targets = typer.Option(
        Targets.developer, help="choose runtime or developer target"
    ),
    args: str = typer.Option(
        "", help=f"Additional args for {DOCKER}/docker, 'must be quoted'"
    ),
    debug: bool = typer.Option(False, help="start a remote debug session"),
):
    """
    Launch an IOC instance using configuration from a domain repo.
    Set generic_ioc_local for a locally editable generic IOC or supply a tag
    to choose any version from the registry.
    """
    log.debug(
        f"launch: ioc_folder={ioc_folder} generic_ioc_local={generic_ioc_local}"
        f" execute={execute} target={target} args={args}"
    )

    ioc_folder = ioc_folder.absolute()
    ioc_name = ioc_folder.name
    values = ioc_folder / "values.yaml"
    if not values.exists():
        typer.echo(f"values.yaml not found in {ioc_folder}")
        raise typer.Exit(1)

    values_text = values.read_text()
    matches = re.findall(r"image: (.*):(.*)", values_text)
    if len(matches) == 1:
        image, tag = matches[0]
    else:
        typer.echo(f"image tag definition not found in {values}")
        raise typer.Exit(1)

    if target == Targets.developer:
        image = image.replace(Targets.runtime, Targets.developer)

    # make sure there are not 2 copies running
    run_command(f"{DOCKER} rm -f {ioc_name}", error_OK=True)

    # TODO promote these to globals or similar
    if execute is None:
        start_script = "-c '/epics/ioc/start.sh; bash'"
    else:
        start_script = f"-c '{execute}'"
    config_folder = "/epics/ioc/config"
    config = all_params() + f' -v {ioc_folder / "config"}:{config_folder} ' + args

    if not generic_ioc_local:
        image_name = f"{image}:{tag}"

    run_command(
        f"{DOCKER} run --rm --entrypoint 'bash' --name {ioc_name} {config}"
        f" {image_name} {start_script}",
        interactive=True,
    )


@dev.command()
def debug_last(
    folder: Path = typer.Argument(Path("."), help="Container project folder"),
    mount_repos: bool = typer.Option(
        True, help="Mount generic IOC repo folder into the container"
    ),
):
    """Launches a container with the most recent image build.
    Useful for debugging failed builds"""
    last_image = run_command(
        f"{DOCKER} images | awk '{{print $3}}' | awk 'NR==2'", interactive=False
    )

    params = all_params()
    _, repo_root = get_git_name(folder)

    if mount_repos:
        params += f" -v{repo_root}:/epics/ioc/${repo_root.name} "

    run_command(
        f"{DOCKER} run --entrypoint bash --rm --name debug_build "
        f"{params} {last_image}"
    )


@dev.command()
def build(
    ctx: typer.Context,
    folder: Path = typer.Option(Path("."), help="Container project folder"),
    arch: Architecture = typer.Option(
        Architecture.linux, help="choose target architecture"
    ),
    cache: bool = typer.Option(True, help="use --no-cache to do a clean build"),
):
    """
    Build a generic IOC container locally from a container project.

    Builds both developer and runtime targets.
    """
    repo, _ = get_git_name(folder, full=True)

    for target in Targets:
        image = get_image_name(repo, arch, target)
        image_name = f"{image}:{IMAGE_TAG} " f"{'--no-cache' if not cache else ''}"
        run_command(
            f"{DOCKER} build --target {target} --build-arg TARGET_ARCHITECTURE={arch}"
            f" -t {image_name} {folder}"
        )


@dev.command()
def versions(
    ctx: typer.Context,
    folder: Path = typer.Argument(Path("."), help="Generic IOC project folder"),
    arch: Architecture = typer.Option(
        Architecture.linux, help="choose target architecture"
    ),
    image: str = typer.Option("", help="override container image to use"),
):
    """
    List the available versions of the generic IOC container image in the registry

    You can supply the full registry image name e.g.
        ec dev versions --image ghcr.io/epics-containers/ioc-template-linux-developer

    or the local project folder (defaults to .) e.g.
        ec dev versions ../ioc-template
    """
    if image == "":
        repo, _ = get_git_name(folder, full=True)
        image = image or get_image_name(repo, arch)

    typer.echo(f"looking for versions of image {image}")
    run_command(
        f"{DOCKER} run --rm quay.io/skopeo/stable " f"list-tags docker://{image}"
    )
