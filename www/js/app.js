import {createApp} from './vue.esm-browser.prod.js'

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
            mapping: null,
            mappingLoadFailed: false,
            input: '',
            displaySans: true,
            displaySerif: true,
            fontSize: 160,
            fontWeight: 400,
        }
    },
    computed: {
        searchQuery() {
            let query = []
            for (let c of this.input) {
                let codePoint = c.codePointAt(0)
                if (codePoint in this.mapping && !query.includes(codePoint)) {
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
        settings(newValue) {
            console.log(newValue)
            localStorage.setItem('source-han-mapping-viewer', JSON.stringify(newValue))
        },
    },
    async created() {
        try {
            let response = await fetch('data/mapping.json')
            if (response.ok) {
                this.mapping = await response.json()
                console.debug(this.mapping)
            } else {
                this.mappingLoadFailed = true
                return
            }
        } catch (e) {
            this.mappingLoadFailed = true
            return
        }

        let json = localStorage.getItem('source-han-mapping-viewer')
        if (json) {
            Object.assign(this, JSON.parse(json))
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
            if (glyphName.endsWith('-JP')) {
                return 'red'
            }
            if (glyphName.endsWith('-KR')) {
                return 'violet'
            }
            return 'black'
        },
    },
}).mount('#app')
