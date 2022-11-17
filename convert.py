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
    @font-face {{
        font-family: {family};
        font-style: {style};
        font_weight: {weight};
        src: url('{url}/{name}-{version}-{subset}.eot');
        src: local(''),
             url('{url}/{name}-{subset}-{variant}.eot?#iefix') format('embedded-opentype'),
             url('{url}/{name}-{subset}-{variant}.woff2') format('woff2'),
             url('{url}/{name}-{subset}-{variant}.woff') format('woff'),
             url('{url}/{name}-{subset}-{variant}.ttf') format('truetype'),
             url('{url}/{name}-{subset}-{variant}.svg#{name_capitalized}') format('svg');
    }}
    """
    main_font = blue_print.format(family=characteristics[0].replace('+', ' '),
                                  style='normal',  # TODO: How to determine??
                                  weight=characteristics[1],
                                  url=url,
                                  name=characteristics[0].replace('+', '-'),
                                  subset='latin',
                                  variant='regular',
                                  name_capitalized=characteristics[0].replace('+', '')
                                  )

    replace_strs = [main_font]

    for font in characteristics[2]:
        font_str = blue_print.format(family=font.replace('+', ' '),
                                     style='normal',  # TODO: How to determine??
                                     weight=characteristics[1],
                                     url=url,
                                     name=font.replace('+', '-'),
                                     subset='latin',
                                     variant='regular',
                                     name_capitalized=font.replace('+', '')
                                     )
        replace_strs.append(font_str)
    return "\n".join(replace_strs)


def replace_google_fonts(c, url):
    content = c.copy()
    matching_indices = [idx for idx, line in enumerate(content) if "fonts.googleapis" in line]
    if not len(matching_indices):
        return c
    replace_strs = "<style>\n"
    for idx in reversed(matching_indices):
        characteristics = __retrieve_characteristics(content[idx])
        replace_str = __generate_replace_string(characteristics, url)
        del content[idx]
        replace_strs += replace_str
        replace_strs += '\n'
    head_end = [idx for idx, line in enumerate(content) if "</head>" in line][0]
    content.insert(head_end, replace_strs + '</style>\n')
    return content


def write_file(path, content):
    with open(path, 'w') as f:
        f.writelines(content)


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
