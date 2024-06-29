import json
import shutil
from typing import Any

import unidata_blocks
from character_encoding_utils import gb2312, big5, shiftjis, ksx1001

from tools import data_dir, www_data_dir, font_styles, language_flavors


def _build_mapping() -> dict[int, Any]:
    mapping = {}

    for font_style in font_styles:
        glyph_id_to_name = {}
        ai0_text = data_dir.joinpath(font_style, f'AI0-SourceHan{font_style.capitalize()}').read_text('utf-8')
        for line in ai0_text.splitlines():
            tokens = line.split(' ')
            glyph_id = int(tokens[0])
            glyph_name = tokens[3]
            glyph_id_to_name[glyph_id] = glyph_name

        for language_flavor in language_flavors:
            map_text = data_dir.joinpath(font_style, f'utf32-{language_flavor}.map').read_text('utf-8')
            for line in map_text.splitlines():
                tokens = line.split(' ')
                code_point = int(tokens[0].removeprefix('<').removesuffix('>'), 16)
                glyph_id = int(tokens[1])
                glyph_name = glyph_id_to_name[glyph_id]

                if code_point not in mapping:
                    c = chr(code_point)
                    tags = [unidata_blocks.get_block_by_code_point(code_point).name]

                    gb2312_category = gb2312.query_category(c)
                    if gb2312_category is not None:
                        tags.append(f'gb2312/{gb2312_category}')

                    big5_category = big5.query_category(c)
                    if big5_category is not None:
                        tags.append(f'big5/{big5_category}')

                    shiftjis_category = shiftjis.query_category(c)
                    if shiftjis_category is not None:
                        tags.append(f'shiftjis/{shiftjis_category}')

                    ksx1001_category = ksx1001.query_category(c)
                    if ksx1001_category is not None:
                        tags.append(f'ksx1001/{ksx1001_category}')

                    mapping[code_point] = {
                        'tags': tags,
                    }

                if font_style not in mapping[code_point]:
                    mapping[code_point][font_style] = {}

                mapping[code_point][font_style][language_flavor] = glyph_name

    return mapping


def main():
    if www_data_dir.exists():
        shutil.rmtree(www_data_dir)
    www_data_dir.mkdir(parents=True)

    mapping = _build_mapping()

    file_path = www_data_dir.joinpath('mapping.json')
    file_path.write_text(json.dumps(mapping), 'utf-8')
    print(f"Build: '{file_path}'")


if __name__ == '__main__':
    main()
