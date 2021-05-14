Vue.component('led', {
    template: /*html*/
        `
      <div class='card-container md-layout-item md-size-60 md-xsmall-size-95'>
        <md-card>
          <md-switch id="led_on" v-model="led_on" class="md-primary" @change="changeStatus">
            {{ led_on ? 'On' : 'Off' }}
          </md-switch>
        </md-card>
      </div>
      `,
    data() {
        return {
            led_on: false
        }
    },
    methods: {
        async checkStatus() {
            console.log('>> Fetching LED status');
            await Vue.Constants.AWS_CLIENT.fetch(Vue.Constants.SHADOW_URI)
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else if (response.status == 404) {
                        return Promise.reject('No shadow');
                    }
                })
                .then(data => {
                    this.led_on = data.state.reported.led_on;
                    console.log('<< Done');
                })
                .catch(error => console.error(error));
        },
        async changeStatus(value) {
            console.log(`>> Updating LED status to "${value ? 'on' : 'off'}"`);
            await Vue.Constants.AWS_CLIENT.fetch(Vue.Constants.SHADOW_URI, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    state: {
                        desired: {
                            led_on: value
                        }
                    }
                })
            })
                .then(_ => {
                    this.led_on = value;
                    console.log('<< Done');
                })
                .catch(error => console.error(error));
        }
    },
    mounted() {
        this.checkStatus();
    }
});
