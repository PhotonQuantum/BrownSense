import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    summary_pulled: false
  },
  mutations: {
    set_summary_pulled(state, is_pulled){
      state.summary_pulled = is_pulled;
    }
  },
  actions: {
  },
  modules: {
  }
})
