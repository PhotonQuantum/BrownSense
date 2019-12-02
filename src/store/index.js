import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    dbs: {}
  },
  mutations: {
      add_db(store, db){
        Vue.set(store.dbs, db.name, db.instance)
      }
  },
  actions: {
  },
  modules: {
  }
})
