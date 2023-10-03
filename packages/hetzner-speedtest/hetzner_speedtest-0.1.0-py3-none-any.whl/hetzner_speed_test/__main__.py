from importlib.metadata import PackageNotFoundError, version
from typing import Optional

import typer
from rich import print

import requests
import time
from ping3 import ping
from rich.table import Table
from rich.console import Console

from rich.progress import Progress

app = typer.Typer()

REGIONS = {
    "nbg1": "nbg1-speed.hetzner.com",
    "fsn1": "fsn1-speed.hetzner.com",
    "hel1": "hel1-speed.hetzner.com",
    "ash": "ash-speed.hetzner.com",
    "hil": "hil-speed.hetzner.com",
}

try:
    __version__ = version("hetzner-speed-test")
except PackageNotFoundError:
    __version__ = "dev"


def version_callback(value: bool):
    if value:
        print(__version__)
        raise typer.Exit()


def start_test(region=None, action="both", ping_count=10, chunk_size=1024):
    if action in ["both", "ping"]:
        test_ping(region=region, ping_count=ping_count)
    if action in ["both", "download"]:
        test_download_speed(region=region, chunk_size=chunk_size)


def test_ping(region=None, ping_count=10):
    ping_results = {}
    if region:
        ping_results[region] = []
    else:
        ping_results = {k: [] for k in REGIONS.keys()}

    with Progress(transient=True) as progress:
        ping_task = progress.add_task("Pinging", total=ping_count * len(ping_results.keys()))

        for region in ping_results.keys():
            for _ in range(ping_count):
                ping_results[region].append(ping(REGIONS[region]))
                progress.update(ping_task, advance=1)

    table = Table(title="Ping Results")
    table.add_column("Region")
    table.add_column("Average")
    table.add_column("Min")
    table.add_column("Max")
    for region, results in ping_results.items():
        mean = sum(results) / len(results) * 1000
        table.add_row(region, f"{mean:.0f}", f"{min(results) * 1000:.0f}", f"{max(results) * 1000:.0f}")
    console = Console()
    console.print(table)


def test_download_speed(region=None, chunk_size=1024):
    download_results = {}
    if region:
        download_results[region] = None
    else:
        download_results = {k: None for k in REGIONS.keys()}

    with Progress(transient=True) as progress:
        download_task = progress.add_task("Downloading", total=len(download_results.keys()) * 1024 * 1024 * 100)
        for region in download_results.keys():
            url = f"https://{REGIONS[region]}/100MB.bin"
            download_results[region] = do_download(url, progress, download_task)

    table = Table(title="Download Results")
    table.add_column("Region")
    table.add_column("Speed")
    for region, results in download_results.items():
        table.add_row(region, f"{results:.2f}MB/s")
    console = Console()
    console.print(table)


def do_download(url, progress, task):
    start_time = time.time()

    response = requests.get(url, stream=True)
    content_length = int(response.headers["Content-Length"])

    if response.status_code == 200:
        for _ in response.iter_content(chunk_size=1024):
            progress.update(task, advance=1024)

        end_time = time.time()
        download_time = end_time - start_time
        download_speed = content_length / (download_time * 1024 * 1024)  # Convert bytes to megabytes
        return download_speed


@app.command()
def main(
    region: str = None,
    action: str = typer.Option("both"),
    ping_count: int = 10,
    chunk_size: int = 1024,
    _: Optional[bool] = typer.Option(None, "-v", "--version", callback=version_callback, is_eager=True),
):
    if region and region not in REGIONS.keys():
        print(f"Region not found, must be one of: {', '.join(REGIONS.keys())}")
        raise typer.Exit(1)

    if action not in ["both", "ping", "download"]:
        print("Action must be either `both`, `ping` or `download`")
        raise typer.Exit(2)

    start_test(region=region, action=action, ping_count=ping_count, chunk_size=chunk_size)


if __name__ == "__main__":
    app()
