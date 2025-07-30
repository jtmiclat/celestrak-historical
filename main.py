import click
import json
import git
from itertools import batched

relative_path = "raw-data/tle-data.txt"
branch_name = "main"
show_progress = True  # Set to False to disable progress bar

def parse_tle_file(content: bytes):
    """Parse TLE file content and yield lines."""
    lines = content.decode('utf-8').strip().splitlines()
    tles = {}
    for tle in batched(lines, 3):
        norad_id = tle[2].split()[1]
        tles[norad_id] = '\n'.join(tle).strip()
    return tles

def get_tle_data(noradid: str, show_progress: bool):
    """Get TLE data for a specific NORAD ID."""
    repo = git.Repo(".", odbt=git.GitDB)
    commits = reversed(list(repo.iter_commits(branch_name, paths=[relative_path])))
    progress_bar = None
    if show_progress:
        progress_bar = click.progressbar(commits, show_pos=True, show_percent=True)
    for commit in commits:
        if progress_bar:
            progress_bar.update(1)
        try:
            content = commit.tree[relative_path].data_stream.read()
            tles = parse_tle_file(content)
            tle = tles[noradid]
            yield commit.committed_datetime, commit.hexsha, tle
        except KeyError:
            continue

@click.command()
@click.option('--output', default="-",  help='Path to the file in the')
@click.option('--norad-id', required=True, help='NORAD ID of the satellite')
@click.option('--progress-bar/--no-progress-bar', default=True)
def main(output: str, norad_id: str, progress_bar: bool):
    info = get_tle_data(norad_id, show_progress=progress_bar)
    dedup = set()
    results = []
    for date, sha, tle in info:
        if tle in dedup:
            # already seen this TLE, skip it. this usually means the tle was not updated
            continue
        results.append(dict(date=date.isoformat(), sha=sha, tle=tle))
        dedup.add(tle)
    if output == "-":
        click.echo("\n")
        click.echo(json.dumps(results, indent=2))
    else:
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
