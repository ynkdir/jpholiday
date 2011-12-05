#!/usr/bin/env python3
# 内閣府/「国民の祝日」について
# http://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html
# 国立天文台/暦要項
# http://eco.mtk.nao.ac.jp/koyomi/yoko/
# 国民の祝日 - Wikipedia
# http://ja.wikipedia.org/wiki/%E5%9B%BD%E6%B0%91%E3%81%AE%E7%A5%9D%E6%97%A5

import sys
import argparse
import datetime


MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATUEDAY = 5
SUNDAY = 6


option_parser = argparse.ArgumentParser()
option_parser.add_argument("-f", type=int, required=True, help="from year")
option_parser.add_argument("-t", type=int, required=True, help="to year")


# うるう年
def isleapyear(year):
    return (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))


# 第何曜日
def nthweekday(year, month, weekday, nth):
    date = datetime.date(year, month, 1)
    n = 0
    while True:
        if date.weekday() == weekday:
            n += 1
        if n == nth:
            break
        date += datetime.timedelta(days=1)
    return date


# 祝日としての春分の日・秋分の日は、前年の2月1日に、春分の日・秋分の日の
# 日付が書かれた「暦要項（れきようこう）」が官報に掲載されることによっ
# て、正式決定となる。
# 春分の日 - Wikipedia
# http://ja.wikipedia.org/wiki/%E6%98%A5%E5%88%86%E3%81%AE%E6%97%A5
def shunnbunn(year):
    if year % 4 == 0:
        if 1900 <= year <= 1956:
            return datetime.date(year, 3, 21)
        elif 1960 <= year <= 2088:
            return datetime.date(year, 3, 20)
        elif 2092 <= year <= 2096:
            return datetime.date(year, 3, 19)
    elif year % 4 == 1:
        if 1901 <= year <= 1989:
            return datetime.date(year, 3, 21)
        elif 1993 <= year <= 2097:
            return datetime.date(year, 3, 20)
    elif year % 4 == 2:
        if 1902 <= year <= 2022:
            return datetime.date(year, 3, 21)
        elif 2026 <= year <= 2098:
            return datetime.date(year, 3, 20)
    elif year % 4 == 3:
        if 1903 <= year <= 1923:
            return datetime.date(year, 3, 22)
        elif 1927 <= year <= 2055:
            return datetime.date(year, 3, 21)
        elif 2059 <= year <= 2099:
            return datetime.date(year, 3, 20)
    return None


# 祝日としての春分の日・秋分の日は、前年の2月1日に、春分の日・秋分の日の
# 日付が書かれた「暦要項（れきようこう）」が官報に掲載されることによっ
# て、正式決定となる。
# 秋分の日
# http://ja.wikipedia.org/wiki/%E7%A7%8B%E5%88%86%E3%81%AE%E6%97%A5
def shuubunn(year):
    if year % 4 == 0:
        if 1900 <= year <= 2008:
            return datetime.date(year, 9, 23)
        elif 2012 <= year <= 2096:
            return datetime.date(year, 9, 22)
    elif year % 4 == 1:
        if 1901 <= year <= 1917:
            return datetime.date(year, 9, 24)
        elif 1921 <= year <= 2041:
            return datetime.date(year, 9, 23)
        elif 2045 <= year <= 2097:
            return datetime.date(year, 9, 22)
    elif year % 4 == 2:
        if 1902 <= year <= 1946:
            return datetime.date(year, 9, 24)
        elif 1950 <= year <= 2074:
            return datetime.date(year, 9, 23)
        elif 2078 <= year <= 2098:
            return datetime.date(year, 9, 22)
    elif year % 4 == 3:
        if 1903 <= year <= 1979:
            return datetime.date(year, 9, 24)
        elif 1983 <= year <= 2099:
            return datetime.date(year, 9, 23)
    return None


# 明治 西暦=和暦+1867 1868-09-08 - 1912-07-30
# 大正 西暦=和暦+1911 1912-07-30 - 1926-12-25
# 昭和 西暦=和暦+1925 1926-12-25 - 1989-01-07
# 平成 西暦=和暦+1988 1989-01-08 - ...
def wareki(year):
    if 1868 <= year <= 1911:
        return ("明治", year - 1867)
    elif 1912 <= year <= 1925:
        return ("大正", year - 1911)
    elif 1926 <= year <= 1988:
        return ("昭和", year - 1925)
    elif 1989 <= year:
        return ("平成", year - 1988)


