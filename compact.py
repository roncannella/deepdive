# compact.py

import csv


# ------------------------------------------------------------
# Part 3 - A Clever hack to save a lot of memory
# ------------------------------------------------------------

class Row(object):
    __slots__ = ('route', 'date', 'daytype', 'rides')
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

def read_as_instances(filename):
    records = []
    cache = {}
    
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        
        for row in rows:
            # Observation: Route numbers and dates are highly repetitive
            # in the data.   Perhaps they can be cached and previous objects reused
            route = cache.setdefault(row[0], row[0])
            date = cache.setdefault(row[1], row[1])
            daytype = row[2]
            rides = int(row[3])

            records.append(Row(route, date, daytype, rides))

    return records

if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    rows = read_as_instances('ctabus.csv')
    print('Current %s, Peak %s' % tracemalloc.get_traced_memory())
