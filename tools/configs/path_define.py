from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent.joinpath('..', '..').resolve()

ASSETS_DIR = PROJECT_ROOT_DIR.joinpath('assets')
FONTS_DIR = ASSETS_DIR.joinpath('fonts')

CACHE_DIR = PROJECT_ROOT_DIR.joinpath('cache')

WWW_DIR = PROJECT_ROOT_DIR.joinpath('www')
WWW_FONTS_DIR = WWW_DIR.joinpath('fonts')
WWW_DATA_DIR = WWW_DIR.joinpath('data')
