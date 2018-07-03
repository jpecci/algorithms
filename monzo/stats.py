
import os
import pandas as pd
import itertools as it
import calendar
from collections import defaultdict

#parameters -------
filename=
dir=
file = os.path.join(dir, filename)
print "Processing file: %s"%file

FROM_YEAR=2018
#------------------

class MonthPeriod:

    def __init__(self, month, year):
        self.month = month
        self.year = year

    def __lt__(self, other):
        return self.year*100+self.month < other.year*100+other.month

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month

    def __repr__(self):
        return "%d %s"%(self.year, calendar.month_abbr[self.month])

    def __hash__(self):
        return hash(self.month) + hash(self.year)

'''
Generate sub category using the first hash tag
'''
def extract_hash_category(notes):
    hash_categories = filter(lambda w: w.startswith('#'), notes.split())
    if len(hash_categories) > 0:
        first = hash_categories[0]
        return first[1:].lower() # trim the hash character
    return 'general'

def build_full_category(monzo_category, hash_category):

    return monzo_category+'-'+hash_category

class Record:

    def __init__(self, ts, amount, monzo_category, hash_category):
        self.ts = ts
        self.amount = amount
        self.monzo_category = monzo_category
        self.hash_category = hash_category

        self.full_category = build_full_category(monzo_category, hash_category)
        self.period = MonthPeriod(ts.month, ts.year)


def select_category(row):

    category = row['category']

    if row['amount'] < 0:
        if "Transfer to pot" in row['description']:
            category="to_pots"

    else:
        if len(row['category']) == 0:
            category = 'incoming'

    return category

with open(file, 'r') as fp:
    data = pd.read_csv(fp, parse_dates=['created']).fillna(value={'notes': '',
                                                                  'category': ''})

records = [Record(row['created'], row['amount'], select_category(row), extract_hash_category(row['notes']))
           for index, row in data.iterrows()]

records = [r for r in records if r.ts.year >= FROM_YEAR]

periods = sorted(set(r.period for r in records))
monzo_categories = set(r.monzo_category for r in records)
full_categories = set(r.full_category for r in records)

monzo2hash_cats=defaultdict(set)  # establish the hierarchy
for r in records:
    monzo2hash_cats[r.monzo_category].add(r.hash_category)

totals = {}
for period in periods:
    totals[period] = {}
    for cat in it.chain(monzo_categories, full_categories):
        totals[period][cat] = 0


records = sorted(records, key=lambda r: r.period)
for period, xs in it.groupby(records, key=lambda r: r.period):
    for cat_to_sort in (lambda r: r.monzo_category, lambda r: r.full_category):
        xs = sorted(xs, key=cat_to_sort)
        for cat, ys in it.groupby(xs, key=cat_to_sort):
            totals[period][cat] = sum(y.amount for y in ys)


totals_per_category ={}
avgs_per_category ={}
for cat in it.chain(monzo_categories, full_categories):
    amounts = [totals[period][cat] for period in totals.keys()]
    total = sum(amounts)
    totals_per_category[cat] = total
    avgs_per_category[cat] = total/float(len(amounts))

totals_per_period = {}
for period in periods:
    amounts = [totals[period][cat] for cat in monzo_categories if cat!="incoming"] #sum over outgoing base_categories only
    totals_per_period[period] = sum(amounts)


#format output --------------
def format_line(caption, values, sum, avg):
    return "%-13s:"%caption + "\t".join("%9s"% v for v in values) + "%9s"%sum + "%9s"%avg

print format_line("Period", periods, "Sum", "Avg")+"\n"

sorted_monzo_categories = sorted(monzo_categories,
                                key=lambda c: totals_per_category[c])

for monzo_cat in sorted_monzo_categories:

    tot = "%.0f"%totals_per_category[monzo_cat]
    avg = "%.0f"%avgs_per_category[monzo_cat]
    values = ["%.0f"%totals[period][monzo_cat] for period in periods]
    print format_line(monzo_cat.upper(), values, tot, avg)

    sorted_hash_categories = sorted(monzo2hash_cats[monzo_cat],
                                   key=lambda h_cat: totals_per_category[build_full_category(monzo_cat,h_cat)])
    if len(sorted_hash_categories) > 1:
        for hash_cat in sorted_hash_categories:
            cat = "   %s"%hash_cat
            full_cat = build_full_category(monzo_cat, hash_cat)
            tot = "%.0f"%totals_per_category[full_cat]
            avg = "%.0f"%avgs_per_category[full_cat]
            values = ["%.0f"%totals[period][full_cat] for period in periods]
            print format_line(cat, values, tot, avg)

values = ["%.0f"%totals_per_period[period] for period in periods]
tot = "%.0f"%sum(totals_per_period[period] for period in periods)
avg = "%.0f"%(float(tot)/len(periods))
print format_line("OUTGOING", values, tot, avg)
