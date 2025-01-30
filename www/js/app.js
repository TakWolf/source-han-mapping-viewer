import { createApp } from './vue.esm-browser.prod.js'
import db from '../data/db.js'

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
            input: '',
            displaySans: true,
            displaySerif: true,
            fontSize: 160,
            fontWeight: 400,
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
            }
        },
    },
    watch: {
        input(newValue) {
            window.location.hash = newValue
        },
        settings(newValue) {
            console.log('保存配置：', newValue)
            localStorage.setItem('source-han-mapping-viewer', JSON.stringify(newValue))
        },
    },
    async created() {
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
            if (glyphName.endsWith('-CN')) {
                return 'orange'
            }
            if (glyphName.endsWith('-HK')) {
                return 'dodgerblue'
            }
            if (glyphName.endsWith('-TW')) {
                return 'green'
            }
            if (glyphName.endsWith('-JP90-JP')) {
                return 'crimson'
            }
            if (glyphName.endsWith('uE0101-JP')) {
                return 'darkred'
            }
            if (glyphName.endsWith('uE0102-JP')) {
                return 'indianred'
            }
            if (glyphName.endsWith('-JP')) {
                return 'red'
            }
            if (glyphName.endsWith('-KR')) {
                return 'violet'
            }
            return 'black'
        },
        onResetOptionsClick() {
            this.fontSize = 160
            this.fontWeight = 400
        },
        onExampleTextClick(text) {
            this.input = text
        },
    },
}).mount('#app')
