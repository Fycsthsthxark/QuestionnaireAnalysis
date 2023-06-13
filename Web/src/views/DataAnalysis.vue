<script>
import Problem from "@/components/Problem.vue";
import dateUtil from "../utils/js/dateUtil";

export default {
    computed: {
        dateUtil() {
            return dateUtil
        }
    },
    components: {Problem},

    data() {
        return {
            problemList: [
                {
                    number: 1,
                    title: "您的性别？",
                    answer: "",
                    required: true,
                },
                {
                    number: 2,
                    title: "您的年龄？",
                    answer: "",
                    required: true,
                },
                {
                    number: 3,
                    title: "您是否知道ChatGPT是什么？",
                    answer: "",
                    required: true,
                },
                {
                    number: 4,
                    title: "您是在哪个渠道上了解到ChatGPT的？",
                    answer: "",
                    required: true,
                },
                {
                    number: 5,
                    title: "您觉得ChatGPT在解决问题上有效性如何？",
                    answer: "",
                    required: true,
                },
                {
                    number: 6,
                    title: "您使用ChatGPT的频率是多少次/天？",
                    answer: "",
                    required: true,
                },
                {
                    number: 7,
                    title: "您在使用ChatGPT时，是否遇到过技术方面的问题？",
                    answer: "",
                    required: true,
                },
                {
                    number: 8,
                    title: "您对ChatGPT的隐私和安全问题有多担心？",
                    answer: "",
                    required: true,
                },
                {
                    number: 9,
                    title: "您的职业是？",
                    answer: "",
                    required: true,
                },
                {
                    number: 10,
                    title: "您使用ChatGPT的目的是什么？",
                    answer: "",
                    required: false,
                },
                {
                    number: 11,
                    title: "您在使用ChatGPT时，最常使用的功能是什么？",
                    answer: "",
                    required: false,
                },
                {
                    number: 12,
                    title: "如果您曾经遇到过问题/故障，请描述您的情况和解决方法。",
                    answer: "",
                    required: false,
                },
                {
                    number: 13,
                    title: "您认为ChatGPT未来的应用在哪些方面有发展潜力？",
                    answer: "",
                    required: false,
                },
                {
                    number: 14,
                    title: "您希望ChatGPT在国内开发哪些具有国内特色的功能？",
                    answer: "",
                    required: false,
                },
                {
                    number: 15,
                    title: "您认为聊天机器人在今后使用过程中，应该采取哪些措施来保障用户隐私和安全？",
                    answer: "",
                    required: false,
                }
            ],
            count: 0,
            loading: false
        }
    },

    methods: {
        submit() {
            const access = this.problemList.filter(problem => problem.required).every(problem => problem.answer)
            if (!access) {
                return this.$message({
                    message: "请将问卷内容填写完整",
                    type: 'warning'
                })
            }

            this.request.post("/submit/", {
                problemList: this.problemList
            }).then((response) => {
                const status = response["status"] === 200

                if (status) {
                    this.$router.push("/over")
                }
            })
        },

        getCount() {
            this.request.post("/getCount/", {}).then((response) => {
                const status = response["status"] === 200

                if (status) {
                    this.count = response["data"]["count"]
                }
            })
        },

        getDataAnalysis() {
            this.loading = true
            this.request.post("/getDataAnalysis/", {
                problemList: this.problemList
            }).then((response) => {
                const status = response["status"] === 200

                if (status) {
                    this.problemList = response["data"]["problemList"]
                }
                this.loading = false
            })
        }
    },

    mounted() {
        this.getCount()
        this.getDataAnalysis()
    }
}
</script>

<template>
    <div class="dataAnalysisBox">
        <div class="title">
            <h2>《关于ChatGPT在国内的使用情况的调查问卷》数据分析结果</h2>
            <small>截止{{
                    dateUtil.formatTimeStampToYYMMDD(dateUtil.dateToTimeStampString(new Date()))
                }}，此问卷共收集了【{{ count }}】份结果</small>
        </div>
        <div class="content" v-loading="loading">
            <problem :title="problemList[0].title" :number="problemList[0].number"
                     :required="problemList[0].required">
                <template #content>
                    <el-image :src="problemList[0].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[1].title" :number="problemList[1].number"
                     :required="problemList[1].required">
                <template #content>
                    <el-image :src="problemList[1].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[2].title" :number="problemList[2].number"
                     :required="problemList[2].required">
                <template #content>
                    <el-image :src="problemList[2].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[3].title" :number="problemList[3].number"
                     :required="problemList[3].required">
                <template #content>
                    <el-image :src="problemList[3].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[4].title" :number="problemList[4].number"
                     :required="problemList[4].required">
                <template #content>
                    <el-image :src="problemList[4].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[5].title" :number="problemList[5].number"
                     :required="problemList[5].required">
                <template #content>
                    <el-image :src="problemList[5].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[6].title" :number="problemList[6].number"
                     :required="problemList[6].required">
                <template #content>
                    <el-image :src="problemList[6].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[7].title" :number="problemList[7].number"
                     :required="problemList[7].required">
                <template #content>
                    <el-image :src="problemList[7].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[8].title" :number="problemList[8].number"
                     :required="problemList[8].required">
                <template #content>
                    <el-image :src="problemList[8].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[9].title" :number="problemList[9].number"
                     :required="problemList[9].required">
                <template #content>
                    <el-image :src="problemList[9].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[10].title" :number="problemList[10].number"
                     :required="problemList[10].required">
                <template #content>
                    <el-image :src="problemList[10].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[11].title" :number="problemList[11].number"
                     :required="problemList[11].required">
                <template #content>
                    <el-image :src="problemList[11].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[12].title" :number="problemList[12].number"
                     :required="problemList[12].required">
                <template #content>
                    <el-image :src="problemList[12].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[13].title" :number="problemList[13].number"
                     :required="problemList[13].required">
                <template #content>
                    <el-image :src="problemList[13].answer"></el-image>
                </template>
            </problem>
            <problem :title="problemList[14].title" :number="problemList[14].number"
                     :required="problemList[14].required">
                <template #content>
                    <el-image :src="problemList[14].answer"></el-image>
                </template>
            </problem>
        </div>
    </div>
</template>

<style scoped lang="less">
.dataAnalysisBox {
    padding: 15px;

    .title {
        height: 16vh;
        padding-bottom: 15px;
        border-bottom: 2px solid var(--grayColor);

        h2 {
            text-align: center;
            color: var(--color);
            margin: 15px 0;
        }
    }

    .content {
        height: calc(84vh - 30px);
        margin: 0 15px;
        overflow-y: scroll;
    }
}
</style>