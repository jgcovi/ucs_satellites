from datetime import datetime
import requests
from bs4 import BeautifulSoup
from hashlib import md5
from requests.sessions import RecentlyUsedContainer

from utils import get_files_in_dir

def get_date_updated_on(soup):
    """Get the date of the last page update."""
    updated_on_str = soup.find_all('span', attrs={'class': "date-updated"})[0].contents[0]
    updated_on_str = updated_on_str.lower().lstrip('updated ')
    return datetime.strptime(updated_on_str, '%B %d, %Y')

def get_file_checksum(f):
    pass

def save_file(file_url, fname):
    """Download the file from the url."""
    req = requests.get(file_url, allow_redirects=True)
    with open(fname, 'wb') as output:
        output.write(req.content)
        
def get_file_from_ucs_page(url='https://www.ucsusa.org/resources/satellite-database', data_dir='data'):
    """Read the UCS webpage to determine if there is a new file available. If yes, then save it."""
    # Get info to build urls later
    protocol = url.split('//')[0]  # get transfer protocol
    domain = url.split('//')[1].split('/')[0]  # get url domain
    # Get the url contents
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    updated_on = get_date_updated_on(soup)

    # Create filename with updated_on date 
    read_fname = 'usc_satellites_' + datetime.strftime(updated_on, '%Y%b%d') + '.csv'
    # Get the contents of the data_dir file where the file should be located, if already saved
    data_files = get_files_in_dir(data_dir)
    # if the data dir is empty OR a filename matching the most recent version is not in the dir, save the new file
    if (len(data_files) == 0) | (not any([f == read_fname for f in data_files])):  
        db_filelist = []
        for a in soup.find_all('a', href=True):
            if ('/media/' in a['href']) & (a.contents[0] == 'Database'):
                db_filelist.append(a['href'])
        file_path = db_filelist[0]  # the first one is the Excel version.
        save_file(protocol + '//' + domain + file_path, read_fname)
    
    return read_fname
