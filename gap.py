import argparse
import datetime
import dateutil
import git
import pandas
import plotnine as p9
import sys

from statsmodels.duration.survfunc import SurvfuncRight


def dates_to_duration(dates, *, window_size=20):
    """
    Convert a list of dates into a list of durations
    (between consecutive dates). The resulting list is composed of
    'window_size' durations.
    """
    dates = sorted(set(dates))
    kept = dates[-window_size - 1:]  # -1 because intervals vs. bounds
    durations = []
    for first, second in zip(kept[:-1], kept[1:]):
        duration = (second - first).days - 1
        durations.append(duration)

    return durations


def model(durations, probabilities=[0.5, 0.75, 0.9], *, return_surv=False):
    """
    Return the durations corresponding to given probabilities, using survival analysis.
    """
    surv = SurvfuncRight(durations, [1] * len(durations))
    if return_surv:
        return surv
    else:
        return [surv.quantile(p) for p in probabilities]


def cli():
    parser = argparse.ArgumentParser(description='GAP - Git Activity Predictor')
    parser.add_argument('paths', metavar='PATH', type=str, nargs='*', default=['.'], help='Paths to one or more git repositories')
    parser.add_argument('--date', type=lambda d: dateutil.parser.parse(d).date(), required=False, default=datetime.date.today(), help='Date used for predictions (default to current date)')
    parser.add_argument('--obs', type=int, required=False, default=20, help='Number of observations to consider')
    parser.add_argument('--probs', metavar='PROB', type=float, nargs='*', required=False, default=[0.5, 0.7, 0.9], help='Probabilities to output, strictly in [0,1].')
    parser.add_argument('--limit', type=int, required=False, default=30, help='Limit contributors to the one that were active at least once during the last x days (default 30)')
    parser.add_argument('--mapping', type=str, nargs='?', help='Mapping file to merge identities. This file must be a csv file where each line contains two values: the name to be merged, and the corresponding identity. Use "IGNORE" as identity to ignore specific names.')
    parser.add_argument('--branches', metavar='BRANCH', type=str, nargs='*', default=list(), help='Git branches to analyse (default to all).')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--text', action='store_true', help='Print results as text.')
    group.add_argument('--csv', action='store_true', help='Print results as csv.')
    group.add_argument('--json', action='store_true', help='Print results as json.')
    group.add_argument('--plot', nargs='?', const=True, help='Export results to a plot. Filepath can be optionaly specified.')

    args = parser.parse_args()

    # Default plot location
    if args.plot is True:
        args.plot = str(args.date) + '.pdf'

    # Default to text if not other option is provided
    if not args.csv and not args.json and not args.plot:
        args.text = True

    # Identity mapping
    if args.mapping:
        d = pandas.read_csv(args.mapping, names=['source', 'target'])
        mapping = {r.source: r.target for r in d.itertuples()}
    else:
        mapping = {}

    raw_data = dict()  # author -> dates of activity

    # Get information from git
    for path in args.paths:
        try:
            repo = git.Repo(path)
        except Exception as e:  # Must be refined
            print('Unable to access repository {} ({}:{})'.format(path, e.__class__.__name__, e))
            sys.exit()

        # Default branches
        if len(args.branches) == 0:
            commits = repo.iter_commits('--all')
        else:
            commits = repo.iter_commits(' '.join(args.branches))

        for commit in commits:
            try:
                author = commit.author.name
                identity = mapping.get(author, author)
                if author.lower() != 'ignore' and identity.lower() == 'ignore':
                    continue

                date = datetime.date.fromtimestamp(commit.authored_date)
                raw_data.setdefault(identity, []).append(date)
            except Exception as e:
                print('Unable to read commit ({}: {}): {}'.format(e.__class__.__name__, e, commit))

    # Compute durations and apply model
    data = []  # (author, past activities, predicted durations)

    for author, commits in raw_data.items():
        commits = sorted([e for e in commits if e <= args.date])
        durations = dates_to_duration(commits, window_size=args.obs)

        if len(durations) >= args.obs:
            predictions = model(durations, args.probs)
            last_day = [e for e in commits if e <= args.date][-1]

            if last_day >= args.date - datetime.timedelta(args.limit):
                data.append((
                    author,
                    commits,
                    predictions,
                ))

    # Prepare dataframe
    df = pandas.DataFrame(
        index=set([a for a, c, p in data]),
        columns=['last'] + args.probs
    )
    if len(df) == 0:
        print('No author has {} observations and was active at least once during the last {} days'.format(args.obs, args.limit))
        sys.exit()

    df.index.name = 'author'

    if not args.plot:
        for author, commits, predictions in data:
            last = commits[-1]
            df.at[author, 'last'] = last
            for prob, p in zip(args.probs, predictions):
                df.at[author, prob] = last + datetime.timedelta(days=int(p))
        df = df.sort_values('last', ascending=False)
        df = df.astype(str)

        if args.text:
            pandas.set_option('expand_frame_repr', False)
            pandas.set_option('display.max_columns', 999)
            print(df)
        elif args.csv:
            print(df.to_csv())
        elif args.json:
            print(df.to_json(orient='index'))
    else:
        # Because of plotnine's way of initializing matplotlib
        import warnings
        warnings.filterwarnings("ignore")

        VIEW_LIMIT = 28

        activities = []  # List of (author, day) where day is a delta w.r.t. given date
        forecasts = []  # List of (author, from_day, to_day, p) where probability p
                        # applies between from_day and to_day (delta w.r.t. given date)

        for author, commits, predictions in data:
            last = (commits[-1] - args.date).days
            for e in commits:
                activities.append((author, (e - args.date).days))

            previous = 0
            for d, p in zip(predictions, args.probs):
                forecasts.append((
                    author, last + previous, last + d, p
                ))
                previous = d

        activities = pandas.DataFrame(columns=['author', 'day'], data=activities)
        forecasts = pandas.DataFrame(columns=['author', 'fromd', 'tod', 'p'], data=forecasts)

        plot = (
            p9.ggplot(p9.aes(y='author'))
            + p9.geom_segment(
                p9.aes('day - 0.5', 'author', xend='day + 0.5', yend='author'),
                data=activities,
                size=4,
                color='orange',
            )
            + p9.geom_segment(
                p9.aes('fromd + 0.5', 'author', xend='tod + 0.5', yend='author', alpha='factor(p)'),
                data=forecasts,
                size=4,
                color='steelblue',
            )
            + p9.geom_vline(xintercept=0, color='r', alpha=0.5, linetype='dashed')
            + p9.scale_x_continuous(name='  <<  past days {:^20} future days  >>'.format(str(args.date)), breaks=range(-VIEW_LIMIT // 7 * 7, (VIEW_LIMIT // 7 * 7) + 1, 7), minor_breaks=6)
            + p9.scale_y_discrete(name='', limits=activities.sort_values('day', ascending=False)['author'].unique())
            + p9.scale_alpha_discrete(range=(1, 0.2),  name=' ')
            + p9.coord_cartesian(xlim=(-VIEW_LIMIT, VIEW_LIMIT))
            + p9.theme_matplotlib()
            + p9.theme(
                figure_size=(6, 4 * activities['author'].nunique() / 15)
            )
        )

        fig = plot.draw()
        fig.savefig(args.plot, bbox_inches='tight')
        print('Plot exported to {}'.format(args.plot))


if __name__ == '__main__':
    cli()