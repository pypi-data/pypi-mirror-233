from argparse import ArgumentParser
from datetime import date
from pathlib import Path

import polars as pl

from glutamate.database import E621DataFrameDB, Query
from glutamate.datamodel import ANY_EXT, ANY_RATING, EXT, Rating


parser = ArgumentParser('glutamate', description='Glutamate CLI.')

subparsers = parser.add_subparsers(title='actions')

query_options = subparsers.add_parser('query')
query_options.add_argument('--posts', type=Path, required=True, help='Path to posts file')
query_options.add_argument('--tags', type=Path, required=True, help='Path to tags file')
query_options.add_argument('--files-naming', nargs='?',
                           choices=['id', 'md5'], default='id',
                           help='Download selected posts',
                           )
filters = query_options.add_argument_group(title='filters')
filters.add_argument('--required', nargs='*',
                     default=[],
                     help='Required tags. If post contains any of this tags post will be included to reslting set.',
                     )
filters.add_argument('--blacklist', nargs='*',
                     default=[],
                     help='Blacklisted tags. If post contains any of this tags post will NOT be included to reslting set.',
                     )
filters.add_argument('--extensions', nargs='*',
                     default=[],
                     help='Extensions filter. Only posts with images of selected extensions will be included to reslting set.',
                     )  # EXT | Iterable[EXT] = ANY_EXT
filters.add_argument('--ratings', nargs='*',
                     choices=['s', 'q', 'e'], default=[],
                     help='Posts rating filter.',
                     )  # Rating | Iterable[Rating] = ANY_RATING
filters.add_argument('--min-score', nargs='?',
                     type=int, default=0,
                     help='Posts score filter.',
                     )
filters.add_argument('--min-favs', nargs='?',
                     type=int, default=0,
                     help='Posts favorites count filter.',
                     )
filters.add_argument('--min-date', nargs='?',
                     type=date.fromisoformat,
                     help='Posts date filter. Should be in YYYY-MM-DD format.',
                     )
filters.add_argument('--min-area', nargs='?',
                     type=int, default=0,
                     help='Images area filter.',
                     )
filters.add_argument('--top-n', nargs='?',
                     type=int,
                     )
filters.add_argument('--add-rate-tags', nargs='*')  # Rating | Iterable[Rating] = ANY_RATING
# filters.add_argument('--skip-posts', nargs='*')  # Iterable[int | str] = ()
downloading = query_options.add_argument_group(title='downloading')
downloading.add_argument('--download-posts', action='store_true',
                         default=False,
                         help='Download selected posts',
                         )
downloading.add_argument('--proxy-url', nargs='?',
                         help='URL of proxy which will be used for downloading. '
                              'Should be in format {protocol}://[user:password@]{host}[:port].',
                         )
writing_captions = query_options.add_argument_group(title='captions writing')
writing_captions.add_argument('--write-captions-to', type=Path, nargs='?')
writing_stats = query_options.add_argument_group(title='stats writing')
writing_stats.add_argument('--write-stats-to', type=Path, nargs='?')
query_options.add_argument('--output-file', type=Path, required=True, help='Path for file to write selected posts info to')

download_options = subparsers.add_parser('download')
download_options.add_argument('--posts', type=Path, required=True, help='Path to posts file')
download_options.add_argument('--images-directory', type=Path, required=True)
download_options.add_argument('--proxy-url', nargs='?')

captions_options = subparsers.add_parser('write-captions')
captions_options.add_argument('--posts', type=Path, required=True, help='Path to posts file')
captions_options.add_argument('--captions-path', type=Path)

stats_options = subparsers.add_parser('write-stats')
stats_options.add_argument('--posts', type=Path, required=True, help='Path to posts file')
stats_options.add_argument('--stats-path', type=Path)


def main(argv: list[str]):
    args = parser.parse_args(argv)
    if 'required' in args:
        query_posts(args)
    elif 'images_directory' in args:
        download_posts(args)
    elif 'captions_path' in args:
        write_captions(args)
    elif 'stats_path' in args:
        write_stats(args)
    else:
        raise ValueError(f'Unexpected input: {argv}')


def query_posts(args):
    print(args)
    posts_path: Path = args.posts
    tags_path: Path = args.tags
    include_tags = args.required
    exclude_tags = args.blacklist
    extensions = [EXT(ext) for ext in args.extensions] or ANY_EXT
    ratings = [Rating(rating) for rating in args.ratings] or ANY_RATING
    min_score = args.min_score
    min_favs = args.min_favs
    min_date = args.min_date
    min_area = args.min_area
    top_n = args.top_n
    download_posts = args.download_posts
    if posts_path.suffix == 'csv':
        posts_df = pl.scan_csv(posts_path)
    elif posts_path.suffix == 'parquet':
        posts_df = pl.scan_parquet(posts_path)
    else:
        raise ValueError(f'Unknown posts file extension: "{posts_path.suffix}"')
    if posts_path.suffix == 'csv':
        tags_df = pl.scan_csv(posts_path)
    elif posts_path.suffix == 'parquet':
        tags_df = pl.scan_parquet(posts_path)
    else:
        raise ValueError(f'Unknown posts file extension: "{tags_path.suffix}"')
    e6db = E621DataFrameDB(posts_df=posts_df, tags_df=tags_df)
    query = Query(
        include_tags=include_tags, exclude_tags=exclude_tags,
        extensions=extensions, ratings=ratings,
        min_score=min_score, min_favs=min_favs, min_date=min_date, min_area=min_area,
        top_n=top_n
    )
    posts = e6db.select_posts(query)


def download_posts(args):
    print(args)


def write_captions(args):
    print(args)


def write_stats(args):
    print(args)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
