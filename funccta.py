# funccta.py

# ------------------------------------------------------------
# Part 4: Thinking in functions
# ------------------------------------------------------------
import tracemalloc
tracemalloc.start()

import readrides
rows = readrides.read_as_instances('ctabus.csv')

# 1. How many bus routes exist?
#    Solution: Read into a set

routes = { row.route for row in rows }
print(len(routes), 'routes')

# 2. How many people rode route 22 on 9-Apr-2007?
#    Solution: Build an index mapping routes, dates to ride totals.
#    You'll use (route,date) as a composite key.

by_route_and_date = { (row.route, row.date): row.rides for row in rows }
print('Route 22 on 9-Apr-2007:', by_route_and_date['22','04/09/2007'])

# 3. Find out what day the route 22 bus had the highest ridership

rt22 = [(row.rides, row.date) for row in rows if row.route == '22']
print('Max ridership:', max(rt22))

print('Current %s, Peak %s' % tracemalloc.get_traced_memory())
