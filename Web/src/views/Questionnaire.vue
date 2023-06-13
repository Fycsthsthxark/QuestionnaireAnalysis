<script>
import Problem from "@/components/Problem.vue";

export default {
    components: {Problem},

    data() {
        return {
            problemList: [
                {
                    number: 1,
                    title: "您的性别？",
                    answer: null,
                    required: true,
                },
                {
                    number: 2,
                    title: "您的年龄？",
                    answer: null,
                    required: true,
                },
                {
                    number: 3,
                    title: "您是否知道ChatGPT是什么？",
                    answer: null,
                    required: true,
                },
                {
                    number: 4,
                    title: "您是在哪个渠道上了解到ChatGPT的？",
                    answer: null,
                    required: true,
                },
                {
                    number: 5,
                    title: "您觉得ChatGPT在解决问题上有效性如何？",
                    answer: null,
                    required: true,
                },
                {
                    number: 6,
                    title: "您使用ChatGPT的频率是多少次/天？",
                    answer: null,
                    required: true,
                },
                {
                    number: 7,
                    title: "您在使用ChatGPT时，是否遇到过技术方面的问题？",
                    answer: null,
                    required: true,
                },
                {
                    number: 8,
                    title: "您对ChatGPT的隐私和安全问题有多担心？",
                    answer: null,
                    required: true,
                },
                {
                    number: 9,
                    title: "您的职业是？",
                    answer: null,
                    required: true,
                },
                {
                    number: 10,
                    title: "您使用ChatGPT的目的是什么？",
                    answer: null,
                    required: false,
                },
                {
                    number: 11,
                    title: "您在使用ChatGPT时，最常使用的功能是什么？",
                    answer: null,
                    required: false,
                },
                {
                    number: 12,
                    title: "如果您曾经遇到过问题/故障，请描述您的情况和解决方法。",
                    answer: null,
                    required: false,
                },
                {
                    number: 13,
                    title: "您认为ChatGPT未来的应用在哪些方面有发展潜力？",
                    answer: null,
                    required: false,
                },
                {
                    number: 14,
                    title: "您希望ChatGPT在国内开发哪些具有国内特色的功能？",
                    answer: null,
                    required: false,
                },
                {
                    number: 15,
                    title: "您认为聊天机器人在今后使用过程中，应该采取哪些措施来保障用户隐私和安全？",
                    answer: null,
                    required: false,
                }
            ]
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
        }
    }
}
</script>

