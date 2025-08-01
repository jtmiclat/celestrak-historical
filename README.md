# celestrak-historical

Historical celestrak data pulled and saved to git using https://github.com/githubocto/flat.

Pulled every 12 hrs starting July 30, 2025

Inspired from the following

- https://www.keiruaprod.fr/blog/2021/05/23/automated-history-of-celestrak-satellite-data.html
- https://github.com/simonw/git-history

## Usage

**Clone the data**

```bash
git clone git@github.com:jtmiclat/celestrak-historical.git
git pull
git checkout origin/main
```

**Getting all data**

```bash
uv run main.py --norad-id=$NORADID

# Example
# [
#   {
#     "date": "2025-07-30T14:18:55+02:00",
#     "sha": "4f867ff8e38a9ed7a8d1bb8bdd8620d48e03363b",
#     "tle": "ISS (ZARYA)             \n1 25544U 98067A   25211.15559314  .00012687  00000+0  22820-3 0  9994\n2 25544  51.6363  94.0992 0002130 129.4737   6.6755 15.50214428521827"
#   }
# ]
```

**Getting all latest**

```bash
uv run main.py --norad-id $NORADID --no-progress-bar | jq -r '.[0].tle'
```

**Fetching for certain ranges**

```bash
uv run main.py --start 2025-07-31 --end 2025-07-01 --norad-id $NORADID --no-progress-bar | jq -r '.[0].tle'
```

## License

MIT for the code
