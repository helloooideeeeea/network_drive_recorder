from datetime import datetime


def date_parse(date_dir):
    return datetime.strptime(date_dir, "%Y%m%d%H%M%S")


def date_format(date_dir):
    return date_parse(date_dir).strftime("%Y年%m月%d日%H時%M分")