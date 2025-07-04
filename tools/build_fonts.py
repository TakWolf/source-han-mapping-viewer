import shutil
from collections import defaultdict
from io import StringIO

import unidata_blocks
from fontTools import subset
from fontTools.ttLib import TTFont

from tools import configs
from tools.configs import path_define


def _get_slice_alphabets(alphabet: list[int]) -> list[tuple[str, list[int]]]:
    block_alphabets = defaultdict[str, list[int]](list)
    for code_point in alphabet:
        block = unidata_blocks.get_block_by_code_point(code_point)
        block_alphabets[block.name].append(code_point)

    slice_alphabets = []
    for block_name, block_alphabet in block_alphabets.items():
        slice_name = block_name.replace(' ', '-')
        slice_index = 0
        slice_alphabet = []
        for code_point in sorted(block_alphabet):
            if len(slice_alphabet) >= 200:
                slice_alphabets.append((f'{slice_name}-{slice_index}', slice_alphabet))
                slice_index += 1
                slice_alphabet = []
            slice_alphabet.append(code_point)
        slice_alphabets.append((f'{slice_name}-{slice_index}', slice_alphabet))
    return slice_alphabets


def _alphabet_to_text(alphabet: list[int]) -> str:
    return ''.join(chr(code_point) for code_point in sorted(alphabet))


def _alphabet_to_unicode_range(alphabet: list[int]) -> str:
    pairs = []
    code_start = None
    code_end = None
    for code_point in sorted(alphabet):
        if code_start is None:
            assert code_end is None
            code_start = code_point
            code_end = code_point
        elif code_point == code_end + 1:
            code_end = code_point
        else:
            pairs.append((code_start, code_end))
            code_start = code_point
            code_end = code_point
    pairs.append((code_start, code_end))

    unicode_range = []
    for code_start, code_end in pairs:
        if code_start == code_end:
            unicode_range.append(f'U+{code_start:04X}')
        else:
            unicode_range.append(f'U+{code_start:04X}-{code_end:04X}')
    return ', '.join(unicode_range)


def main():
    if path_define.www_fonts_dir.exists():
        shutil.rmtree(path_define.www_fonts_dir)
    path_define.www_fonts_dir.mkdir(parents=True)

    index_css = StringIO()

    for font_style in configs.font_styles:
        font_style_css = StringIO()

        font_style_dir = path_define.www_fonts_dir.joinpath(font_style)
        font_style_dir.mkdir(parents=True)

        for language_flavor, name_flavor in configs.language_flavors.items():
            font_path = path_define.fonts_dir.joinpath(font_style, f'SourceHan{font_style.capitalize()}{name_flavor}-VF.otf.woff2')
            slice_alphabets = _get_slice_alphabets(TTFont(font_path).getBestCmap())

            language_flavor_css = StringIO()

            language_flavor_dir = font_style_dir.joinpath(language_flavor)
            language_flavor_dir.mkdir(parents=True)

            for slice_name, slice_alphabet in slice_alphabets:
                print(f'{slice_name}: {len(slice_alphabet)}')

                sliced_font_path = language_flavor_dir.joinpath(f'SourceHan{font_style.capitalize()}-{language_flavor.upper()}-VF-{slice_name}.otf.woff2')
                subset.main([
                    f'{font_path}',
                    f'--text={_alphabet_to_text(slice_alphabet)}',
                    "--layout-features='*'",
                    f'--output-file={sliced_font_path}',
                ])
                print(f"Make Font: '{sliced_font_path}'")

                language_flavor_css.write('\n')
                language_flavor_css.write('@font-face {\n')
                language_flavor_css.write(f'    font-family: SourceHan{font_style.capitalize()}-{language_flavor.upper()};\n')
                language_flavor_css.write('    font-display: swap;\n')
                language_flavor_css.write(f'    src: url("{sliced_font_path.name}") format("woff2");\n')
                language_flavor_css.write(f'    unicode-range: {_alphabet_to_unicode_range(slice_alphabet)};\n')
                language_flavor_css.write('}\n')

            language_flavor_css_path = language_flavor_dir.joinpath('index.css')
            language_flavor_css_path.write_text(language_flavor_css.getvalue(), 'utf-8')
            print(f"Make CSS: '{language_flavor_css_path}'")

            font_style_css.write(f'@import "{language_flavor}/index.css";\n')

        font_style_css_path = font_style_dir.joinpath('index.css')
        font_style_css_path.write_text(font_style_css.getvalue(), 'utf-8')
        print(f"Make CSS: '{font_style_css_path}'")

        index_css.write(f'@import "{font_style}/index.css";\n')

    index_css_path = path_define.www_fonts_dir.joinpath('index.css')
    index_css_path.write_text(index_css.getvalue(), 'utf-8')
    print(f"Make CSS: '{index_css_path}'")


if __name__ == '__main__':
    main()
