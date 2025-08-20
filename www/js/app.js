import { createApp } from './vue.esm-browser.prod.js'
import db from '../data/db.json' with { type: 'json' }

createApp({
    data() {
        return {
            languageFlavors: [
                'cn',
                'hk',
                'tw',
                'jp',
                'kr',
            ],
            db: db,
            fontsLoadingStatus: 'done',
            input: '',
            displaySans: true,
            displaySerif: true,
            fontSize: 160,
            fontWeight: 400,
            strokeMode: false,
        }
    },
    computed: {
        searchQuery() {
            const query = []
            for (const c of this.input) {
                const codePoint = c.codePointAt(0)
                if (codePoint in this.db.mapping && !query.includes(codePoint)) {
                    query.push(codePoint)
                }
            }
            return query
        },
        settings() {
            return {
                input: this.input,
                displaySans: this.displaySans,
                displaySerif: this.displaySerif,
                fontSize: this.fontSize,
                fontWeight: this.fontWeight,
                strokeMode: this.strokeMode,
            }
        },
    },
    watch: {
        input(newValue) {
            if (newValue.length > 500) {
                this.input = newValue.substring(0, 500)
            } else {
                window.location.hash = newValue
            }
        },
        settings(newValue) {
            console.log('保存配置：', newValue)
            localStorage.setItem('source-han-mapping-viewer', JSON.stringify(newValue))
        },
    },
    async created() {
        document.fonts.addEventListener('loading', () => {
            console.log('字体加载回调：', 'loading')
            this.fontsLoadingStatus = 'loading'
        })
        document.fonts.addEventListener('loadingdone', () => {
            console.log('字体加载回调：', 'done')
            this.fontsLoadingStatus = 'done'
        })
        document.fonts.addEventListener('loadingerror', () => {
            console.log('字体加载回调：', 'error')
            this.fontsLoadingStatus = 'error'
        })

        const json = localStorage.getItem('source-han-mapping-viewer')
        if (json) {
            const settings = JSON.parse(json)
            console.log('加载配置：', settings)
            Object.assign(this, settings)
        }

        const hash = decodeURIComponent(window.location.hash).replace('#', '')
        if (hash !== '') {
            console.log('设置搜索：', hash)
            this.input = hash
        }
    },
    methods: {
        getGlyphColor(glyphName) {
            let suffix
            let i = glyphName.indexOf('-')
            if (i >= 0) {
                suffix = `-${glyphName.slice(i + 1)}`
            } else {
                i = glyphName.indexOf('.')
                if (i >= 0) {
                    suffix = `.${glyphName.slice(i + 1)}`
                } else {
                    suffix = ''
                }
            }

            if (['-CN', '-CN-V'].includes(suffix)) {
                return 'orange'
            }
            if (['-HK'].includes(suffix)) {
                return 'dodgerblue'
            }
            if (['-TW'].includes(suffix)) {
                return 'green'
            }
            if (['-JP', '-JP-V', '-JP90-JP', '-HW-JP'].includes(suffix)) {
                return 'crimson'
            }
            if (['-KR', '-HW-KR'].includes(suffix)) {
                return 'violet'
            }
            if (['.ljmo01', '.ljmo02', '.ljmo03', '.ljmo04', '.ljmo05', '.ljmo06', '.tjmo01', '.tjmo02', '.tjmo03', '.tjmo04', '.vjmo01', '.vjmo02'].includes(suffix)) {
                return 'blueviolet'
            }
            if (['-FW', '-FW-V', '-HW', '-PW', '-V'].includes(suffix)) {
                return 'gray'
            }
            return 'black'
        },
        getCharStyle(isSans, languageFlavor, glyphName) {
            const style = {
                width: `${this.fontSize * 1.4}px`,
                fontSize: `${this.fontSize}px`,
                fontWeight: this.fontWeight,
            }
            if (isSans) {
                style.fontFamily = `SourceHanSans-${languageFlavor.toUpperCase()}, sans-serif`
            } else {
                style.fontFamily = `SourceHanSerif-${languageFlavor.toUpperCase()}, serif`
            }
            if (this.strokeMode) {
                style.color = 'transparent'
                style.webkitTextStrokeColor = this.getGlyphColor(glyphName)
                style.webkitTextStrokeWidth = '2px'
            } else {
                style.color = this.getGlyphColor(glyphName)
            }
            return style
        },
        onResetOptionsClick() {
            this.fontSize = 160
            this.fontWeight = 400
            this.strokeMode = false
        },
        onExampleTextClick(text) {
            this.input = text
        },
    },
}).mount('#app')
