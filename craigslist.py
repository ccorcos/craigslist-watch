from secrets import *
import urllib
import json
import pydash
import chetEmail
import datetime

# Search For Houses / Apartments

emailTos = ['ccorcos@gmail.com', 'mqnavarr@gmail.com']

#############################################
################### SETUP ###################
#############################################

# base url for the craigslist catogory
base_url = 'http://losangeles.craigslist.org/search/apa?'

# fill out the filters on craigslist and set the url parameters here
filters = {
    'hasPic': 1,
    'maxAsk': 5500,
    'bedrooms': 4,
    'housing_type': 1,
    'housing_type': 2,
    'housing_type': 3,
    'housing_type': 4,
    'housing_type': 5,
    'housing_type': 6,
    'housing_type': 9
}

# search queries to look through
queries = ['el segundo', 'redondo beach', 'hermosa beach', 'manhattan beach', 'santa monica beach', 'venice beach', 'marina del rey']

# number of pages to search through
numberOfPages = 1

# dollars per room
maxRate = 1100.0

# Setup the rest of your API below

#############################################
################### FETCH ###################
#############################################

pageInc = 100

apts = []
for query in queries:
    for page in range(numberOfPages):
        print 'FETCHING:', query, str(page*pageInc) + "-" + str((page+1)*pageInc)

        params = filters.copy()
        params['query'] = query
        params['s'] = page*pageInc

        url = urllib.quote(base_url + urllib.urlencode(params,''))

        # Setup your REST GET request URL here
        getUrl = 'https://api.import.io/store/data/ae9b3481-fd34-4f31-88dc-ab2c18edde46/_query?input/webpage/url='+url+'&_user=43864eeb-fab1-4163-94ab-29ce26a543e5&_apikey='+urllib.quote(api_key,'')

        response = urllib.urlopen(getUrl).read()
        data = json.loads(response)

        if 'results' in data:
            results = data['results']
            for result in results:
                # Gather the information you want from your API request
                if all(key in result for key in ['title/_text', 'title', 'price', 'bedrooms']):
                    title = result['title/_text']
                    url = result['title']
                    price = float(result['price'].replace(',','').replace('$',''))
                    bedrooms = float(result['bedrooms'].replace('br',''))
                    apt = {'title':title, 'url':url, 'price':price, 'bedrooms':bedrooms, 'ratio':price/bedrooms}
                    apts.append(apt)
        else:
            print ''
            print 'FAILURE: ' + getUrl
            print ''


print ''
print 'RESULTS:'
print ''

# sort based on ratio
sortedApts = pydash.sort_by(apts, lambda x: x['ratio'])

# filter based on ratio
filteredApts = pydash.select(sortedApts, lambda x: x['ratio'] <= maxRate and x['ratio'] > 1)

# only show the unique results!
uniqAps = pydash.uniq(filteredApts)

# generate an email!
text = 'gathered ' +str(numberOfPages*pageInc) +' results for each of the following queries:\n\n"' + '"\n"'.join(queries)
text = text + '"\n\n Here are the results with a price to bedroom ratio less than $' + str(maxRate) + '.\n\n\n'
for apt in uniqAps:
    text = text + '$' + str( apt['ratio'])  + ' / ' + str(apt['bedrooms']) + 'br - $' + str(apt['price']) + ' total : '
    text = text + apt['title'].encode('utf-8') + '\n' + apt['url'].encode('utf-8') + '\n\n'
    print text

text = text + 'Happy Hacking ;)\n\nRobot'

today = datetime.date.today().strftime("%B %d, %Y")

chetEmail.send(emailTos, 'Robot Craigslist Results '+today, text)
