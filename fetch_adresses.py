#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import bs4
import csv
import json
import requests

def combine_with_geo_data(address_data, geo_filename):
    webaddress = address_data

    with open(geo_filename, "r") as f:
        spamreader = csv.DictReader(f, delimiter=",", quotechar="\"")
        for row in spamreader:
            if row['Kürzel'].startswith('O'):
                name = "Ortsverband %s" % row['Ortsverband']
            elif row['Kürzel'].startswith('G'):
                name = "Geschäftsstelle %s" % row['Geschäftsstelle']
            elif row['Kürzel'].startswith('L'):
                if row['Landesverband / Schule'] == "Hamburg, Mecklenburg-Vorpommern":
                    name = "Landesverband Hamburg, Mecklenburg-Vorpommern, Schleswig-Holstein"
                else:
                    name = "Landesverband %s" % row['Landesverband / Schule']
            elif row["Kürzel"].startswith('S'):
                name = row['Name 1']
            elif row['Kürzel'].startswith('T'):
                if row['Name 1'] == "Leitung":
                    name = "Leitung Technisches Hilfswerk"
                elif row['Name 1'] == "Logistikzentrum":
                    name = "Referat Logistik Heiligenhaus"
                elif row['Name 1'] == "Zentrum für Auslandslogistik":
                    name = row['Name 1']

            else:
                print("Something strange happened - %s" % repr(row))
                continue

            if name not in webaddress:
                print("%s not found in web-scraped addresses" % name)
                continue

            webaddress[name]['code'] = row['Kürzel']

#    for k,v in webaddress.items():
#        if 'code' not in v:
#            print(k)

    return webaddress

def fetch_data(filename=None, url=None):
    """
    Read Dienststellen-data and process it into a dict

    This Method retrieves the data from thw.de (not implemented) or reads the data from a textfile.
    This data is then converted into a dictionary which might be used for further processing

    Args:
        filename (str): Name of file to read data from
        url (str): Url to fetch data from

    Returns:
        dict: containing name, street, city, zip-code, email, fax, phone

    """
    if url is not None:
        raise NotImplementedError()
    if filename is not None and url is not None:
        raise AssertionError("Only filename or url may be set")

    with open(filename) as f:
        data = f.read()

    thw_addresses = dict()

    soup = bs4.BeautifulSoup(data, "html.parser")

    whole_table = soup.find_all("tr", ["zeileUngerade", "zeileGerade"])
    for entry in whole_table:
        department = dict()
        department["name"] = entry.find("a").string

        address_divs = entry.find_all("div", "address")
        location_lines = address_divs[0].find_all("span", "value")
        department["street"] = location_lines[0].string
        department["zip"], department["city"] = location_lines[1].string.strip().split(maxsplit=1)

        contact_lines = address_divs[1].find_all("span", "value")
        department["phone"] = contact_lines[0].string.replace(" ", "")
        if len(contact_lines) == 3:
            department["fax"] = contact_lines[1].string.replace(" ", "")
            department["email"] = contact_lines[2].find("a")["href"].split(":")[1].lower()
        elif len(contact_lines) == 2:
            department["email"] = contact_lines[1].find("a")["href"].split(":")[1].lower()

        if department['name'] == "Geschäftsstelle Frankfurt/Oder":
            department['name'] = "Geschäftsstelle Frankfurt (Oder)"
        thw_addresses[department['name']] = department

    return thw_addresses

def main():
    raw_data_file = 'raw_data.html'
    geo_data_file = 'thw_adressen_geo.csv'

    argp = argparse.ArgumentParser()
    argp.add_argument('--raw-file', required=True)
    argp.add_argument('--geo-csv-file', required=True)
    argp.add_argument('--output-file', required=True)
    args = argp.parse_args()

    thw_de_data = fetch_data(args.raw_file)
    combined_data = combine_with_geo_data(thw_de_data, args.geo_csv_file)

    with open(args.output_file, 'w') as f:
        json.dump(combined_data, f, indent=2)

if __name__ == '__main__':
    main()
