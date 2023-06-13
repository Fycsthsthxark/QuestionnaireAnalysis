// 开发环境：true，部署环境：false
const DEBUG = process.env.NODE_ENV !== 'production'

// 配置全局域名
const PROTOCOL = window.location.protocol
const BASE_HOST = window.location.hostname
let BASE_PORT = null
if (DEBUG) BASE_PORT = "8000"
else BASE_PORT = window.location.port
const SERVER_URL = `${PROTOCOL}//${BASE_HOST}:${BASE_PORT}`

/* 跟后端约定的一些参数 */

// JSON数据中传输token时的键
const JSON_TOKEN_KEY = "token"
// 请求头中存放token的键
const HEADER_TOKEN_KEY = "TOKEN"
// 在cookie中存放token的键
const LOCAL_STORAGE_TOKEN_KEY = "token"
// token的前缀
const JWT_AUTH_HEADER_PREFIX = "Bearer "

// 身份过期，重新登录的请求status标识
const RE_LOGIN_STATUS = 401


export default {
    PROTOCOL,
    BASE_HOST,
    BASE_PORT,
    SERVER_URL,
    HEADER_TOKEN_KEY,
    JWT_AUTH_HEADER_PREFIX,
    JSON_TOKEN_KEY,
    RE_LOGIN_STATUS,
    LOCAL_STORAGE_TOKEN_KEY,
    DEBUG
}