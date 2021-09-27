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