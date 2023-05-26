# import modules

from bs4 import BeautifulSoup
import requests, csv, lxml, time

reg_start = 1
reg_end =  4

# generate urls function
def generate_urls(start_index, end_index):
	# initialize urls
	urls = []
	base_url = "https://melanchthon.hadw-bw.de/regest.html?reg_nr={}"
	
	# generate urls
	for i in range(start_index, end_index + 1):
		url = base_url.format(i)
		url_a = base_url.format(i) + "a"
		urls.append(url)
		urls.append(url_a)
	return urls

# verify target availability
def verify_urls(url_list):
	# initialize available urls
	av_urls = []

	# get results
	with requests.Session() as session:
		for i in url_list:
			source = requests.get(i).text
			soup = BeautifulSoup(source, 'lxml')
			if not soup.find('name'):
				print("Skipping MBW " + i[-2:] + "...")
			else:
				print("Found database entry for " + soup.select_one('div#nav_regesten span[style="font-size:2rem;"]').text.rstrip("\n") + "...")
				av_urls.append(i)
	return av_urls

# main function
def main():
	data = generate_urls(reg_start, reg_end)
	av_data = verify_urls(data)

	# create csv
	csv_file = open('mbw_output.csv', 'w', newline='')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Regest-Nr', 'Empfänger', 'Empfänger-GND', 'Empfänger-location', 'location-url', 'Autor-location', 'Datum', 'source'])

	for url in av_data:
		# get url
		source = requests.get(url).text
		soup = BeautifulSoup(source, 'lxml')

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

if __name__ == "__main__":
	main()