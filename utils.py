import requests


def get_html(url):
    response = requests.get(url)
    html = response.text
    return html


def save_to_file(filename, html):
    try:
        with open("output\\" + filename, 'w', encoding="utf-8") as f:
            f.write(html)
    except Exception as e:
        print(e)
        return False
    return True


def sanitize_filename(filename):
    invalid_chars = '\\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
