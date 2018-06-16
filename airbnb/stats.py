import pandas as pd
import datetime as dt
import calendar
import itertools as it
from collections import namedtuple
import os

 
FILE_HEADER=['Data',
 'Tipo',
 'Codice di Conferma',
 'Arrivo',
 'Notti',
 'Ospite',
 'Annuncio',
 'Dettagli',
 'Referenza',
 'Valuta',
 'Totale', #Total paid to my bank account, hence reduced by the Airbnb commissions and including cleaning
 'Pagamento',
 'Commissione Host', #commission I pay to Airbnb
 'Spese di Pulizia'
 ]


def merge_records_of_reservation(r1, r2):
    '''used to merge:
    1) a reservation longer than 1 month which  comes split 
        in monthly records in the Airbnb report
    2) adjustments to change the value of a reservation'''

    if (r1['Codice di Conferma'] != r2['Codice di Conferma']):
        raise Exception('trying to merge two records of different reservations')

    sum_field = lambda r1,r2,field: r1[field]+r2[field]
    ans=r1.copy()
    ans['Totale'] = sum_field(r1, r2, 'Totale')
    ans['Commissione Host'] = sum_field(r1, r2, 'Commissione Host')
    ans['Spese di Pulizia'] = sum_field(r1, r2, 'Spese di Pulizia')  
    #Arrivo: is already set to the very beginning of the staying
    #Notti: is already set to the sum of all the nights
    return ans
 

Period = namedtuple('Period', ['date', 'nights'])

def split_in_monthly_periods(arrival_day, nights):
    cursor_day = arrival_day
    nights_left = nights 

    while nights_left > 0:
        _, end = calendar.monthrange(cursor_day.year, cursor_day.month)
        cursor_monthend = dt.date(cursor_day.year, cursor_day.month, end)
        days_to_monthend = (cursor_monthend - cursor_day).days + 1

        nights = min(nights_left, days_to_monthend)
        yield Period(cursor_day, nights)
        cursor_day = cursor_day + dt.timedelta(days=nights)
        nights_left -= nights
 

def get_pxnight_commissions(r):
    amount_paid = r['Totale'] + r['Commissione Host']
    px_night=0 #needed to deal with adjustments that cancel a reservation
    commissions=0
    if amount_paid > 0:
        #this is the px I should put on Airbnb website
        px_night = (amount_paid - r['Spese di Pulizia']) / float(r['Notti'])
        commissions = float(r['Commissione Host']) / (amount_paid - r['Spese di Pulizia'])
    return px_night, commissions


MonthlyStats = namedtuple('MonthlyStats', ['date', 'nights', 'px', 'px2', 'commissions'])

def combine_stats(splits, length_period):
    tot_nights = 0
    avg_px = 0
    avg_comm = 0
    start_split = None
    for s in splits:
        if start_split is None:
            start_split = s.date
        tot_nights += s.nights
        avg_px += s.px * s.nights
        avg_comm += s.commissions * s.nights
    avg2_px=avg_px 
    avg_px /= float(tot_nights)
    avg2_px /= float(length_period) #average price if we had a 100% occupancy
    avg_comm /= float(tot_nights)
    return MonthlyStats(start_split, tot_nights, avg_px, avg2_px, avg_comm)


#----------------------------------------------------
#----------------- START SCRITP ---------------------
#----------------------------------------------------

#read multiple files
dir='/Users/jacopo/GDrive/Housing/Short_term_inverness/'
files=filter(lambda d: d.startswith("airbnb_"), os.listdir(dir)) 
fn_adj=os.path.join(dir, 'adjustments.csv')

fns=map(lambda f:os.path.join(dir, f), files)

#combine in the same dataframe
dfs=[pd.read_csv(fn, parse_dates=[0,3], dayfirst=True, names=FILE_HEADER, header=0) for fn in fns]
df=pd.concat(dfs, ignore_index=True ) 
df['Commissione Host']=df['Commissione Host'].fillna(0)
df['Spese di Pulizia']=df['Spese di Pulizia'].fillna(0)

#load and concat adjustments
df_adj=pd.read_csv(fn_adj, parse_dates=[0,3], dayfirst=True, names=FILE_HEADER+['Adjustment','Notes'], header=0)
df_adj['Commissione Host']=df_adj['Commissione Host'].fillna(0)
df_adj['Spese di Pulizia']=df_adj['Spese di Pulizia'].fillna(0)

for field in ['Totale', 'Commissione Host','Spese di Pulizia']:
    df_adj[field]*=df_adj['Adjustment'] 
df_adj=df_adj[FILE_HEADER]

df=pd.concat([df, df_adj[FILE_HEADER]], ignore_index=True ) 

#coalesce single reservations split in multiple records
df=df.sort_values(by='Codice di Conferma')
reservations = [] 
for _, iter_records in it.groupby([r for _, r in df.iterrows()], lambda r: r['Codice di Conferma']):
    reservation=reduce(merge_records_of_reservation, iter_records )
    reservations.append(reservation)
   
#split reservations spanning across more then one month for monthly stats
Split = namedtuple('Split', ['code', 'date', 'nights', 'px', 'commissions'])
splits = []
for r in reservations:
    px_night, commissions= get_pxnight_commissions(r)
    periods = split_in_monthly_periods(r['Arrivo'].to_datetime().date(), r['Notti'])
    r_splits=map(lambda p: Split(r['Codice di Conferma'],p.date, p.nights, px_night, commissions), periods)
    splits.extend(r_splits)

def format_stats_title():
    return "{:6} {:6} {:>7} {:7} {:11}".format('Period', 'Nights', 'Price', 'Revenue', 'Commissions')


def format_stats(stats, period_type):
    revenue = stats.px * stats.nights

    if period_type == 'year':
        period_str = stats.date.year
        return "{:>6} {:6} {:7.1f}/{:4.1f} {:7.0f} {:11.1%}".format(period_str, stats.nights, stats.px, stats.px2, revenue, stats.commissions)
    elif period_type == 'month':
        period_str = calendar.month_name[stats.date.month][:3]
        return "{:>6} {:6} {:7.1f}/{:4.1f} {:7.0f} {:11.1%}".format(period_str, stats.nights, stats.px, stats.px2, revenue, stats.commissions)
    else:
        period_str = stats.date.day
        return "{:>6} {:6} {:7.1f} {:7.0f} {:11.1%} {}".format(period_str, stats.nights, stats.px, revenue, stats.commissions,stats.code)

    
splits.sort(key=lambda s: s.date)
print format_stats_title()
for year, year_splits in it.groupby(splits, key=lambda split: split.date.year):
    year_splits=tuple(year_splits)

    for month, month_splits in it.groupby(year_splits, key=lambda split: split.date.month):
        month_splits=tuple(month_splits)

        print calendar.month_name[month][:3].upper()+' '+'-'*(len(format_stats_title())-4) 
        for s in month_splits:
            print format_stats(s, 'day')
        
        days_in_month=calendar.monthrange(year, month)[1]
        print format_stats(combine_stats(month_splits, days_in_month), 'month')
        print ''

    print '-'*(len(format_stats_title())) 
    days_in_year=365
    print format_stats(combine_stats(year_splits, days_in_year), 'year') 
    print "\n" 
