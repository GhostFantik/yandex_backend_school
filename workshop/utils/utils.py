import datetime


def str2datetime(s: str) -> dict[str, datetime.datetime]:
    (begin, end) = s.split('-')
    begin_time = datetime.datetime.strptime(begin, '%H:%M')
    end_time = datetime.datetime.strptime(end, '%H:%M')
    return {
        'begin_time': begin_time,
        'end_time': end_time
    }


def datetime2str(begin: datetime.datetime, end: datetime.datetime) -> str:
    return f'{begin.strftime("%H:%M")}-{end.strftime("%H:%M")}'
