# deepdive.py
#
# Code examples from "Python Data Handling: A Deeper Dive"
# David Beazley (@dabeaz)
# Presented: April 20, 2018

# A function to read a CSV file into a list of records
import csv
def read_data(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            record = make_record(row)
            records.append(record)
    return records

# You have different choices when it comes to representing the
# records.  Let's review the options.

# Do nothing
def make_record(row):
    return row

#:Memory: 194744739
#

# Tuples (doing nothing else)
def make_record(row):
    return (row[0], row[1], row[2], row[3])

#:Memory: 182961163
#
# Notice: Using tuples are more efficiently than lists

# Tuples (with conversion)
def make_record(row):
    return (row[0], row[1], row[2], int(row[3]))

#:Memory: 163672400

# Dicts 
def make_record(row):
    return {
        'route': row[0],
        'date': row[1],
        'daytype': row[2],
        'rides': int(row[3])
        }

#:Memory: 281503720

# Instances
class Row(object):
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

def make_record(row):
    return Row(row[0], row[1], row[2], int(row[3]))

#:Memory: 228480816
# Note: Using an instance is better than a dictionary

# Instances with slots
class Row(object):
    __slots__ = ('route', 'date', 'daytype', 'rides')
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

    def __repr__(self):
        return f'Row({self.route}, {self.date}, {self.daytype}, {self.rides})'

#:Memory: 157782072
# 
# An instance with slots is the best of all (even better than a tuple)

# Namedtuples
from collections import namedtuple
Row = namedtuple('Row', ['route', 'date', 'daytype', 'rides'])

#:Memory: 169565440
# Note: Slighly worse than a tuple

# Clever "hack" to save memory.   There is a lot of repeated and 
# redundant data.  For example, there are only 185 unique route names
# and only a few thousand dates.  You can use a lot less memory if you
# do a bit of string caching.  For example:
#
cache = { }

def cached_string(s):
    if s in cache:
        return cache[s]
    else:
        cache[s] = s
        return s

def make_record(row):
    return Row(cached_string(row[0]), cached_string(row[1]), row[2], int(row[3]))

# Recall : 157MB before (slots)
#:Memory: 79494150
# That's a pretty big drop!

# This bit of code reads the data and reports the memory statistics
import tracemalloc
tracemalloc.start()
rows = read_data('ctabus.csv')
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print("Memory:", current)


# Calculations involving the data.  These assume an instance representation
#:>>> len(rows)
#:736461
#:>>> # 1. Find out how many bus routes exist
#:>>> unique_routes = set()
#:>>> for row in rows:
#:...     unique_routes.add(row.route)
#:... 
#:>>> len(unique_routes)
#:185
#:>>> # 2. How many rides on route 22 on April 9, 2007
#:>>> # DON'T DO THIS
#:>>> for row in rows:
#:...     if row.route == '22' and row.date == '04/09/2007':
#:...         break
#:... 
#:>>> row
#:Row(22, 04/09/2007, W, 24154)
#:>>> # BETTER: Build a (route,date)->row index
#:>>> route_date = { }
#:>>> for row in rows:
#:...     route_date[row.route, row.date] = row
#:... 
#:>>> route_date['22', '04/09/2007']
#:Row(22, 04/09/2007, W, 24154)
#:>>> route_date['6', '05/04/2011']
#:Row(6, 05/04/2011, W, 11675)
#:>>> # 3. What are ten most popular routes?
#:>>> from collections import Counter
#:>>> popular = Counter()
#:>>> for row in rows:
#:...     popular[row.route] += row.rides
#:... 
#:>>> popular['22']
#:111886681
#:>>> popular['6']
#:65624844
#:>>> popular.most_common(10)
#:[('79', 165309712),
#: ('9', 147507182),
#: ('49', 121673788),
#: ('66', 120662106),
#: ('4', 120176371),
#: ('77', 114243228),
#: ('22', 111886681),
#: ('3', 111559864),
#: ('151', 110893971),
#: ('53', 109925583)]
#:>>> # 4. What are ten most popular routes in 2016?
#:>>> by_year = {
#:...     '2001': Counter(),
#:...     '2002': Counter(),
#:...     '2003': Counter(),
#:...     }
#:... 
#:>>> by_year['2001']['22'] += 123
#:>>> by_year['2002']['6'] += 445
#:>>> by_year
#:{
#:  '2001': Counter({'22': 123})
#:  '2002': Counter({'6': 445})
#:  '2003': Counter()
#:}
#:>>> from collections import defaultdict
#:>>> by_year = defaultdict(Counter)
#:>>> by_year
#:defaultdict(<class 'collections.Counter'>, {})
#:>>> by_year['2012']['22'] += 123
#:>>> by_year
#:{
#:  '2012': Counter({'22': 123})
#:}
#:>>> for row in rows:
#:...     year = row.date[-4:]   # last 4 digits
#:...     by_year[year][row.route] += row.rides
#:... 
#:>>> by_year['2016']['22']
#:5620134
#:>>> by_year['2011']['22']
#:7392947
#:>>> # 5. What 10 routes had the greatest increase in ridership 2001-2016?
#:>>> diff = by_year['2016'] - by_year['2001']
#:>>> diff.most_common(10)
#:[('J14', 3296029),
#: ('15', 2301408),
#: ('X9', 2075111),
#: ('146', 1516226),
#: ('147', 1315199),
#: ('115', 1114940),
#: ('12', 1001598),
#: ('26', 920307),
#: ('134', 722110),
#: ('18', 684923)]
#:>>> 

# Simplified calculations involving list/set/dict comprehensions
#:>>> # Get all route 22 data
#:>>> rt22 = [row for row in rows if row.route == '22']
#:>>> rt22[0:4]
#:[Row(22, 01/01/2001, U, 7877),
#: Row(22, 01/02/2001, W, 19558),
#: Row(22, 01/03/2001, W, 19286),
#: Row(22, 01/04/2001, W, 20265)]
#:>>> [ row for row in rt22 if row.rides < 5000]
#:[Row(22, 12/25/2001, U, 4327),
#: Row(22, 12/25/2002, U, 4392),
#: Row(22, 12/25/2003, U, 4420),
#: Row(22, 12/25/2004, U, 3799),
#: Row(22, 12/25/2007, U, 4925),
#: Row(22, 12/25/2008, U, 4560),
#: Row(22, 12/25/2010, U, 4910),
#: Row(22, 12/25/2012, U, 4901),
#: Row(22, 12/25/2013, U, 4611),
#: Row(22, 12/25/2014, U, 4871),
#: Row(22, 12/25/2015, U, 4358),
#: Row(22, 12/25/2016, U, 3893)]
#:>>> rides_date = [ (row.rides, row.date) for row in rt22 ]
#:>>> rides_date[:4]
#:[(7877, '01/01/2001'),
#: (19558, '01/02/2001'),
#: (19286, '01/03/2001'),
#: (20265, '01/04/2001')]
#:>>> max(rides_date)
#:(26896, '06/11/2008')
#:>>> min(rides_date)
#:(3799, '12/25/2004')
#:>>> unique_routes = { row.route for row in rows }    # Note: { }
#:>>> len(unique_routes)
#:185
#:>>> route_date = { (row.route, row.date): row for row in rows }
#:>>> route_date['22', '04/09/2007']
#:Row(22, 04/09/2007, W, 24154)
#:>>> 


# A version of the read_data() function that reads the data into columns.
# Each column stored as a numpy array.  This is very similar to Pandas
# DataFrame.

import numpy

def read_data_as_columns(filename):
    routes = []
    dates = []
    daytypes = []
    rides = [] 

    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            rides.append(int(row[3]))

    return {
        'route': numpy.array(routes),
        'date': numpy.array(dates),
        'daytype': numpy.array(daytypes),
        'rides': numpy.array(rides)
        }


import tracemalloc
tracemalloc.start()
data = read_data_as_columns('ctabus.csv')
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print("Memory:", current)


# An example of processing the CTA-data in a stream-oriented fashion

#:>>> import tracemalloc
#:>>> tracemalloc.start()
#:>>> f = open('ctabus.csv')
#:>>> f
#:<_io.TextIOWrapper name='ctabus.csv' mode='r' encoding='UTF-8'>
#:>>> import csv
#:>>> rows = csv.reader(f)
#:>>> rows
#:<_csv.reader object at 0x7f55adfbd9e8>
#:>>> next(rows)
#:['route', 'date', 'daytype', 'rides']
#:>>> next(rows)
#:['3', '01/01/2001', 'U', '7354']
#:>>> def make_records(rows):
#:...     for row in rows:
#:...         yield { 'route': row[0], 'date': row[1], 'daytype': row[2], 'rides': int(row[3]) }
#:... 
#:>>> records = make_records(rows)
#:>>> records
#:<generator object make_records at 0x7f55ad1697d8>
#:>>> next(records)
#:{
#:  'route': '4'
#:  'date': '01/01/2001'
#:  'daytype': 'U'
#:  'rides': 9288
#:}
#:>>> next(records)
#:{
#:  'route': '6'
#:  'date': '01/01/2001'
#:  'daytype': 'U'
#:  'rides': 6048
#:}
#:>>> rt22 = (r for r in records if r['route'] == '22')   # Generator expression
#:>>> rt22
#:<generator object <genexpr> at 0x7f55adf50518>
#:>>> next(rt22)
#:{
#:  'route': '22'
#:  'date': '01/01/2001'
#:  'daytype': 'U'
#:  'rides': 7877
#:}
#:>>> next(rt22)
#:{
#:  'route': '22'
#:  'date': '01/02/2001'
#:  'daytype': 'W'
#:  'rides': 19558
#:}
#:>>> rides_date = ( (r['rides'], r['date']) for r in rt22 )
#:>>> rides_date
#:<generator object <genexpr> at 0x7f55adf503b8>
#:>>> next(rides_date)
#:(19286, '01/03/2001')
#:>>> next(rides_date)
#:(20265, '01/04/2001')
#:>>> max(rides_date)
#:(26896, '06/11/2008')
#:>>> tracemalloc.get_traced_memory()
#:(41332, 101503)
#:>>> min(rides_date)
#:ValueError: min() arg is an empty sequence
