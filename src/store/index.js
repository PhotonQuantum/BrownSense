import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    dbs: {},
    bread_nav: []
  },
  mutations: {
      add_db(store, db){
        Vue.set(store.dbs, db.name, db.instance);
      },
      set_nav(store, nav){
          store.bread_nav = nav;
      }
  },
  actions: {
  },
  modules: {
  }
})
