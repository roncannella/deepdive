# cta.py
#
# Example code from "Python Data Handling: A Deeper Dive"
# David Beazley (http://www.dabeaz.com)
# Copyright (C) 2017


import readrides
rows = readrides.read_as_instances('ctabus.csv')

# ------------------------------------------------------------
# Part 2 - Collections
# ------------------------------------------------------------

# 1. How many bus routes exist?
#    Solution: Read into a set

routes = set()
for row in rows:
    routes.add(row.route)

print(len(routes), 'routes')

# 2. How many people rode route 22 on 9-Apr-2007?
#    Solution: Build an index mapping routes, dates to ride totals.
#    You'll use (route,date) as a composite key.

by_route_and_date = {}
for row in rows:
    by_route_and_date[row.route, row.date] = row.rides

print('Route 22 on 9-Apr-2007:', by_route_and_date['22','04/09/2007'])

# 3. What the 10 most popular routes?
#    Solution: Put ride totals into a Counter and rank them.

from collections import Counter
route_totals = Counter()
for row in rows:
    route_totals[row.route] += row.rides

print('Most popular routes (all time)')
for routeno, count in route_totals.most_common(10):
    print(routeno, count)

# 4. What are the 10 most popular routes in 2016?
#    Solution: Group the data by year and build a Counter for each year

from collections import Counter, defaultdict

by_year = defaultdict(Counter)
for row in rows:
    year = row.date[-4:]
    by_year[year][row.route] += row.rides

print('Most popular routes in 2016')
for routeno, count in by_year['2016'].most_common(10):
    print(routeno, count)

# 5. What 10 routes had the greatest increase in ridership from 2001 - 2016?
#    Solution.  Compute the difference between counters

diff = by_year['2016'] - by_year['2001']

print('Greatest increase 2001 - 2016')
for routeno, delta in diff.most_common(10):
    print(routeno, delta)