<template>
    <div class="questionnaireBox">
        <div class="title">
            <h2>关于ChatGPT在国内的使用情况的调查问卷</h2>
            <small>
                尊敬的先生/女生，感谢您参与此问卷。本问卷旨在了解您对ChatGPT的态度和看法，请按您的真实想法如实填写，您的回答对我们至关重要。谢谢!</small>
        </div>
        <div class="content">
            <problem :title="problemList[0].title" :number="problemList[0].number"
                     :required="problemList[0].required">
                <template #content>
                    <el-radio v-model="problemList[0].answer" label="男">男</el-radio>
                    <el-radio v-model="problemList[0].answer" label="女">女</el-radio>
                </template>
            </problem>
            <problem :title="problemList[1].title" :number="problemList[1].number"
                     :required="problemList[1].required">
                <template #content>
                    <el-radio v-model="problemList[1].answer" label="18以下">18以下</el-radio>
                    <el-radio v-model="problemList[1].answer" label="19-25">19-25</el-radio>
                    <el-radio v-model="problemList[1].answer" label="26-35">26-35</el-radio>
                    <el-radio v-model="problemList[1].answer" label="36-45">36-45</el-radio>
                    <el-radio v-model="problemList[1].answer" label="46以上">46以上</el-radio>
                </template>
            </problem>
            <problem :title="problemList[2].title" :number="problemList[2].number"
                     :required="problemList[2].required">
                <template #content>
                    <el-radio v-model="problemList[2].answer" label="是">是</el-radio>
                    <el-radio v-model="problemList[2].answer" label="否">否</el-radio>
                </template>
            </problem>
            <problem :title="problemList[3].title" :number="problemList[3].number"
                     :required="problemList[3].required">
                <template #content>
                    <el-radio v-model="problemList[3].answer" label="社交媒体">社交媒体</el-radio>
                    <el-radio v-model="problemList[3].answer" label="新闻媒体">新闻媒体</el-radio>
                    <el-radio v-model="problemList[3].answer" label="科技论坛">科技论坛</el-radio>
                    <el-radio v-model="problemList[3].answer" label="其他">其他</el-radio>
                </template>
            </problem>
            <problem :title="problemList[4].title" :number="problemList[4].number"
                     :required="problemList[4].required">
                <template #content>
                    <el-radio v-model="problemList[4].answer" label="非常有效">非常有效</el-radio>
                    <el-radio v-model="problemList[4].answer" label="比较有效">比较有效</el-radio>
                    <el-radio v-model="problemList[4].answer" label="不太有效">不太有效</el-radio>
                    <el-radio v-model="problemList[4].answer" label="无效">无效</el-radio>
                </template>
            </problem>
            <problem :title="problemList[5].title" :number="problemList[5].number"
                     :required="problemList[5].required">
                <template #content>
                    <el-radio v-model="problemList[5].answer" label="1-3">1-3</el-radio>
                    <el-radio v-model="problemList[5].answer" label="3-6">3-6</el-radio>
                    <el-radio v-model="problemList[5].answer" label="6-9">6-9</el-radio>
                    <el-radio v-model="problemList[5].answer" label=">9">>9</el-radio>
                </template>
            </problem>
            <problem :title="problemList[6].title" :number="problemList[6].number"
                     :required="problemList[6].required">
                <template #content>
                    <el-radio v-model="problemList[6].answer" label="是">是</el-radio>
                    <el-radio v-model="problemList[6].answer" label="否">否</el-radio>
                </template>
            </problem>
            <problem :title="problemList[7].title" :number="problemList[7].number"
                     :required="problemList[7].required">
                <template #content>
                    <el-radio v-model="problemList[7].answer" label="非常担心">非常担心</el-radio>
                    <el-radio v-model="problemList[7].answer" label="担心">担心</el-radio>
                    <el-radio v-model="problemList[7].answer" label="不太担心">不太担心</el-radio>
                    <el-radio v-model="problemList[7].answer" label="不担心">不担心</el-radio>
                </template>
            </problem>
            <problem :title="problemList[8].title" :number="problemList[8].number"
                     :required="problemList[8].required">
                <template #content>
                    <el-input type="text" v-model="problemList[8].answer"></el-input>
                </template>
            </problem>
            <problem :title="problemList[9].title" :number="problemList[9].number"
                     :required="problemList[9].required">
                <template #content>
                    <el-input type="textarea" v-model="problemList[9].answer"></el-input>
                </template>
            </problem>
            <problem :title="problemList[10].title" :number="problemList[10].number"
                     :required="problemList[10].required">
                <template #content>
                    <el-input type="textarea" v-model="problemList[10].answer"></el-input>
                </template>
            </problem>
            <problem :title="problemList[11].title" :number="problemList[11].number"
                     :required="problemList[11].required">
                <template #content>
                    <el-input type="textarea" v-model="problemList[11].answer"></el-input>
                </template>
            </problem>
            <problem :title="problemList[12].title" :number="problemList[12].number"
                     :required="problemList[12].required">
                <template #content>
                    <el-input type="textarea" v-model="problemList[12].answer"></el-input>
                </template>
            </problem>
            <problem :title="problemList[13].title" :number="problemList[13].number"
                     :required="problemList[13].required">
                <template #content>
                    <el-input type="textarea" v-model="problemList[13].answer"></el-input>
                </template>
            </problem>
            <problem :title="problemList[14].title" :number="problemList[14].number"
                     :required="problemList[14].required">
                <template #content>
                    <el-input type="textarea" v-model="problemList[14].answer"></el-input>
                </template>
            </problem>
        </div>
        <div class="footer">
            <el-button type="primary" @click="submit">提交</el-button>
            <div class="endMsg">
                <small>
                    感谢您抽出时间完成这份问卷，您的答案对于我们更好的了解ChatGPT在国内的使用情况非常有帮助。
                </small>
            </div>
        </div>
    </div>
</template>

<style scoped lang="less">
.questionnaireBox {
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

    .content {
        margin: 0 15px;
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