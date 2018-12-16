from pprint import PrettyPrinter
pp = PrettyPrinter(width=1, indent=1)
print = pp.pprint

# 1. Generating dataset from file----------------------------------------- 
'''
Expected dataset example:
{
    'Jane': { 
        '10.11.2018': { 
            'apple': {
                'quantity':1,
                'price': 4.5
            } #, ...
        } #,...
    } #,...
}
'''
# Method 1. Column-wise read
'''
Temorary dataset example: {'Jane': [['10.11.2018', 'apple', '1', '4.5']] }
'''
def convert_2_dict(lst):
    '''
    Args:
        lst (list): list of lists for a curent column sub-dictionary
    '''
    if len(lst[0]) == 2:
        return {
            'quantity': lst[0][0],
            'price': lst[0][1]
        }
    dct = {}
    for sublst in lst:
        key = sublst[0]
        if key not in dct:
            dct[key] = []
        dct[key].append(sublst[1:])
    for key in dct:
        dct[key] = convert_2_dict(dct[key])
    return dct

with open('orders.csv', encoding='utf-8') as f:
    f.readline()
    file = [[el.strip() for el in line.split(',')] for line in f]
    result = convert_2_dict(file)

print(result)

"""
# Method 2. Row-wise read
def add_to_dict(dct, lst):
    '''
    Args:
        dct (dict): (sub)dictionary that is currently updated
        lst (list): list of items in a currently processed row
    '''
    if len(lst) == 3:
        dct[lst[0]] = {
            'quantity': lst[1],
            'price': lst[2]
        }
        return dct
    key = lst[0]
    if key not in dct:
        dct[key] = {}
    add_to_dict(dct[key], lst[1:])
    return dct

def convert_str(s):
    return list(map(str.strip, s.split(',')))

from functools import reduce

with open('orders.csv', encoding='utf-8') as f:
    f.readline()
    result = reduce(add_to_dict, map(convert_str, f), {})

print(result)
"""

# 2. Extracting data from dataset--------------------------------------
# Method 1. Iterate over data slice
res = set()

for val in result.values():
    for val2 in val.values():
        res = res.union(set(val2.keys()))
for name in result:
    client_products = set()
    for date in result[name]:
        client_products = client_products.union(set(result[name][date].keys()))
    res = res.intersection(client_products)

print(res)

"""
# Method 2. Use map-reduce
def convert_values(dct):
    def extract_keys(value):
        return set(value.keys())
    return reduce(set.union, map(extract_keys, dct.values()))

res = reduce(set.intersection, map(convert_values, result.values()))
print(res)
"""

# 3. Extracting and plotting data series---------------------------- 
apples = {}

for _, dates in result.items():
    for date, products in dates.items():
        for prod, chars in products.items():
            if prod == 'apple':
                apples[date] = chars['price']
# this can also be written as
# apples = { 
#    date: chars['price'] 
#    for _, dates in result.items()
#    for date, products in dates.items()
#    for prod, chars in products.items()
#    if prod == 'apple'
# }
# or even as
# def collect_apples(date_price, date_prods):
#     def have_apples(date_prod_item):
#         return 'apple' in date_prod_item[1].keys()
#     def get_date_price_pair(date_prod_item):
#         return (date_prod_item[0], date_prod_item[1]['apple']['price'])
#     date_price.update(map(get_date_price_pair, filter(have_apples, date_prods.items())))
#     return date_price
# apples = reduce(collect_apples, result.values(), {})

print(apples)

import plotly.offline as pl
import plotly.graph_objs as go

xs = sorted(list(apples.keys()))
ys = [apples[key] for key in xs]

pl.plot([go.Scatter(x=xs,y=ys)])
# same as
#
# pl.plot({
#    'data': [go.Scatter(x=xs,y=ys)]
# })
#
# or even
#
# series1 = go.Scatter(x=xs,y=ys)
# options = {
#    'data': [series1]
# }
# pl.plot(options)

#-----------------4---------------------------------------
price={}
for name, dates in result.items():
	price[name]=[]
	for data, prods in dates.items():
		for char in prods.values():
			pr=float(char['quantity'])*float(char['price'])
			price[name].append(pr)
	price[name]=sum(price[name])
			

xs=[name for name in price]
ys=[price[name] for name in price] 
pl.plot([go.Bar(x=xs,y=ys)])			

#------------------5--------------------------------------------
a=0
l=0
c=0
g=0
dict={}
for dates in result.values():
	for date in dates.values():	
		for prod in date:
			if prod=='apple':
				a+=1
			elif prod=='lemon':
				l+=1
			elif prod=='cake':
				c+=1
			elif prod=='grape':
				g+=1
dict[a]='apple'
dict[l]='lemon'
dict[c]='cake'
dict[g]='grape'
mx=max(a,l,c,g)
print(dict[mx])
	
#-------------------------6----------------------------------
product_popularity = {}
for client in result:
		for date in result[client]:
			for product in result[client][date]:
				if product not in product_popularity:
					product_popularity[product] = 0
				product_popularity[product] = float(result[client][date][product]['quantity'])
products = list(product_popularity.keys())
quantities = list(product_popularity.values())
min_quantities = min(quantities)
mn = quantities.index(min_quantities)
print(products[mn])

#-----------------------7------------------------------------
product_popularity = {}
for client in result:
		for date in result[client]:
			for product in result[client][date]:
				if product not in product_popularity:
					product_popularity[product] = 0
				product_popularity[product]= float(result[client][date][product]['price'])
products = list(product_popularity.keys())
quantities = list(product_popularity.values())
max_quantities = max(quantities)
mx = quantities.index(max_quantities)
print(products[mx])
#---------------------------8-----------------------------------------
product_user = dict()
for client in result:
	for date in result[client]:
		for product in result[client][date]:
			if product not in product_user:
				product_user[product] = 0
			product_user[product]+=1
xs=list(product_user.keys())
ys=list(product_user.values())

pl.plot([go.Bar(x=xs, y=ys)])




