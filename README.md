# 思源映射查看器

查看思源字体字形映射的便捷工具。

## 在线访问

[点此链接](https://source-han-mapping-viewer.takwolf.com) 在线访问。

## 本地构建

```shell
python -m tools.build_fonts
python -m tools.build_data
```

## 字体切片

为了优化网络加载体验，基于 [CSS unicode-range](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range) 特性，对 woff2 字体进行切片。

导入 CSS 样式：

```html
<link rel="stylesheet" href="https://source-han-mapping-viewer.takwolf.com/fonts/index.css">
```

然后可以在样式中使用：

```css
body {
    font-family: SourceHanSans-CN, sans-serif;
}

h1 {
    font-family: SourceHanSerif-CN, serif;
}
```

全部字体名如下：

| 字体 | font-family |
|---|---|
| 黑体 - 简体中文 | SourceHanSans-CN |
| 黑体 - 繁体中文 - 香港 | SourceHanSans-HK |
| 黑体 - 繁体中文 - 台湾 | SourceHanSans-TW |
| 黑体 - 日语 | SourceHanSans-JP |
| 黑体 - 韩语 | SourceHanSans-KR |
| 宋体 - 简体中文 | SourceHanSerif-CN |
| 宋体 - 繁体中文 - 香港 | SourceHanSerif-HK |
| 宋体 - 繁体中文 - 台湾 | SourceHanSerif-TW |
| 宋体 - 日语 | SourceHanSerif-JP |
| 宋体 - 韩语 | SourceHanSerif-KR |

## 字体版本

- [思源黑体 - 2.005R](https://github.com/adobe-fonts/source-han-sans/releases/tag/2.005R)
- [思源宋体 - 2.003R](https://github.com/adobe-fonts/source-han-serif/releases/tag/2.003R)

## 程序依赖

- [HTTPX](https://github.com/encode/httpx)
- [tqdm](https://github.com/tqdm/tqdm)
- [FontTools](https://github.com/fonttools/fonttools)
- [Unidata Blocks](https://github.com/TakWolf/unidata-blocks)
- [Character Encoding Utils](https://github.com/TakWolf/character-encoding-utils)
- [Vue.js](https://cn.vuejs.org)

## 参考资料

- [MDN - CSS unicode-range](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range)
- [FontTools Docs - pyftsubset](https://fonttools.readthedocs.io/en/latest/subset/)

## 灵感来源

[思源映射管理器](https://github.com/NightFurySL2001/shs-cid)

## 许可证

[MIT License](LICENSE)
