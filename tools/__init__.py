from pathlib import Path

project_root_dir = Path(__file__).parent.joinpath('..').resolve()

assets_dir = project_root_dir.joinpath('assets')
data_dir = assets_dir.joinpath('data')

www_dir = project_root_dir.joinpath('www')
www_data_dir = www_dir.joinpath('data')

font_styles = [
    'sans',
    'serif',
]

language_flavors = [
    'cn',
    'hk',
    'tw',
    'jp',
    'kr',
]

font_versions = {
    'sans': '2.004R',
    'serif': '2.003R',
}
