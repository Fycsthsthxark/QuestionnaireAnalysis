import $ from 'jquery'

// 时间戳转Date实例
function timeStampToDate(timeStamp) {
    return new Date(parseInt(timeStamp))
}

// Date实例转时间戳
function dateToTimeStampString(date) {
    return Date.parse(date).toString()
}

// 判断两个时间戳是否在同一天
function twoTimeStampIsSameDay(oneTimeStamp, twoTimeStamp) {
    return timeStampToDate(oneTimeStamp).toDateString() === timeStampToDate(twoTimeStamp).toDateString()
}

// 判断两个时间戳的HH:mm时间是否一致
function twoTimeStampHHmmIsSame(oneTimeStamp, twoTimeStamp) {
    const oneDate = timeStampToDate(oneTimeStamp)
    const twoDate = timeStampToDate(twoTimeStamp)
    return oneDate.getHours() === twoDate.getHours() && oneDate.getMinutes() === twoDate.getMinutes()
}

// 判断timeStamp是否在规定时间内
function isStartDateTimeStampBetweenEndDateTimeStamp(startDateTimeStamp, timeStamp, endDateTimeStamp) {
    return timeStamp >= startDateTimeStamp && timeStamp <= endDateTimeStamp
}

// 将时间戳格式化时间为HH:mm格式
function formatTimeStampToHHmm(timeStamp) {
    const date = timeStampToDate(timeStamp)
    return date.getHours().toString().padStart(2, '0') + ":" + date.getMinutes().toString().padStart(2, '0')
}

// 将时间戳格式化时间为YY-MM-DD格式
function formatTimeStampToYYMMDD(timeStamp) {
    const date = timeStampToDate(timeStamp)
    return `${date.getFullYear().toString()}.${(timeStampToDate(timeStamp).getMonth() + 1).toString().padStart(2, '0')}.${date.getDate().toString().padStart(2, '0')}`
}


// 抛出
export default {
    timeStampToDate,
    dateToTimeStampString,
    twoTimeStampIsSameDay,
    twoTimeStampHHmmIsSame,
    formatTimeStampToYYMMDD,
    isStartDateTimeStampBetweenEndDateTimeStamp,
    formatTimeStampToHHmm,
}
