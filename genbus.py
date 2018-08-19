# genbus.py

# Another stream example

import csv

class Row(object):
    __slots__ = ('route', 'date', 'daytype', 'rides')
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

def read_rides_as_instances(filename):
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)   # Skip (not data)
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Row(route, date, daytype, rides)  #instance
            yield record

rows = read_rides_as_instances('ctabus.csv')

def find_route(rows, route):
    for row in rows:
        if row.route == route:
            yield row

def date_rides(rows):
    for row in rows:
        yield (row.rides, row.date)

# Example of a pipeline
import tracemalloc
tracemalloc.start()

rows = read_rides_as_instances('ctabus.csv')
rt22 = find_route(rows, '22')
data = date_rides(rt22)
print(max(data))

print('Current %s, Peak %s' % tracemalloc.get_traced_memory())
