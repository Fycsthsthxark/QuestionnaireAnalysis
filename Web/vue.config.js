const {defineConfig} = require('@vue/cli-service')


module.exports = defineConfig({
    transpileDependencies: true,

    // 打包
    assetsDir: 'vue_static',
    parallel: false,
    publicPath: './',
})

