import $ from 'jquery'


/*
设置按钮点击动画
*/

// 按钮样式恢复
function btnBlur(ele) {
    ele = $(ele)
    setTimeout(() => $(ele).removeClass("btnActive"), 50)
}

// 为所有.btnFocus的元素绑定动画事件
function btnFocusBind() {
    document.querySelectorAll(".btnFocus").forEach(ele => {
        ele.onmousedown = function () {
            $(this).addClass("btnActive")
        }

        ele.onmouseup = function () {
            btnBlur(this)
        }

        ele.ontouchstart = function () {
            $(this).addClass("btnActive")
        }

        ele.ontouchcancel = function () {
            btnBlur(this)
        }

        ele.ontouchend = function () {
            btnBlur(this)
        }
    })
}

// 按钮防抖
function bottomDisableOrAllow(ele, msg, disable = false) {
    ele = $(ele)
    ele.val(msg)
    ele.text(msg)
    ele.attr("disabled", disable)
    let isDisable = disable ? "opacity(50%)" : "none"
    ele.css("filter", isDisable)
}


// 图片压缩
function cutImage(file, max_size, quality = 1) {
    /*  图片压缩
        返回Promise，调用需要前缀await
        file: File对象
        max_size: 压缩后最大的字节数
        quality: 压缩后的图片质量，递归使用，无需传入
    */
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    return new Promise((resolve) => {
        const img = new Image()
        const url = window.URL || window.webkitURL
        img.src = url.createObjectURL(file)
        img.onload = function () {
            canvas.width = this.width
            canvas.height = this.height
            ctx.drawImage(img, 0, 0, this.width, this.height)
            canvas.toBlob((cutBlob) => {
                if (cutBlob.size > max_size && quality > 0) resolve(cutImage(new File([cutBlob], file.name.split(".").shift() + ".jpeg", {type: "image/jpeg"}), max_size, quality - 0.1))
                else resolve(new File([cutBlob], file.name.split(".").shift() + ".jpeg", {type: "image/jpeg"}))
            }, file.type, quality)
        }
    })
}


// 抛出
export default {
    btnFocusBind,
    bottomDisableOrAllow,
    cutImage,
}
