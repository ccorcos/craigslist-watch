from secrets import *
import urllib
import json
import pydash
import chetEmail
import datetime

# Search For Houses / Apartments

SEND_EMAIL = False

emailTos = ['ccorcos@gmail.com', 'mqnavarr@gmail.com']

#############################################
################### SETUP ###################
#############################################

# base url for the craigslist catogory
base_url = 'http://losangeles.craigslist.org/search/apa?'

# fill out the filters on craigslist and set the url parameters here
filters = [
    ('hasPic', 1),
    ('maxAsk', 5500),
    ('bedrooms', 4),
    ('housing_type', 1),
    ('housing_type', 2),
    ('housing_type', 3),
    ('housing_type', 4),
    ('housing_type', 5),
    ('housing_type', 6),
    ('housing_type', 9),
]

# search queries to look through
queries = ['el segundo', 'redondo beach', 'hermosa beach', 'manhattan beach', 'santa monica beach', 'venice beach', 'marina del rey']

# make sure the locations include one of the following strings, all lowercase
locations = ['segundo', 'redondo', 'hermosa', 'manhattan', 'santa monica', 'venice', 'marina']

# number of pages to search through
numberOfPages = 1

# dollars per room
maxRate = 1100.0

#############################################
################### FETCH ###################
#############################################

api_key="6ry0OW6wJFglXoNKrDSaxOSbeni9i9hlvQ8AeTSwy3qmfzNd2w0LdzLWSBYt5RADq+OKUF840wRzj7/HWBLMJQ=="

pageInc = 100

apts = []
for query in queries:
    for page in range(numberOfPages):

        params = list(filters)
        params.append(('query',query))
        params.append(('s',page*pageInc))

        plainUrl = base_url + urllib.urlencode(params,'')
        url = urllib.quote(plainUrl)

        # Setup your REST GET request URL here
        getUrl = 'https://api.import.io/store/data/ae9b3481-fd34-4f31-88dc-ab2c18edde46/_query?input/webpage/url='+url+'&_user=43864eeb-fab1-4163-94ab-29ce26a543e5&_apikey='+urllib.quote(api_key,'')

        print 'FETCHING:'
        print ''
        print 'search:', query
        print ''
        print 'paging:', str(page*pageInc) + "-" + str((page+1)*pageInc)
        print ''
        print 'craigslist url:', plainUrl
        print ''
        print 'import.io API url:', getUrl
        print ''



        response = urllib.urlopen(getUrl).read()
        data = json.loads(response)

        if 'results' in data:
            results = data['results']
            print str(len(results)) + ' results'
            for result in results:
                # Gather the information you want from your API request
                if all(key in result for key in ['title/_text', 'title', 'price', 'bedrooms', 'location']):
                    title = result['title/_text']
                    url = result['title']
                    price = float(result['price'].replace(',','').replace('$',''))
                    bedrooms = float(result['bedrooms'].replace('br',''))
                    location = result['location'].lower()
                    apt = {'title':title, 'url':url, 'price':price, 'bedrooms':bedrooms, 'ratio':price/bedrooms, 'location':location}
                    apts.append(apt)
        else:
            print 'FAILURE'
            print data

        print ''
        print '-'*79
        print ''

def validLoaction(string):
    found = map(lambda loc: string.find(loc) != -1, locations)
    if 1 in found:
        return True
    else:
        return False

totalResults = len(apts)

# sort based on ratio
sortedApts = pydash.sort_by(apts, lambda x: x['ratio'])

# filter based on ratio
filteredApts = pydash.select(sortedApts, lambda x: x['ratio'] <= maxRate and x['ratio'] > 1)

# filter location strings
locationApts = pydash.select(filteredApts, lambda x: validLoaction(x['location']))

# only show the unique results!
uniqAps = pydash.uniq(locationApts)

# generate an email!
text = 'Found ' +str(len(uniqAps)) +' results from the following search queries:\n\n"' + '"\n"'.join(queries)
text = text + '"\n\nHere are the results with a price to bedroom ratio less than $' + str(maxRate) + '.\n\n\n'
for apt in uniqAps:
    text = text + '$' + str( apt['ratio'])  + ' = $' + str(apt['price']) + ' / '+ str(apt['bedrooms']) + 'br : '
    text = text + apt['title'].encode('utf-8') + '\n' + apt['url'].encode('utf-8') + '\n\n'

# print text

text = text + 'Happy Hacking ;)\n\nRobot'

print text

if SEND_EMAIL:
    today = datetime.date.today().strftime("%B %d, %Y")

    chetEmail.send(emailTos, 'Robot Craigslist Results '+today, text)
