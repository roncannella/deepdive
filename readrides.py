# readrides.py
#
# This program is starting point for a lot of code to follow.  It
# will be built-upon in the course.

import csv

def read_as_tuples(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            records.append((route, date, daytype, rides))

    return records

def read_as_dicts(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            records.append({
                    'route': route, 
                    'date': date, 
                    'daytype': daytype, 
                    'rides': rides})

    return records

class Row(object):
    # __slots__ = ('route', 'date', 'daytype', 'rides')
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

# Alternative to defining a class
if False:
    from collections import namedtuple
    Row = namedtuple('Row', ['route','date','daytype','rides'])

def read_as_instances(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            records.append(Row(route, date, daytype, rides))

    return records

# Alternate data layout (columns)
def read_as_columns(filename):
    route = []
    date = []
    daytype = []
    rides = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            route.append(row[0])
            date.append(row[1])
            daytype.append(row[2])
            rides.append(int(row[3]))
    return dict(route=route, date=date, daytype=daytype, rides=rides)

# Pandas. 
def read_as_dataframe(filename):
    import pandas
    data = pandas.read_csv(filename)
    # Discussion: Pandas allocates memory using a mix of internal
    # arrays and Python objects.  The internal arrays aren't tracked
    # by the internal Python memory allocator and aren't reported in
    # tracemalloc statistics.  The .info() method will report the
    # usage of the arrays themselves, but not the associated Python
    # objects.  For the the example shown here, info() will report
    # about 22MB of memory in use.  You'll need to add this to the
    # overall memory reported by tracemalloc.get_traced_memory() to
    # get a better picture of memory use.
    print(data.info())
    return data

if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    # Change this to one of the functions above
    data = read_as_tuples('ctabus.csv')
    print('Current %s, Peak %s' % tracemalloc.get_traced_memory())