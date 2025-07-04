import shutil

import httpx

from tools import configs
from tools.configs import path_define


def _fetch_raw_data(font_style: str, font_version: str, file_name: str):
    url = f'https://raw.githubusercontent.com/adobe-fonts/source-han-{font_style}/{font_version}/Resources/{file_name}'
    response = httpx.get(url)
    assert response.is_success and 'text/plain' in response.headers['Content-Type']
    file_path = path_define.fonts_dir.joinpath(font_style).joinpath(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(response.text.replace('\t', ' '), 'utf-8')
    print(f"Update: '{url}'")


def main():
    if path_define.fonts_dir.exists():
        shutil.rmtree(path_define.fonts_dir)

    for font_style in configs.font_styles:
        font_version = configs.font_versions[font_style]
        _fetch_raw_data(font_style, font_version, f'AI0-SourceHan{font_style.capitalize()}')
        for language_flavor in configs.language_flavors:
            _fetch_raw_data(font_style, font_version, f'utf32-{language_flavor}.map')


if __name__ == '__main__':
    main()
