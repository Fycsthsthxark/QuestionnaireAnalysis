import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import request from "@/utils/js/request"
import $ from 'jquery'
import publicJS from '@/utils/js/public'
import "@/utils/style/public.less"


// 使用到的element组件
import {
    Message,
    Button,
    Radio,
    Input,
    Image,
    Loading
} from 'element-ui'

Vue.use(Button)
Vue.use(Radio)
Vue.use(Input)
Vue.use(Image)
Vue.use(Loading)

Vue.prototype.$message = Message


Vue.prototype.request = request
Vue.prototype.$ = $
// 公共JS对象
Vue.prototype.$public = publicJS
Vue.prototype.$EventBus = new Vue()


Vue.config.productionTip = false


new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')