
import os
import pandas as pd
import itertools as it
import calendar
from collections import defaultdict

#parameters -------
#filename = 'MonzoDataExport_Alltime_2018-06-15_135248.csv'
filename = "monzo_lucia.csv"
dir= r'/Users/jacopo/GDrive/'
file = os.path.join(dir, filename)

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

def build_full_category(base_category, sub_category):

    return base_category+'-'+sub_category

class Record:

    def __init__(self, ts, amount, base_category, sub_category):
        self.ts = ts
        self.amount = amount
        self.base_category = base_category
        self.sub_category = sub_category
        self.full_category = build_full_category(base_category, sub_category)

        self.period = MonthPeriod(ts.month, ts.year)


def extract_sub_category(notes):
    sub_categories = filter(lambda w: w.startswith('#'), notes.split())
    if len(sub_categories) > 0:
        first = sub_categories[0]
        return first[1:].lower() # trim the hash character
    return 'general'


with open(file, 'r') as fp:
    data = pd.read_csv(fp, parse_dates=['created']).fillna(value={'notes': '',
                                                                  'category': ''})

records = []
for index, row in data.iterrows():

    ts = row['created']
    amount = row['amount']
    notes = row['notes']
    description = row['description']

    if amount >= 0:
        category = 'incoming'
    elif "Transfer to pot" in description:
        category="to_pots"
    elif len(row['category']) > 0:
        category = row['category']
    else:
        category = 'N/A'

    records.append(Record(ts, amount, category, extract_sub_category(notes)))


records = [r for r in records if r.ts.year >= FROM_YEAR]

periods = sorted(set(r.period for r in records))
base_categories = set(r.base_category for r in records)
full_categories = set(r.full_category for r in records)

base2sub_cats=defaultdict(set)  # establish the hierarchy
for r in records:
    base2sub_cats[r.base_category].add(r.sub_category)

totals = {}
for period in periods:
    totals[period] = {}
    for cat in it.chain(base_categories, full_categories):
        totals[period][cat] = 0


records = sorted(records, key=lambda r: r.period)
for period, xs in it.groupby(records, key=lambda r: r.period):
    for sorting_cat in (lambda r: r.full_category, lambda r: r.base_category):
        xs = sorted(xs, key=sorting_cat)
        for cat, ys in it.groupby(xs, key=sorting_cat):
            totals[period][cat] = sum(y.amount for y in ys)


totals_per_category ={}
avgs_per_category ={}
for cat in it.chain(base_categories, full_categories):
    amounts = [totals[period][cat] for period in totals.keys()]
    total = sum(amounts)
    totals_per_category[cat] = total
    avgs_per_category[cat] = total/float(len(amounts))

totals_per_period = {}
for period in periods:
    amounts = [totals[period][cat] for cat in base_categories if cat!="incoming"] #sum over outgoing base_categories only
    totals_per_period[period] = sum(amounts)


#print all --------------
def format_line(caption, values, sum, avg):
    return "%-13s:"%caption + "\t".join("%9s"% v for v in values) + "%9s"%sum + "%9s"%avg

print format_line("Period", periods, "Sum", "Avg")+"\n"

sorted_base_categories = sorted(base_categories,
                                key=lambda c: totals_per_category[c])

for base_cat in sorted_base_categories:

    tot = "%.0f"%totals_per_category[base_cat]
    avg = "%.0f"%avgs_per_category[base_cat]
    values = ["%.0f"%totals[period][base_cat] for period in periods]
    print format_line(base_cat.upper(), values, tot, avg)

    sorted_sub_categories = sorted(base2sub_cats[base_cat],
                                   key=lambda sub_cat: totals_per_category[build_full_category(base_cat,sub_cat)])
    if len(sorted_sub_categories) > 1:
        for sub_cat in sorted_sub_categories:
            cat = "   %s"%sub_cat
            full_cat = build_full_category(base_cat, sub_cat)
            tot = "%.0f"%totals_per_category[full_cat]
            avg = "%.0f"%avgs_per_category[full_cat]
            values = ["%.0f"%totals[period][full_cat] for period in periods]
            print format_line(cat, values, tot, avg)

values = ["%.0f"%totals_per_period[period] for period in periods]
tot = "%.0f"%sum(totals_per_period[period] for period in periods)
avg = "%.0f"%(float(tot)/len(periods))
print format_line("OUTGOING", values, tot, avg)
