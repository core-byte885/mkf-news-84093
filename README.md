# news-image-20261119

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/core-byte885/mkf-news-84093/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/core-byte885/mkf-news-84093/reward.svg)](https://make.fun/bounty/news-image-20261119)

A newspaper-style front page summarizing world news of Thursday 19 November 2026, drawn with a hand-built 5x7 bitmap font and pure `zlib`/`struct` PNG encoding (Python standard library only, no network).

## Run

```bash
python3 main.py
```

Writes `entry.png` (1024x768) to `$MAKEFUN_OUTPUT_DIR` (default `./out/`). Deterministic: two runs produce byte-identical output.

## License

MIT - see LICENSE.
