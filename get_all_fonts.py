import requests, zipfile, io

base_url = "https://google-webfonts-helper.herokuapp.com/api/fonts"

# List all fonts
fonts = requests.get(base_url).json()
print('Number of fonts:', len(fonts))

# Download all fonts
print('Start download of fonts')
for font in fonts:
    try:
        cur_url = base_url + '/{}/?download=zip'.format(font['id'])
        content = requests.get(cur_url)
        z = zipfile.ZipFile(io.BytesIO(content.content))
        z.extractall('/opt/fonts')
        break
    except Exception as e:
        print(font['id'], e)
print('Finish download of fonts')
