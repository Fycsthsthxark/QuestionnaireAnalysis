import Vue from 'vue'
import Vuex from 'vuex'
import DemoModule from "@/store/modules/DemoModule";


Vue.use(Vuex)


export default new Vuex.Store({
    namespaced: true,
    state: {},
    getters: {},
    mutations: {},
    actions: {},
    modules: {
        DemoModule,
    }
})
