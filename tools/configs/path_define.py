from pathlib import Path

project_root_dir = Path(__file__).parent.joinpath('..', '..').resolve()

assets_dir = project_root_dir.joinpath('assets')
fonts_dir = assets_dir.joinpath('fonts')

cache_dir = project_root_dir.joinpath('cache')

www_dir = project_root_dir.joinpath('www')
www_data_dir = www_dir.joinpath('data')
