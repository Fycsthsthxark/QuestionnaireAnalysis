<script>
export default {}
</script>

<template>
    <div class="overBox">
        <div class="title">
            <h2>感谢您的参与！</h2>
        </div>
        <div class="footer">
            <el-button type="primary" @click="$router.push('/')">重新填写问卷</el-button>
            <div class="endMsg">
                <small>
                    感谢您抽出时间完成这份问卷，您的答案对于我们更好的了解ChatGPT在国内的使用情况非常有帮助。
                </small>
            </div>
        </div>
    </div>
</template>

<style scoped lang="less">
.overBox {
    padding: 15px;

    .title {
        padding-bottom: 15px;
        border-bottom: 2px solid var(--grayColor);

        h2 {
            text-align: center;
            color: var(--color);
            margin: 15px 0;
        }
    }

    .footer {
        margin-top: 35px;
        text-align: center;

        .endMsg {
            margin: 15px 0;
            font-weight: lighter;
            font-size: 12px;
        }
    }
}
</style>