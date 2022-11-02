from pathlib import Path
import re


def get_file(path):
    with open(path, 'r') as f:
        return f.readlines()


def __retrieve_characteristics(fonts_string):
    regex = r"(?:\?|\&)([\w]+)=([\w+,-]+):(\d+,\d+)([\%7C\w,\+]*)"
    characteristics = re.findall(regex, fonts_string)[0]
    primary_font = characteristics[1]
    font_weight = characteristics[2].split(',')[0]
    additional_fonts = characteristics[3].split('%7C')[1:]
    return primary_font, font_weight, additional_fonts


def __generate_replace_string(characteristics, url):
    blue_print = """
    @font-face {
        font-family: {family};
        font-style: {style};
        font_weight: {weigth};
        src: url('{url}/{name}-{version}-{subset}.eot);'
        src: local(''),
             url('{url}/{name}-{version}-{subset}.eot?#iefix) format('embedded-opentype'),'
             url('{url}/{name}-{version}-{subset}.woff2) format('woff2'),'
             url('{url}/{name}-{version}-{subset}.woff) format('woff'),'
             url('{url}/{name}-{version}-{subset}.ttf) format('truetype'),'
             url('{url}/{name}-{version}-{subset}.svg#{name_capitalized}) format('svg');'
    }
    """
    main_font = blue_print.format(family=characteristics[0].replace('+', ' '),
                                  style='normal',  # TODO: How to determine??
                                  weight=characteristics[1],
                                  url=url,
                                  name=characteristics[0].replace('+', '-'),
                                  version='v23',  # TODO: How to determine??
                                  subset='latin'  # TODO: How to determine??
                                  )

    replace_strs = [main_font]

    for font in characteristics[2]:
        font_str = blue_print.format(family=font.replace('+', ' '),
                                     style='normal',  # TODO: How to determine??
                                     weight=characteristics[1],
                                     url=url,
                                     name=font.replace('+', '-'),
                                     version='v23',  # TODO: How to determine??
                                     subset='latin'  # TODO: How to determine??
                                     )
        replace_strs.append(font_str)
    return replace_strs


def replace_google_fonts(content, url):
    for line in content:
        if 'fonts.googleapis.com' in line:
            characteristics = __retrieve_characteristics(line)
            replace_strings = __generate_replace_string(characteristics, url)
            # TODO: Replace fonts entry with new entries
            return [replace_strings]
    return content


def write_file(path, content):
    pass


def iter_files(path):
    pathlist = Path(path).glob('**/*.html')
    url = ""
    for path in pathlist:
        original_content = get_file(path)
        filtered_content = replace_google_fonts(original_content, url)
        write_file(path, filtered_content)
        if original_content != filtered_content:
            print('Changed file:', path)


def main():
    iter_files('.')


if __name__ == '__main__':
    main()
