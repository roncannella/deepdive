# stream.py

# ------------------------------------------------------------
# Part 6: Thinking in streams
# ------------------------------------------------------------

import csv
import os
import tracemalloc
tracemalloc.start()

with open('ctabus.csv') as f:
    rows = csv.reader(f)
    headers = next(rows)
    rides = (dict(zip(headers, row)) for row in rows)
    rt22 = ((int(row['rides']), row['date']) for row in rides if row['route'] == '22')
    print(max(rt22))

print('Current %s, Peak %s' % tracemalloc.get_traced_memory())

    
