import pandas as pd
import requests
from lxml import etree

XML_FILE = "1234.xml"
HTTP_STATUS_CODES = "http-status-codes-1.csv"

def get_url_status(urls, status_codes):  # checks status for each url in list urls

    df = pd.DataFrame(columns=["URL", "Status"])

    for url in urls:
        try:
            r = requests.get(url)
            print(url + "\tStatus: " + str(r.status_code))
            data = [[url, str(r.status_code), str(status_codes.loc[status_codes["Status"] == str(r.status_code), "Description"].iloc[0])]]
            df = pd.concat([df, pd.DataFrame(data, columns=["URL", "Status", "Description"])], ignore_index=True)
        except Exception as e:
            print(url + "\tNA FAILED TO CONNECT\t" + str(e))

    return df

def main():

    # Load and parse XML file
    tree = etree.parse(XML_FILE)
    
    # Initialize list of urls
    urls = []
    
    # Get hyperlinks via xpath
    for url in tree.xpath("//ext-link/@xlink:href", namespaces={
            "xlink": 'http://www.w3.org/1999/xlink'
        }):
        if not url in urls:
            urls.append(url)
    
    # Import http status codes from csv file
    status_codes = pd.read_csv(HTTP_STATUS_CODES, names=["Status", "Description", "RFC"], header=None, index_col=False)

    # Check urls
    df = get_url_status(urls, status_codes)

    # Report console output
    print(str(len(df.index)) + " URLs gefunden")
    
    for status in df["Status"].unique():
        print("Status " + str(status) 
            + " [" + status_codes.loc[status_codes['Status'] == status, 'Description'].iloc[0] + "]: " 
            + str(df['Status'].value_counts()[status]) + " von " + str(len(df.index)) + " URLs")

    # Write result to csv file
    df.to_csv(XML_FILE + ".csv", sep='\t', encoding='utf-8')

if __name__ == "__main__":
    main()