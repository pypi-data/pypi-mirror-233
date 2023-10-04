from pathvalidate import sanitize_filepath


def clean_filename(filename):
    filename = sanitize_filepath(filename)
    count = 1
    while count:
        new_filename = filename.replace("..", ".")
        count = filename.count("..")
        filename = new_filename

    return filename