# (start, end, name, factory)
# end=9999 for the present system
JPHOLIDAYS = [
        (1949, 9999, "元日", lambda year: datetime.date(year, 1, 1)),
        (1949, 1999, "成人の日", lambda year: datetime.date(year, 1, 15)),
        (2000, 9999, "成人の日", lambda year: nthweekday(year, 1, MONDAY, 2)),
        (1967, 9999, "建国記念の日", lambda year: datetime.date(year, 2, 11)),
        (1949, 9999, "春分の日", lambda year: shunnbunn(year)),
        (1949, 1988, "天皇誕生日", lambda year: datetime.date(year, 4, 29)),
        (1989, 2006, "みどりの日", lambda year: datetime.date(year, 4, 29)),
        (2007, 9999, "昭和の日", lambda year: datetime.date(year, 4, 29)),
        (1949, 9999, "憲法記念日", lambda year: datetime.date(year, 5, 3)),
        (2007, 9999, "みどりの日", lambda year: datetime.date(year, 5, 4)),
        (1949, 9999, "こどもの日", lambda year: datetime.date(year, 5, 5)),
        (1996, 2002, "海の日", lambda year: datetime.date(year, 7, 20)),
        (2003, 9999, "海の日", lambda year: nthweekday(year, 7, MONDAY, 3)),
        (1966, 2002, "敬老の日", lambda year: datetime.date(year, 9, 15)),
        (2003, 9999, "敬老の日", lambda year: nthweekday(year, 9, MONDAY, 3)),
        (1948, 9999, "秋分の日", lambda year: shuubunn(year)),
        (1966, 1999, "体育の日", lambda year: datetime.date(year, 10, 10)),
        (2000, 9999, "体育の日", lambda year: nthweekday(year, 10, MONDAY, 2)),
        (1948, 9999, "文化の日", lambda year: datetime.date(year, 11, 3)),
        (1948, 9999, "勤労感謝の日", lambda year: datetime.date(year, 11, 23)),
        (1989, 9999, "天皇誕生日", lambda year: datetime.date(year, 12, 23)),
        (1959, 1959, "皇太子・明仁親王の結婚の儀", lambda year: datetime.date(year, 4, 10)),
        (1989, 1989, "昭和天皇の大喪の礼", lambda year: datetime.date(year, 2, 24)),
        (1990, 1990, "即位の礼正殿の儀", lambda year: datetime.date(year, 11, 12)),
        (1993, 1993, "皇太子・徳仁親王の結婚の儀", lambda year: datetime.date(year, 6, 9)),
        ]


# 振替休日
# 1973-2006: 国民の祝日が日曜日となった翌日の平日。
# 2007-    : 国民の祝日が日曜日となった日の後の最初の平日。
def furikae(year, days):
    if year <= 1972:
        return days
    elif 1973 <= year <= 2006:
        i = 0
        while i < len(days):
            if days[i][0] < datetime.date(1973, 4, 29):
                # not yet applied
                pass
            elif days[i][0].weekday() == SUNDAY:
                day = days[i][0] + datetime.timedelta(days=1)
                if i + 1 >= len(days) or day != days[i + 1][0]:
                    i += 1
                    days.insert(i, (day, "振替休日"))
            i += 1
        return days
    elif 2007 <= year:
        i = 0
        while i < len(days):
            if days[i][0].weekday() == SUNDAY:
                day = days[i][0] + datetime.timedelta(days=1)
                i += 1
                while i < len(days) and day == days[i][0]:
                    day = days[i][0] + datetime.timedelta(days=1)
                    i += 1
                days.insert(i, (day, "振替休日"))
            i += 1
        return days


# 国民の休日
# 2つの祝日に挟まれた平日（月曜日は振替休日のため除く）。
def kokumin(year, days):
    if year <= 1987:
        return days
    elif 1988 <= year:
        i = 1
        while i < len(days):
            if days[i][0] - days[i - 1][0] == datetime.timedelta(days=2):
                day = days[i][0] - datetime.timedelta(days=1)
                if day.weekday() != SUNDAY and day.weekday() != MONDAY:
                    days.insert(i, (day, "国民の休日"))
                    i += 1
            i += 1
        return days


# 祝日
def holidays(year):
    days = []
    for start, end, name, factory in JPHOLIDAYS:
        if start <= year <= end:
            days.append((factory(year), name))
    days = furikae(year, days)
    days = kokumin(year, days)
    days.sort()
    return days


def main(args=None):
    args = option_parser.parse_args(args)
    for year in range(args.f, args.t + 1):
        for date, name in holidays(year):
            nengo, nen = wareki(date.year)
            print("%s,%s%d年,%s" % (date, nengo, nen, name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
