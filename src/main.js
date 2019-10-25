import Vue from 'vue'
import App from './App.vue'
import router from "./router"
import store from './store'
import PouchDB from 'pouchdb-browser'
import PouchVue from 'pouch-vue'
import lf from 'pouchdb-find';
import plf from 'pouchdb-live-find';
import auth from 'pouchdb-authentication';
import vuetify from './plugins/vuetify';
PouchDB.plugin(lf);
PouchDB.plugin(plf);
PouchDB.plugin(auth);

Vue.config.productionTip = false

Vue.use(PouchVue, {
  pouch: PouchDB,    // optional if `PouchDB` is available on the global object
  defaultDB: 'summary',  // this is used as a default connect/disconnect database
  optionDB: {}, // this is used to include a custom fetch() method (see TypeScript example)
  // debug: '*' // optional - See `https://pouchdb.com/api.html#debug_mode` for valid settings (will be a separate Plugin in PouchDB 7.0)
});



new Vue({
  router, 
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
