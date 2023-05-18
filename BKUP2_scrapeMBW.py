"""
Basic webscraping script that collects the following data from the https://melanchthon.hadw-bw.de/index.html database:

    - Regest number
    - Sender + location(s)
    - Recipient(s) + location(s)
    - Date
    
    To do:
    - check whether database entry also exists ending in -a (eg. 4, 4a)

"""

# import modules

from bs4 import BeautifulSoup
import requests, csv, lxml, time

# create csv
csv_file = open('mbw_output.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Regest-Nr', 'Empfänger', 'Empfänger-GND', 'Empfänger-location', 'location-url', 'Autor-location', 'Datum', 'source'])

#generate urls
start_index = 1
end_index = 20


urls = []
base_url = "https://melanchthon.hadw-bw.de/regest.html?reg_nr={}"

for i in range(start_index, end_index +1):
    url = base_url.format(i)
    urls.append(url)

for url in urls:
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
    csv_writer.writerow([text_val, recipient, recip_id, rec_loc, loc_id, reg_loc, url])
    csv_file.flush()

    time.sleep(3)

csv_file.close()


