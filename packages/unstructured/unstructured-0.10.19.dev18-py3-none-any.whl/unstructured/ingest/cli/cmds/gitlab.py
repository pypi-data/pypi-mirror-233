import logging
import typing as t
from dataclasses import dataclass

import click

from unstructured.ingest.cli.cmds.utils import Group, conform_click_options
from unstructured.ingest.cli.common import (
    log_options,
)
from unstructured.ingest.cli.interfaces import (
    CliMixin,
    CliPartitionConfig,
    CliReadConfig,
)
from unstructured.ingest.interfaces import BaseConfig
from unstructured.ingest.logger import ingest_log_streaming_init, logger
from unstructured.ingest.runner import gitlab as gitlab_fn


@dataclass
class GitlabCliConfig(BaseConfig, CliMixin):
    url: str
    git_access_token: t.Optional[str] = None
    git_branch: t.Optional[str] = None
    git_file_glob: t.Optional[str] = None

    @staticmethod
    def add_cli_options(cmd: click.Command) -> None:
        options = [
            click.Option(
                ["--url"],
                required=True,
                type=str,
                help="URL to GitHub repository, e.g. "
                '"https://github.com/Unstructured-IO/unstructured", or '
                'a repository owner/name pair, e.g. "Unstructured-IO/unstructured"',
            ),
            click.Option(
                ["--git-access-token"],
                default=None,
                help="A GitHub or GitLab access token, "
                "see https://docs.github.com/en/authentication or "
                "https://docs.gitlab.com/ee/api/rest/index.html#personalprojectgroup-access-tokens",
            ),
            click.Option(
                ["--git-branch"],
                default=None,
                type=str,
                help="The branch for which to fetch files from. If not given,"
                " the default repository branch is used.",
            ),
            click.Option(
                ["--git-file-glob"],
                default=None,
                type=str,
                help="A comma-separated list of file globs to limit which types of "
                "files are accepted, e.g. '*.html,*.txt'",
            ),
        ]
        cmd.params.extend(options)


@click.group(name="gitlab", invoke_without_command=True, cls=Group)
@click.pass_context
def gitlab_source(ctx: click.Context, **options):
    if ctx.invoked_subcommand:
        return

    conform_click_options(options)
    verbose = options.get("verbose", False)
    ingest_log_streaming_init(logging.DEBUG if verbose else logging.INFO)
    log_options(options, verbose=verbose)
    try:
        # run_init_checks(**options)
        read_config = CliReadConfig.from_dict(options)
        partition_config = CliPartitionConfig.from_dict(options)
        # Run for schema validation
        GitlabCliConfig.from_dict(options)
        gitlab_fn(read_config=read_config, partition_config=partition_config, **options)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise click.ClickException(str(e)) from e


def get_source_cmd() -> click.Group:
    cmd = gitlab_source
    GitlabCliConfig.add_cli_options(cmd)

    # Common CLI configs
    CliReadConfig.add_cli_options(cmd)
    CliPartitionConfig.add_cli_options(cmd)
    cmd.params.append(click.Option(["-v", "--verbose"], is_flag=True, default=False))
    return cmd
