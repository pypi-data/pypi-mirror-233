import calendar
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich import print
from datetime import datetime, timezone
from dateutil import parser
from tickerdax.constants import URL


def truncate_datetime(date, timeframe):
    kwargs = {
        'year': date.year
    }
    if timeframe.endswith(('M', 'd', 'h', 'm')):
        kwargs['month'] = date.month

    if timeframe.endswith(('d', 'h', 'm')):
        kwargs['day'] = date.day

    if timeframe.endswith(('h', 'm')):
        kwargs['hour'] = date.hour

    if timeframe.endswith('m'):
        kwargs['minute'] = date.minute

    return datetime(
        tzinfo=timezone.utc,
        **kwargs
    )


def get_unix_time(date, timeframe):
    return float(calendar.timegm(truncate_datetime(date, timeframe).timetuple()))


def get_timestamp_range(since, till, timeframe):
    """
    Gets a range of timestamps between the start and end dates.

    :param float since: A unix start time.
    :param float till: A unix end time.
    :param str timeframe: The string value of the timeframe, i.e. 1m, 1h, 1d, etc.
    :returns: A list of timestamps.
    :rtype: list[int]
    """
    range_seconds = till - since
    timeframe_in_seconds = convert_timeframe_to_seconds(timeframe)
    time_intervals = range_seconds / timeframe_in_seconds

    timestamps = []
    for time_interval in range(int(time_intervals) + 1):
        timestamps.append(since + (time_interval * timeframe_in_seconds))

    return timestamps


def convert_timeframe_to_seconds(timeframe):
    """
    Converts a timeframe to its value in seconds.

    :param str timeframe: The string value of the timeframe, i.e. 1m, 1h, 1d, etc.
    :returns: The value in seconds.
    :rtype: int
    """
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    return int(timeframe[:-1]) * seconds_per_unit[timeframe[-1]]


def iso_string_to_unix_timestamp(time_string, timeframe):
    """
    Converts iso formatted time string to unix timestamp.

    :param str time_string: A iso formatted time string.
    :param str timeframe: The string value of the timeframe, i.e. 1m, 1h, 1d, etc.
    :returns: A unix timestamp.
    :rtype: int
    """
    return get_unix_time(parser.parse(time_string), timeframe)


def show_download_summary(cached_items, downloaded_items, missing_items, missing_ranges):
    tree = Tree(f'- {cached_items} of the requested items were already cached.\n'
                f'- {downloaded_items} items were downloaded.\n'
                f'- {missing_items} items are missing.',)
    for key, values in missing_ranges.items():
        table = Table(title=key)
        table.add_column("Begins", style="cyan")
        table.add_column("Ends", style="green")

        for start, end in values:
            if start and end:
                table.add_row(
                    datetime.fromtimestamp(start).strftime('%Y-%m-%dT%H:%M:%S'),
                    datetime.fromtimestamp(end).strftime('%Y-%m-%dT%H:%M:%S')
                )
        tree.add(table)
    print(Panel(tree, title="Download Summary"))


def show_routes(routes):
    table = Table(title=f'All Available Routes from {URL}')
    table.add_column("Routes", style="cyan")
    table.add_column("Symbols", style="green")
    table.add_column("Timeframes", style="blue")
    for route in routes:
        table.add_row(
            route['route'],
            ','.join(route['symbols']),
            ','.join(route['timeframes'])
        )
    print()
    print(table)
