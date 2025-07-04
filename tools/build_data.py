import json
import shutil

import unidata_blocks
from character_encoding_utils import gb2312, big5, shiftjis, ksx1001

from tools import configs
from tools.configs import path_define


def _build_db() -> dict:
    tags = []

    for block in unidata_blocks.get_blocks():
        tags.append(block.name)
    for category in gb2312.get_categories():
        tags.append(f'gb2312/{category}')
    for category in big5.get_categories():
        tags.append(f'big5/{category}')
    for category in shiftjis.get_categories():
        tags.append(f'shiftjis/{category}')
    for category in ksx1001.get_categories():
        tags.append(f'ksx1001/{category}')

    ai0 = {}

    for font_style in configs.font_styles:
        glyph_names = []
        for line in path_define.fonts_dir.joinpath(font_style, f'AI0-SourceHan{font_style.capitalize()}').read_text('utf-8').splitlines():
            tokens = line.split('\t')
            glyph_name = tokens[3]
            glyph_names.append(glyph_name)
        ai0[font_style] = glyph_names

    mapping = {}

    for (font_style_index, font_style) in enumerate(configs.font_styles):
        for language_flavor in configs.language_flavors:
            for line in path_define.fonts_dir.joinpath(font_style, f'utf32-{language_flavor}.map').read_text('utf-8').splitlines():
                tokens = line.split('\t')
                code_point = int(tokens[0].removeprefix('<').removesuffix('>'), 16)
                glyph_id = int(tokens[1])

                if code_point not in mapping:
                    c = chr(code_point)
                    tag_indices = [tags.index(unidata_blocks.get_block_by_code_point(code_point).name)]

                    gb2312_category = gb2312.query_category(c)
                    if gb2312_category is not None:
                        tag_indices.append(tags.index(f'gb2312/{gb2312_category}'))

                    big5_category = big5.query_category(c)
                    if big5_category is not None:
                        tag_indices.append(tags.index(f'big5/{big5_category}'))

                    shiftjis_category = shiftjis.query_category(c)
                    if shiftjis_category is not None:
                        tag_indices.append(tags.index(f'shiftjis/{shiftjis_category}'))

                    ksx1001_category = ksx1001.query_category(c)
                    if ksx1001_category is not None:
                        tag_indices.append(tags.index(f'ksx1001/{ksx1001_category}'))

                    mapping[code_point] = [
                        [],
                        [],
                        tag_indices,
                    ]

                mapping[code_point][font_style_index].append(glyph_id)

    return {
        'tags': tags,
        'ai0': ai0,
        'mapping': mapping,
    }


def main():
    if path_define.www_data_dir.exists():
        shutil.rmtree(path_define.www_data_dir)
    path_define.www_data_dir.mkdir(parents=True)

    db = _build_db()

    file_path = path_define.www_data_dir.joinpath('db.js')
    file_path.write_text(f'export default {json.dumps(db)}', 'utf-8')
    print(f"Build: '{file_path}'")


if __name__ == '__main__':
    main()
