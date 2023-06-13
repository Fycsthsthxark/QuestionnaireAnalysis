<script>
export default {
    props: {
        number: {
            type: Number,
            required: true,
        },
        title: {
            type: String,
            required: true,
        },
        required: {
            type: Boolean,
            default: false
        }
    }
}
</script>

<template>
    <div class="problemBox">
        <div class="title">
            <span class="required" v-if="required">*</span>
            {{ number }}. {{ title }}
        </div>
        <div class="content">
            <slot name="content">

            </slot>
        </div>
    </div>
</template>

<style scoped lang="less">
.problemBox {
    * {
        font-size: 14px;
    }

    margin: 25px 0;

    .title {
        font-weight: bold;
        position: relative;

        .required {
            color: red;
            position: absolute;
            left: -8px;
        }
    }

    .content {
        margin: 10px 15px;
    }
}
</style>