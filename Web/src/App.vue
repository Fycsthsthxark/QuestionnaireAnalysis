<template>
    <div id="app">
        <router-view></router-view>
    </div>
</template>


<script>

export default {
    name: 'App',
    data() {
        return {
            timers: [],
        }
    },

    mounted() {
        this.timers.push(
            setInterval(() => {
                // 渲染按钮点击样式事件
                this.$public.btnFocusBind()
            }, 500)
        )
    },

    beforeDestroy() {
        for (const timer of this.timers) {
            if (timer) clearInterval(timer)
        }
    }
}
</script>

<style lang="less" scoped>

</style>
