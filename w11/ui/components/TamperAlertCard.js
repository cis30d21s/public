Vue.component('tamper-alert-card', {
    template: /*html*/
        `
        <div class="card-container md-layout-item md-size-60 md-xsmall-size-95">
            <md-card md-with-hover>
                <md-card-header>
                    <md-content class="md-headline text-left">Tamper alert</md-content>
                </md-card-header>
                <div class="md-layout md-alignment-center-center">
                    <md-content class="md-display-1 md-layout-item md-size-35 md-small-size-45 md-xsmall-size-50">
                        {{ tampered ? "Tampered" : "Not tampered" }}
                    </md-content>
                    <md-card-media-actions class="md-layout-item md-layout md-alignment-center-right">
                        <md-card-media>
                            <md-icon class="md-size-3x" :class="tampered ? 'md-accent' : 'md-primary'">
                                {{ tampered ? "error_outline" : "check_circle_outline" }}
                            </md-icon>
                        </md-card-media>
                        <md-card-media>
                            <md-button class="md-icon-button" v-show="tampered" @click="clear">
                                <md-icon>clear</md-icon>
                            </md-button>
                        </md-card-media>
                    </md-card-media-actions>
                </div>
            </md-card>
        </div>
        `,
    data() {
        return {
            tampered: false
        }
    },
    methods: {
        clear() {
            this.tampered = false;
        }
    }
});
