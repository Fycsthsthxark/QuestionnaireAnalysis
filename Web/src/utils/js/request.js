import axios from 'axios'
import serverConf from "./serverConf"
import Vue from "vue"


// 创建axios实例，封装成request
const request = axios.create({
    // 全局统一请求的url前缀，页面里面写接口的时候就只补充后续地址：例：/后续地址/
    baseURL: `${serverConf.SERVER_URL}/api/v1`,

    // 指定请求超时的毫秒数(0 表示无超时时间)，超时请求将被中断
    timeout: 0
})


// 请求发送前的 拦截器
request.interceptors.request.use(config => {
    // 若存在token，对所有请求的请求头统一设置token
    const token = localStorage.getItem(serverConf.LOCAL_STORAGE_TOKEN_KEY)
    if (token) config.headers[serverConf.HEADER_TOKEN_KEY] = serverConf.JWT_AUTH_HEADER_PREFIX + token

    return config
}, error => {
    return Promise.reject(error)
})


// 接口响应后的 拦截器
request.interceptors.response.use(response => {
        let data = response.data

        // 通知
        if (data["msg"]) {
            const status = data["status"] === 200
            Vue.prototype.$message({
                message: data["msg"],
                type: status ? 'success' : 'warning'
            })
        }

        // 如果返回的是JSON
        if (typeof data === 'object') {
            // 将服务端发来的token存储到Cookie中
            if (data.hasOwnProperty(serverConf.JSON_TOKEN_KEY) && data[serverConf.JSON_TOKEN_KEY]) {
                localStorage.setItem(serverConf.LOCAL_STORAGE_TOKEN_KEY, data[serverConf.JSON_TOKEN_KEY])
            }
        }

        return data
    },
    error => {
        if (error.response) {
            // 需要重新登录的响应信号
            if (error.response.data.status === serverConf.RE_LOGIN_STATUS) {
                Vue.prototype.$message({
                    message: "请先登录",
                    type: 'warning'
                })
                // setTimeout(() => {
                //     localStorage.clear()
                //     location.href = "/#/loginView/"
                // }, 2000)
            }

            // 服务器响应异常
            else {
                Vue.prototype.$message({
                    message: "请求异常",
                    type: 'warning'
                })
                // setTimeout(() => {
                //     history.back()
                // }, 2000)
            }
        } else {
            Vue.prototype.$message({
                message: "网络异常",
                type: 'warning'
            })
        }

        return Promise.reject(error)
    }
)
export default request
