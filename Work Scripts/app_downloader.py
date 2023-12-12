import urllib.parse

def generate_download_link(app_name, app_file_url):
    encoded_app_name = urllib.parse.quote(app_name)
    download_link = f'<a href="{app_file_url}" download="{encoded_app_name}">Download {app_name}</a>'
    return download_link

# Example apps and download URLs
apps = {
    'App1': 'https://example.com/app1.apk',
    'App2': 'https://example.com/app2.apk'
}

for app_name, app_url in apps.items():
    download_link = generate_download_link(app_name, app_url)
    print(download_link)
