"""
Basic webscraping script that collects the following data from https://melanchthon.hadw-bw.de/index.html:

    Regest number
    Sender + location(s)
    Recipient(s) + location(s)
    Date


"""

# import modules

from bs4 import BeautifulSoup
import requests, csv, lxml, time

# create csv
csv_file = open('mbw_output.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Regest-Nr', 'Empfänger', 'Empfänger-GND', 'Empfänger-location', 'location-url', 'Autor-location', 'Datum', 'source'])

#generate urls
def generate_urls(start_index, end_index):
    urls = []
    base_url = "https://melanchthon.hadw-bw.de/regest.html?reg_nr={}"
    for i in range(start_index, end_index +1):
        url = base_url.format(i)
        urls.append(url)
    return urls

def mbw_scrape(url):
    # define source
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    if source:
        # scrape regest id
        reg_id = soup.select_one('div#nav_regesten span[style="font-size:2rem;"]')
        text_val = reg_id.text.strip() if reg_id else None
        print(text_val)

        # scrape recipient name and location
        names = soup.find('sense')
        recipient = recip_id = rec_loc = loc_id = None
        if names:
            name_els = names.find_all('name')
            if len(name_els) > 1:
                # name
                recipient = name_els[1].text
                recip_id = name_els[1].get('ref')

                # location
                rec_loc = name_els[2].text
                loc_id = name_els[2].get('ref')

        # scrape sender location and date
        headline = soup.find_all('h2')
        reg_loc = reg_date = None
        if len(headline) > 1:
            spans = headline[1].find_all('span')
            if spans:
                geoloc = spans[-1].text
                reg_loc, reg_date = geoloc.split(',', 1)

     # write csv output
    csv_writer.writerow([text_val, recipient, recip_id, rec_loc, loc_id, reg_loc, reg_date])
    csv_file.flush()

urls = generate_urls(1, 2)

for url in urls:
    mbw_scrape(url)
    time.sleep(3)

csv_file.close()


""" # create csv

csv_file = open('mbw_output.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Regest-Nr', 'Empfänger', 'Empfänger-GND', 'Empfänger-location', 'location-url', 'Autor-location', 'Datum', 'source'])

# define source

source = requests.get('https://melanchthon.hadw-bw.de/regest.html?reg_nr=2').text
soup = BeautifulSoup(source, 'lxml')

if source:

    # scrape regest id

    reg_id = soup.select_one('div#nav_regesten span[style="font-size:2rem;"]')
    if reg_id:
        text_val = reg_id.text
        text_val.strip()
    print(text_val)

    # scrape recipient name and location

    names = soup.find('sense')
    if names:
        name_els = names.find_all('name')
        if len(name_els) > 1:

            # name
            recipient = name_els[1].text
            recip_id = name_els[1]['ref']

            # location
            rec_loc = name_els[2].text[:-1]
            loc_id = name_els[2]['ref']

    print(recipient + " " + recip_id)
    print(rec_loc + " " + loc_id)


    # scrape sender location and date

    headline = soup.find_all('h2')
    if len(headline) > 1:
        spans = headline[1].find_all('span')
        if spans:
            geoloc = spans[-1].text
            reg_loc, reg_date = geoloc.split(',', 1)
            print(reg_loc.strip())
            print(reg_date.strip())


    # write csv output

    csv_writer.writerow([text_val, recipient, recip_id, rec_loc, loc_id, reg_loc, reg_date])

csv_file.close() """

# create csv
""" with open('mbw_output.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Regest-Nr', 'Empfänger', 'Empfänger-GND', 'Empfänger-location', 'location-url', 'Autor-location', 'Datum', 'source'])

    # define source
    source = requests.get('https://melanchthon.hadw-bw.de/regest.html?reg_nr=1234').text
    soup = BeautifulSoup(source, 'lxml')

    if source:
        # scrape regest id
        reg_id = soup.select_one('div#nav_regesten span[style="font-size:2rem;"]')
        text_val = reg_id.text.strip() if reg_id else None
        print(text_val)

        # scrape recipient name and location
        names = soup.find('sense')
        recipient = recip_id = rec_loc = loc_id = None
        if names:
            name_els = names.find_all('name')
            if len(name_els) > 1:
                # name
                recipient = name_els[1].text
                recip_id = name_els[1].get('ref')

                # location
                rec_loc = name_els[2].text[:-1]
                loc_id = name_els[2].get('ref')

        print(recipient, recip_id)
        print(rec_loc, loc_id)

        # scrape sender location and date
        headline = soup.find_all('h2')
        reg_loc = reg_date = None
        if len(headline) > 1:
            spans = headline[1].find_all('span')
            if spans:
                geoloc = spans[-1].text
                reg_loc, reg_date = geoloc.split(',', 1)
                print(reg_loc.strip())
                print(reg_date.strip())

        # write csv output
        csv_writer.writerow([text_val, recipient, recip_id, rec_loc, loc_id, reg_loc, reg_date, ])

 """