from secrets import *
import urllib
import json
import pydash
import chetEmail
import datetime

# Search For Houses / Apartments

def main():

    SEND_EMAIL = True

    emailTos = ['ccorcos@gmail.com']

    # fill out the filters on craigslist and set the url parameters here
    apts = []
    apts = apts + fetch([('hasPic', 1),('postedToday', 1),('bedrooms', 1)], ['santa monica'], ['santa monica'], 3, 2000.0, numBedrooms=1)


    # generate an email!
    text = 'Found ' +str(len(apts)) +' craigslist results.'
    for apt in apts:
        text = text + '$' + str( apt['ratio'])  + ' = $' + str(apt['price']) + ' / '+ str(apt['bedrooms']) + 'br : '
        text = text + apt['title'].encode('utf-8') + '\n' + apt['url'].encode('utf-8') + '\n\n'
    text = text + 'Happy Hacking ;)\n\nRobot'
    print text

    if SEND_EMAIL:
        today = datetime.date.today().strftime("%B %d, %Y")
        chetEmail.send(emailTos, 'Robot Craigslist Results '+today, text)


#############################################
################### FETCH ###################
#############################################


def fetch(filters, queries, locations, numberOfPages, maxRate, numBedrooms=None, tries=5):
    # base url for the craigslist catogory
    base_url = 'http://losangeles.craigslist.org/search/apa?'

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

            noResponse = True
            t = 0
            response = ''
            data = {}
            while ('results' not in data) and (t < tries):
                response = urllib.urlopen(getUrl).read()
                data = json.loads(response)
                t = t+1

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

    if numBedrooms:
        apts = pydash.select(apts, lambda x: x['bedrooms'] == 1.)

    # sort based on ratio
    sortedApts = pydash.sort_by(apts, lambda x: x['ratio'])

    # filter based on ratio
    filteredApts = pydash.select(sortedApts, lambda x: x['ratio'] <= maxRate and x['ratio'] > 1)

    # filter location strings
    locationApts = pydash.select(filteredApts, lambda x: validLoaction(x['location']))

    # only show the unique results!
    uniqApts = pydash.uniq(locationApts)

    return uniqApts

if __name__ == "__main__":
    main()
