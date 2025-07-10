import json
import shutil
import zipfile

from loguru import logger

from tools import configs
from tools.configs import path_define
from tools.utils import github_api, download_util


def _upgrade_fonts(font_style: str):
    repository_name = f'adobe-fonts/source-han-{font_style}'
    version = github_api.get_releases_latest_tag_name(repository_name).removesuffix('R')

    fonts_dir = path_define.fonts_dir.joinpath(font_style)
    version_file_path = fonts_dir.joinpath('version.json')
    if version_file_path.exists():
        version_info = json.loads(version_file_path.read_bytes())
        if version == version_info['version']:
            return
    logger.info("Need upgrade fonts '{}' to version: '{}'", font_style, version)

    download_dir = path_define.cache_dir.joinpath(repository_name, version)
    download_dir.mkdir(parents=True, exist_ok=True)

    asset_file_name = f'SourceHan{font_style.capitalize()}-VF.zip'
    asset_file_path = download_dir.joinpath(asset_file_name)
    asset_url = f'https://github.com/{repository_name}/releases/download/{version}R/02_{asset_file_name}'
    if not asset_file_path.exists():
        logger.info("Start download: '{}'", asset_url)
        download_util.download_file(asset_url, asset_file_path)
    else:
        logger.info("Already downloaded: '{}'", asset_file_path)

    asset_unzip_dir = asset_file_path.with_suffix('')
    if asset_unzip_dir.exists():
        shutil.rmtree(asset_unzip_dir)
    with zipfile.ZipFile(asset_file_path) as file:
        file.extractall(asset_unzip_dir)
    logger.info("Unzip: '{}'", asset_unzip_dir)

    if fonts_dir.exists():
        shutil.rmtree(fonts_dir)
    fonts_dir.mkdir(parents=True)

    shutil.copyfile(asset_unzip_dir.joinpath('LICENSE.txt'), fonts_dir.joinpath('LICENSE.txt'))
    logger.info("Copy: 'LICENSE.txt'")

    for file_path in asset_unzip_dir.joinpath('Variable', 'WOFF2', 'OTF').iterdir():
        if file_path.suffix != '.woff2':
            continue
        shutil.copyfile(file_path, fonts_dir.joinpath(file_path.name))
        logger.info("Copy: '{}'", file_path.name)

    shutil.rmtree(asset_unzip_dir)

    ai0_file_name = f'AI0-SourceHan{font_style.capitalize()}'
    download_util.download_file(f'https://raw.githubusercontent.com/{repository_name}/{version}R/Resources/{ai0_file_name}', fonts_dir.joinpath(ai0_file_name))
    logger.info("Downloaded: '{}'", ai0_file_name)

    for language_flavor in configs.language_flavors:
        utf_file_name = f'utf32-{language_flavor}.map'
        download_util.download_file(f'https://raw.githubusercontent.com/{repository_name}/{version}R/Resources/{utf_file_name}', fonts_dir.joinpath(utf_file_name))
        logger.info("Downloaded: '{}'", utf_file_name)

    version_info = {
        'version': version,
        'version_url': f'https://github.com/adobe-fonts/source-han-serif/releases/tag/{version}R',
    }
    version_file_path.write_text(f'{json.dumps(version_info, indent=2, ensure_ascii=False)}\n', 'utf-8')
    logger.info("Update version file: '{}'", version_file_path)


def main():
    for font_style in configs.font_styles:
        _upgrade_fonts(font_style)


if __name__ == '__main__':
    main()
