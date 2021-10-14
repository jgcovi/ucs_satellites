from datetime import datetime
from functools import update_wrapper
import requests
from bs4 import BeautifulSoup

import utils

#### General webscraping functions

def save_web_file(file_url, fname):
    """Download the file from the url."""
    req = requests.get(file_url, allow_redirects=True)
    print(fname)
    with open(fname, 'wb') as output:
        output.write(req.content)

def get_webpage_contents(url):
    """Return webpage contents from a url."""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    updated_on = get_ucs_date_updated_on(soup)

    return soup, updated_on

#### Page specific functions

# Union of Concerned Scientists webpage
def get_ucs_date_updated_on(soup):
    """Get the date of the last page update."""
    updated_on_str = soup.find_all('span', attrs={'class': "date-updated"})[0].contents[0]
    updated_on_str = updated_on_str.lower().lstrip('updated ')
    return datetime.strptime(updated_on_str, '%B %d, %Y')
        
def get_file_from_ucs_page(url='https://www.ucsusa.org/resources/satellite-database', data_dir='data'):
    """Read the UCS webpage to determine if there is a new file available. If yes, then save it."""
    protocol, domain = utils.split_url_protocol(url)  # get the transfer protocol and domain to build linked url later
    soup, updated_on = get_webpage_contents(url)

    # Create filename with updated_on date 
    sat_fname = 'usc_satellites_' + datetime.strftime(updated_on, '%Y%b%d') + '.xls'
    save_sat_fname = data_dir + '/' + sat_fname
    
    # Get the contents of the data_dir file where the file should be located, if already saved
    my_files = utils.get_files_in_dir(data_dir)
    # if the data dir is empty OR a filename matching the most recent version is not in the dir, save the new file
    if (len(my_files) == 0) | (not sat_fname in my_files):  
        db_filelist = []
        for a in soup.find_all('a', href=True):
            if ('/media/' in a['href']) & (a.contents[0] == 'Database'):
                db_filelist.append(a['href'])
        db_url_path = db_filelist[0]  # doesn't matter which one we save as long as we save to excel
        # both links work saving to excel, but one format does not save to csv well
        save_web_file(protocol + '//' + domain + db_url_path,  save_sat_fname)
    return save_sat_fname

# Planetary Org's NASA budget
def get_nasa_budget(url='https://www.planetary.org/space-policy/nasa-budget', data_dir='data'):
    pass

# Country's GDPs
def get_global_gdp(url, data_dir='data'):
    pass 