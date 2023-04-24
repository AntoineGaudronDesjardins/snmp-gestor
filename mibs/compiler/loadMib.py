import urllib.request

mibs_to_download = []

for mib in mibs_to_download:
    url = f'http://www.circitor.fr/Mibs/Mib/{mib[0]}/{mib}.mib'
    filename = f'mibs/mibs/{mib}.mib'
    try:
        urllib.request.urlretrieve(url, filename)
        print(f'Successfully downloaded {mib}')
    except:
        print(f'Error downloading {mib}: {sys.exc_info()[1]}')
