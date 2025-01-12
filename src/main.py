import os, shutil

def main():
    source = 'static'
    destination = 'public'
    copy_directory(source, destination)


def copy_directory(source, destination):
    # Delete destination if it exists
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # Make sure destination exists
    if not os.path.exists(destination):
        os.mkdir(destination)
    
    # Get list of everything in source directory
    for item in os.listdir(source):
        # Create full paths
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"file {item} copied from {source} to {destination}")
        else:
            print(f"opening directory {source_path}")
            copy_directory(source_path, dest_path)       

main()