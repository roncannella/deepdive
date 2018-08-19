Python 3.6.4 |Anaconda, Inc.| (default, Jan 16 2018, 10:22:32) [MSC v.1900 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> file = open('portfolio.csv")
		
SyntaxError: EOL while scanning string literal
>>> 
		
>>> file = open("portfolio.csv")
		
>>> file
		
<_io.TextIOWrapper name='portfolio.csv' mode='r' encoding='cp1252'>
>>> import csv
		
>>> file
		
<_io.TextIOWrapper name='portfolio.csv' mode='r' encoding='cp1252'>
>>>  next(file)
		
SyntaxError: unexpected indent
>>> next(file)
		
'name,shares,price\n'
>>> rows = list(csv.reader(file))
		
>>> rows
		
[['AA', '100', '32.20'], ['IBM', '50', '91.10'], ['CAT', '150', '83.44'], ['MSFT', '200', '51.23'], ['GE', '95', '40.37'], ['MSFT', '50', '65.10'], ['IBM', '100', '70.44']]
>>> pprint(rows)
		
Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    pprint(rows)
NameError: name 'pprint' is not defined
>>> from pprint import pprint
		
>>> pprint(rows)
		
[['AA', '100', '32.20'],
 ['IBM', '50', '91.10'],
 ['CAT', '150', '83.44'],
 ['MSFT', '200', '51.23'],
 ['GE', '95', '40.37'],
 ['MSFT', '50', '65.10'],
 ['IBM', '100', '70.44']]
>>> 
		
>>> # 1 to many
		
>>> from collections import defaultdict
		
>>> d = defaultdict(list)
		
>>> d
		
defaultdict(<class 'list'>, {})
>>> d['x']
		
[]
>>> d
		
defaultdict(<class 'list'>, {'x': []})
>>> d['y']
		
[]
>>> from collections import defaultdict
KeyboardInterrupt
>>> 
		
>>> 
		
>>> 
		
>>> 
		
>>> 
		
>>> 
		
>>> 
		
>>> 
		
>>> d
		
defaultdict(<class 'list'>, {'x': [], 'y': []})
>>> d[x]
		
Traceback (most recent call last):
  File "<pyshell#30>", line 1, in <module>
    d[x]
NameError: name 'x' is not defined
>>> d:x
		
Traceback (most recent call last):
  File "<pyshell#31>", line 1, in <module>
    d:x
NameError: name 'x' is not defined
>>> 
		
>>> d.x
		
Traceback (most recent call last):
  File "<pyshell#33>", line 1, in <module>
    d.x
AttributeError: 'collections.defaultdict' object has no attribute 'x'
>>> byname = defaultdict(list)
		
>>> for row in rows:
		byname[row[0]].append(row)

		
>>> pprint(byname)
		
defaultdict(<class 'list'>,
            {'AA': [['AA', '100', '32.20']],
             'CAT': [['CAT', '150', '83.44']],
             'GE': [['GE', '95', '40.37']],
             'IBM': [['IBM', '50', '91.10'], ['IBM', '100', '70.44']],
             'MSFT': [['MSFT', '200', '51.23'], ['MSFT', '50', '65.10']]})
>>> byname['IBM']
		
[['IBM', '50', '91.10'], ['IBM', '100', '70.44']]
>>> from collections import Counter
		
>>> c = Counter()
		
>>> c['x'] += 10
		
>>> c
		
Counter({'x': 10})
>>> c['y'] += 223
		
>>> c
		
Counter({'y': 223, 'x': 10})
>>> c[x] += 10
		
Traceback (most recent call last):
  File "<pyshell#46>", line 1, in <module>
    c[x] += 10
NameError: name 'x' is not defined
>>> c['x'] += 223
		
>>> c
		
Counter({'x': 233, 'y': 223})
>>> c
		
Counter({'x': 233, 'y': 223})
>>> routes = {}
		
>>> routes = set()
		
>>> 
