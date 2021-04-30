Vue.component('arm-switch', {
  template: /*html*/
    `
    <div class='arm-switch-container'>
      <md-switch id="arm-switch" v-model="armed" class="md-primary" @change="changeArmed">
        {{ armed ? 'Armed' : 'Unarmed' }}
      </md-switch>
    </div>
    `,
  data() {
    return {
      armed: false
    }
  },
  methods: {
    checkStatus() {
      console.log('>> Fetching status');
      axios
        .get(`${Vue.Constants.SERVICE_URL}/status`)
        .then(response => {
          this.armed = response.data.armed;
          console.log('<< Done');
        });
    },
    changeArmed(value) {
      axios
        .patch(`${Vue.Constants.SERVICE_URL}/status`, {
          armed: value
        })
        .then(_ => {
          this.armed = value;
        });
    }
  },
  mounted() {
    this.checkStatus();
  }
});
