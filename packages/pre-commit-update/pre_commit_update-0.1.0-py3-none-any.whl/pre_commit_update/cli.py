import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional

import click
import git
from git.exc import GitCommandError
from pyproject_parser import PyProject
from ruamel.yaml import YAML


def _get_toml_config(defaults: dict) -> Optional[dict]:
    try:
        toml_file: PyProject = PyProject.load(
            os.path.join(os.getcwd(), "pyproject.toml")
        )
        return {**defaults, **toml_file.tool["pre-commit-update"]}
    except (FileNotFoundError, KeyError):
        return None


def _colorize(text: str, color: str) -> str:
    return click.style(str(text), fg=color)


def _read_yaml_file(file_path: str) -> str:
    with open(file_path) as f:
        content: str = f.read()
    return content


def _save_yaml_file(file_path: str, yaml_doc: YAML, data: Any) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        yaml_doc.dump(data, f)


def _get_target_tag(tags: list, all_versions: bool) -> str:
    if all_versions:
        return tags[0]
    for t in tags:
        if not any(v in t for v in ("a", "b", "rc")):
            return t
    return tags[0]


def _parse_tags(repo: dict) -> list:
    url: str = repo["repo"]
    try:
        remote_tags: list = (
            git.cmd.Git().ls_remote("--tags", url, sort="v:refname").split("\n")
        )
        tags: list = []
        for tag in remote_tags:
            parsed_tag: str = re.split(r"\t+", tag)[1]
            if parsed_tag.endswith("^{}"):
                continue
            parsed_tag = parsed_tag.replace("refs/tags/", "")
            tags.append(parsed_tag)
        return tags
    except GitCommandError:
        raise Exception(f"No tags found for repo: {url}")


def run(
    dry_run: bool, all_versions: bool, verbose: bool, exclude: tuple, keep: tuple
) -> None:
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    try:
        yaml: YAML = YAML()
        yaml.indent(sequence=4)
        file_path: str = os.path.join(os.getcwd(), ".pre-commit-config.yaml")
        yaml_str: str = _read_yaml_file(file_path)
        data: Any = yaml.load(yaml_str)
        no_update: list = []
        to_update: list = []
        ignored: list = []
        kept: list = []

        with ThreadPoolExecutor(max_workers=10) as pool:
            tasks: list = []
            for i in range(len(data["repos"])):
                repo: dict = data["repos"][i]
                tasks.append(pool.submit(_parse_tags, repo))

        for i, repository in enumerate(data["repos"]):
            if not repository["repo"].startswith("http"):
                continue
            repo = data["repos"][i]
            repo_name: str = repo["repo"].split("/")[-1]
            tag_versions: list = tasks[i].result()
            tag_versions.reverse()
            target_ver: str = _get_target_tag(tag_versions, all_versions)
            if repo_name in exclude:
                ignored.append(
                    f"{repo_name} - {_colorize(repo['rev'] + ' ★', 'magenta')}"
                )
                continue
            if repo_name in keep:
                if repo["rev"] != target_ver:
                    kept.append(
                        f"{repo_name} - {_colorize(repo['rev'] + ' -> ' + target_ver + ' ◉', 'blue')}"
                    )
                else:
                    kept.append(
                        f"{repo_name} - {_colorize(repo['rev'] + ' ◉', 'blue')}"
                    )
                continue
            if repo["rev"] != target_ver:
                to_update.append(
                    f"{repo_name} - {_colorize(repo['rev'], 'yellow')} -> {_colorize(target_ver + ' ✘', 'red')}"
                )
                data["repos"][i]["rev"] = target_ver
            else:
                no_update.append(
                    f"{repo_name} - {_colorize(repo['rev'] + ' ✔', 'green')}"
                )

        if verbose:
            for output in (ignored, kept, no_update):
                if not output:
                    continue
                click.echo("\n".join(output))

        if to_update:
            click.echo("\n".join(to_update))
            if not dry_run:
                _save_yaml_file(".pre-commit-config.yaml", yaml, data)
                click.echo(_colorize("Changes detected and applied", "green"))
            else:
                raise click.ClickException(_colorize("Changes detected", "red"))
        else:
            click.echo(_colorize("No changes detected", "green"))

    except Exception as ex:
        sys.exit(str(ex))


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    show_default=True,
    default=False,
    help="Dry run only checks for the new versions without updating",
)
@click.option(
    "-a",
    "--all-versions",
    is_flag=True,
    show_default=True,
    default=False,
    help="Include the alpha/beta versions when updating",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Display the complete output",
)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    default=(),
    help="Exclude specific repo(s) by the `repo` url trim",
)
@click.option(
    "-k",
    "--keep",
    multiple=True,
    default=(),
    help="Keep the version of specific repo(s) by the `repo` url trim (still checks for the new versions)",
)
@click.pass_context
def cli(
    ctx: click.Context,
    dry_run: bool,
    all_versions: bool,
    verbose: bool,
    exclude: tuple,
    keep: tuple,
):
    defaults: dict = {p.name: p.default for p in ctx.command.params}
    is_default: bool = defaults == ctx.params

    if not is_default:
        run(dry_run, all_versions, verbose, exclude, keep)
        return

    toml_params: Optional[dict] = _get_toml_config(defaults)
    if toml_params:
        run(**toml_params)
        return

    run(**defaults)


if __name__ == "__main__":
    cli()
