Vue.component('motion-distance-card', {
    template: /*html*/
        `
        <div class="card-container md-layout-item md-size-60 md-xsmall-size-95">
            <!--<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.3/css/all.css">-->
            <md-card md-with-hover>
                <md-card-header>
                    <md-content class="md-headline text-left">Motion/distance sensor</md-content>
                </md-card-header>
                <div class="md-layout md-gutter md-alignment-center-center">
                    <md-card-media-actions class="md-layout-item md-size-25">
                        <md-card-media>
                            <md-icon class="md-size-3x">directions_run</md-icon>
                            <md-icon v-show="motion">rss_feed</md-icon>
                        </md-card-media>
                    </md-card-media-actions>
                    <div class="md-layout-item md-layout">
                        <md-content class="md-subheading md-layout-item md-size-5 md-small-size-10 md-xsmall-hide">0</md-content>
                        <md-progress-bar class="md-layout-item md-elevation-8 md-xsmall-size-95"
                            :class="motion ? 'md-accent' : 'md-primary'"
                            md-mode="determinate"
                            :md-value="distance * 100"></md-progress-bar>
                        <md-tooltip md-direction="top">
                            <span class="md-caption md-subheading tooltip">{{ distance.toFixed(1) }}</span>
                        </md-tooltip>
                        <md-content class="md-subheading md-layout-item md-size-5 md-small-size-10 md-xsmall-hide">1m</md-content>
                    </div>
                </div>
            </md-card>
        </div>
        `,
    data() {
        return {
            motion: false,
            distance: 1
        }
    }
});
