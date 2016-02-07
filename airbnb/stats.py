import pandas as pd
import datetime as dt
import calendar
import itertools as it
from collections import namedtuple


def coalesce(rows):
    ans = rows[0].copy()
    ans['Totale'] = sum(r['Totale'] for r in rows)
    ans['Commissione Host'] = sum(r['Commissione Host'] for r in rows)
    ans['Spese di Pulizia'] = sum(r['Spese di Pulizia'] for r in rows)
    return ans


Split = namedtuple('Split', ['date', 'nights'])


def split(arrival_day, nights):
    cursor_day = arrival_day
    nights_left = nights
    ans = []
    while nights_left > 0:
        _, end = calendar.monthrange(cursor_day.year, cursor_day.month)
        cursor_monthend = dt.date(cursor_day.year, cursor_day.month, end)
        days_to_monthend = (cursor_monthend - cursor_day).days + 1

        nights = min(nights_left, days_to_monthend)
        ans.append(Split(cursor_day, nights))
        cursor_day = cursor_day + dt.timedelta(days=nights)
        nights_left -= nights

    return ans


StatsSplit = namedtuple('SplitReservation', ['date', 'nights', 'px', 'commissions'])


def process_reservation(row):
    amount_paid = row['Totale'] + row['Commissione Host']
    px_night = (amount_paid - row['Spese di Pulizia']) / float(row['Notti'])
    commissions = float(row['Commissione Host']) / (amount_paid - row['Spese di Pulizia'])
    splits = split(row['Arrivo'].to_datetime().date(), row['Notti'])
    ans = []
    for start_split, nights in splits:
        ans.append(StatsSplit(start_split, nights, px_night, commissions))

    return ans


def combine_stats(stats_splits):
    tot_nights = 0
    avg_px = 0
    avg_comm = 0
    start_split = None
    for s in stats_splits:
        if start_split is None:
            start_split = s.date
        tot_nights += s.nights
        avg_px += s.px * s.nights
        avg_comm += s.commissions * s.nights
    avg_px /= float(tot_nights)
    avg_comm /= float(tot_nights)
    return StatsSplit(start_split, tot_nights, avg_px, avg_comm)


fn = '/Users/jacopo/GDrive/Housing/Airbnb/data.csv'
fn = '/Users/jacopo/GDrive/Housing/Airbnb/airbnb_pending.csv'
data_df = pd.read_csv(fn, parse_dates=[3], dayfirst=True)
data_list = [row for idx, row in data_df.iterrows()]
data = []
for codice, it_res in it.groupby(data_list, lambda row: row['Codice di Conferma']):
    data.append(coalesce(list(it_res)))

splits = []
for res in data:
    splits.extend(process_reservation(res))
splits = sorted(splits, key=lambda split: split.date)


def format_stats_title():
    return "{:6} {:6} {:>7} {:7} {:11}".format('Period', 'Nights', 'Price', 'Revenue', 'Commissions')


def format_stats(stats, period_type):
    if period_type == 'year':
        period_str = stats.date.year
    elif period_type == 'month':
        period_str = calendar.month_name[stats.date.month][:3]
    else:
        period_str = stats.date.day
    revenue = stats.px * stats.nights
    return "{:>6} {:6} {:7.1f} {:7.0f} {:11.1%}".format(period_str, stats.nights, stats.px, revenue, stats.commissions)


print format_stats_title()
for month, it_splits in it.groupby(splits, key=lambda split: split.date.month):
    m_splits = list(it_splits)
    for s in m_splits:
        print format_stats(combine_stats([s]), 'day')
    print format_stats(combine_stats(m_splits), 'month')

print format_stats(combine_stats(splits), 'year')
