import requests, zipfile, io, re, os

fonts_dir = '/opt/fonts'
base_url = "https://google-webfonts-helper.herokuapp.com/api/fonts"

# List all fonts
fonts = requests.get(base_url).json()
print('Number of fonts:', len(fonts))

# Download all fonts
print('Start download of fonts')
for font in fonts:
    try:
        cur_url = base_url + '/{}/?download=zip&subsets=latin&variants=regular'.format(font['id'])
        content = requests.get(cur_url)
        z = zipfile.ZipFile(io.BytesIO(content.content))
        font_files = z.namelist()
        z.extractall(fonts_dir)
        for font_file in font_files:
            new_font_file = re.sub(r'-v\d+', '', font_file)
            os.replace(fonts_dir + '/' + font_file, fonts_dir + '/' + new_font_file)
    except Exception as e:
        print(font['id'], e)
print('Finish download of fonts')
