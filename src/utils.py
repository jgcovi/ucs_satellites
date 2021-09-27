import os

def get_files_in_dir(dirname='data'):
    """Return all files in the given directory. 
    If the folder does not already exist in the project directory, create it."""
    dirname = dirname.lstrip('/').rstrip('/')  # remove any already included '/'s
    project_dir = os.path.abspath(os.getcwd())
    new_dir = project_dir + '/' + dirname + '/'
    if not os.path.exists(project_dir):
        os.mkdir(new_dir)
    return os.listdir(new_dir)

def split_url(url):
    """"Split a given URL into the protocol, domain, and path for the use of building linked URLs."""
    # Get info to build urls later
    url_split = url.split('//')
    protocol = url_split[0]  # get transfer protocol
    domain = url_split[1].split('/')[0]  # get url domain

    return protocol, domain