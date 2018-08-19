# readcolumns.py

# ------------------------------------------------------------
# Part 5 - Thinking in Columns
# ------------------------------------------------------------

import csv
def read_as_columns(filename):
    routes = []
    dates = []
    daytypes = []
    rides = []

    # Cache of duplicate values (see compact.py)

    cache = { }
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            route = cache.setdefault(row[0], row[0])
            date = cache.setdefault(row[1], row[1])
            daytype = row[2]
            numrides = int(row[3])

            routes.append(route)
            dates.append(date)
            daytypes.append(daytype)
            rides.append(numrides)

    return (routes, dates, daytypes, rides)

if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    columns = read_as_columns('ctabus.csv')
    print('Current %s, Peak %s' % tracemalloc.get_traced_memory())

    # Can you work with the data?
    # The zip function offers some interesting options.

    rt22 = [ (rides, date) for route, date, _, rides in zip(*columns) 
             if route == '22']

    print('Max route 22 rides:', max(rt22))
