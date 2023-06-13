import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'questionnaire',
        // redirect: '/...',
        component: () => import('@/views/Questionnaire.vue'),
        children: [
            {
                path: 'questionnaire',
                name: 'questionnaire',
                component: () => import('@/views/Questionnaire.vue'),
            },
        ]
    },
    {
        path: '/over',
        name: 'over',
        component: () => import('@/views/Over.vue'),
    },
    {
        path: '/dataAnalysis',
        name: 'dataAnalysis',
        component: () => import('@/views/DataAnalysis.vue'),
    },
]

const router = new VueRouter({
    mode: 'hash',
    base: process.env.BASE_URL,
    routes,
})

// 不需要路由跳转延时效果的地址
const noNeedRouterTimeoutPath = []  // ['/a', '/b']


router.beforeEach((to, from, next) => {
    // 路由跳转延时效果
    if (!noNeedRouterTimeoutPath.includes(to.path)) {
        setTimeout(() => next(), 100)
    } else next()
})


// 解决编程式导航跳转报错问题
const originalPush = router.push
const originalReplace = router.replace
router.push = function push(location, onResolve, onReject) {
    if (onResolve || onReject) return originalPush.call(this, location, onResolve, onReject)
    return originalPush.call(this, location).catch(err => err)
}
router.replace = function push(location, onResolve, onReject) {
    if (onResolve || onReject) return originalReplace.call(this, location, onResolve, onReject)
    return originalReplace.call(this, location).catch(err => err)
}

export default router
