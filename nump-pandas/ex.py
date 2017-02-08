import csv
from datetime import datetime
import re
import pandas
import matplotlib.pyplot as plt

def valid_date(s):
    try:
        datetime.strptime(s, "%m-%d-%y")
        return True
    except ValueError as err:
        print(err)

def regexp_date(s):
    pattern = r'\d{2}[-/]\d{2}[-/]\d{2}'
    matches = re.match(pattern, s)
    return matches


raw_data = 'data/exercise_log.csv'
prep_data = []

def chart(data_frame):
    #data_frame.plot()

    #data_frame.date = pandas.to_datetime(data_frame['date'], format='%m-%d-%y') #optional, allows date formatting
    data_frame.set_index('date', inplace=True) #will not work without inplace=True
    data_frame['p_total'].plot()
    data_frame['c_total'].plot()
    plt.show() # keeps global plotting context, that's how it knows

def normalize(prep_data):
    for entry in prep_data:
        p = []
        c = []
        for date,numbers in entry.items():
            for ix, number in enumerate(numbers):
                if ix %2 == 0:
                    p.append(int(number))
                else:
                    c.append(int(number))
        p_total = sum(p)
        p_sets  = len(p)
        p_max   = max(p)
        p_min   = min(p)
        c_total = sum(c)
        c_sets  = len(c)
        c_max = max(c)
        c_min = min(c)
        entry[date]={'date'   : date,
                     'p_max'  :  p_max,
                     'p_min'  :  p_min,
                     'p_total':  p_total,
                     'p_sets' :  p_sets,
                     'c_max'  :  c_max,
                     'c_min'  :  c_min,
                     'c_total':  c_total,
                     'c_sets' :  c_sets }
    print (prep_data)
    li = []
    for entry in prep_data:
        for values in entry.values():
            li.append(values)

    print (li)
    x = pandas.DataFrame(li)
    print (x)
    chart(x)


with open(raw_data) as f:
    snarfed = csv.reader(f, delimiter=',')
    for ix, row in enumerate(snarfed):
        if not valid_date(row[0]):
            print ("skipping row %s" %ix)
            continue
        d = {}
        dvalues = []
        for val in row:
            if regexp_date(val):
                k = val
                d[k] = dvalues
            else:
                dvalues.append(val)
        prep_data.append(d)

normalize(prep_data)




