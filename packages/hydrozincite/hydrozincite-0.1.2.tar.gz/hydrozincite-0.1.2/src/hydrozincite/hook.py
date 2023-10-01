from pathlib import Path

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from . import repo
from .config.config import conf


def is_hook(hook, return_hook=False):
    if not hook.exists():
        return "[red]❌[/red]" if not return_hook else hook
    name = hook.name
    with hook.open() as h:
        read = h.read()
        if hooks[name] == read:
            return "[green]✔️[green]" if not return_hook else None
        else:
            return (
                Panel(
                    Syntax(read, "bash", theme="monokai", line_numbers=True),
                    border_style="red",
                )
                if not return_hook
                else hook
            )


hooks = {
    "post-receive": "#!/usr/bin/env bash\n\nhydrozincite",
    "post-update": "#!/usr/bin/env bash\n\nexec git update-server-info",
}


def list():
    repositories = repo.get_all_bare(Path(conf["repositories"]))

    console = Console()
    console.print(
        Columns(
            Panel(
                Syntax(bash, "bash", theme="monokai", line_numbers=True),
                title="[yellow]%s[/yellow]" % hook,
                title_align="left",
            )
            for hook, bash in hooks.items()
        )
    )

    table = Table(
        title="Hydrozincite - Zn₅(CO₃)₂(OH)₆",
        show_header=True,
        row_styles=["none", "dim"],
        expand=False,
    )
    table.add_column(
        "Repository", justify="left", style="cyan", header_style="cyan", no_wrap=True
    )
    for hook in hooks.keys():
        table.add_column(hook, justify="center")

    for r in repositories:
        path = r.path.relative_to(Path(conf["repositories"]))
        repo_hooks = [is_hook(r.hooks[hook]) for hook in hooks]
        table.add_row(path.as_posix(), *repo_hooks)

    console.print(table)


def write():
    console = Console()
    repositories = repo.get_all_bare(Path(conf["repositories"]))

    for r in repositories:
        path = r.path.relative_to(Path(conf["repositories"]))
        repo_hooks = [
            is_hook(r.hooks[hook], return_hook=True)
            for hook in hooks
            if is_hook(r.hooks[hook], return_hook=True) is not None
        ]
        if not repo_hooks:
            continue

        panel = []

        for hook in repo_hooks:
            if hook is None:
                continue
            with hook.open("w") as f:
                f.write(hooks[hook.name])
            hook.chmod(0o755)
            panel.append(
                "> [green]%s[/green]" % hook.relative_to(Path(conf["repositories"]))
            )

        console.print(
            Panel(
                "\n".join(panel),
                title="[cyan]%s[/cyan]" % path.as_posix(),
                title_align="left",
                highlight=True,
                expand=False,
            )
        )
