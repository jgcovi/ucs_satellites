import os

def check_dir(dirname, mkdir=False):
    """If the folder does not already exist in the project directory, create it if mkdir is True. Return the full path to the folder."""
    project_dir = os.path.abspath(os.getcwd())
    new_dir = project_dir + '/' + dirname.strip('/') + '/' if not project_dir in dirname else dirname
    if not os.path.exists(new_dir) and mkdir:
        os.mkdir(new_dir)
    return new_dir

def get_files_in_dir(dirname='data', mkdir=True):
    """Return all files in the given directory."""
    new_dir = check_dir(dirname, mkdir)
    return os.listdir(new_dir)

def is_file_in_dir(fname, dirname):
    """Returns true if the file is in the directory. Returns False if the directory does not exist or the file is not there."""
    dirpath = check_dir(dirname)
    if not os.path.exists(dirpath) | (not fname in get_files_in_dir(dirname, mkdir=False)):
        return False
    return True

def split_url_protocol(url):
    """"Split a given URL into the protocol, domain, and path for the use of building linked URLs."""
    # Get info to build urls later
    url_split = url.split('//')  # split url into transfer protocol and domain+path
    protocol = url_split[0]  # get transfer protocol
    domain = url_split[1].split('/')[0]  # get url domain

    return protocol, domain
