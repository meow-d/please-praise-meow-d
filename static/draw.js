const canvas = document.getElementById("draw-canvas")
const ctx = canvas.getContext("2d")

const width = canvas.clientWidth
const height = canvas.clientHeight
canvas.width = Math.floor(width * devicePixelRatio)
canvas.height = Math.floor(height * devicePixelRatio)
ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0)

ctx.lineWidth = 2
ctx.lineCap = "round"
ctx.lineJoin = "round"

let prevX = null
let prevY = null
let isPainting = false

canvas.addEventListener("mousedown", (e) => {
    isPainting = true
    draw(e)
})
window.addEventListener("mouseup", () => (isPainting = false))
canvas.addEventListener("mousemove", draw)
canvas.addEventListener("mouseenter", (e) => {
    prevX = e.offsetX
    prevY = e.offsetY
})

canvas.addEventListener("touchstart", (e) => {
    e.preventDefault()
    isPainting = true
    draw(e)
})
window.addEventListener("touchend", () => {
    isPainting = false
})
canvas.addEventListener("touchmove", (e) => {
    e.preventDefault()
    draw(e)
})

function draw(e) {
    if (prevX == null || prevY == null || !isPainting) {
        prevX = e.offsetX
        prevY = e.offsetY
        return
    }

    let currentX = e.offsetX
    let currentY = e.offsetY

    ctx.beginPath()
    ctx.moveTo(prevX, prevY)
    ctx.lineTo(currentX, currentY)
    ctx.stroke()

    prevX = currentX
    prevY = currentY
}

function clearCanvas() {
    isPainting = false
    ctx.clearRect(0, 0, canvas.width, canvas.height)
}

function saveImage() {
    const dataURL = canvas.toDataURL()
    const link = document.createElement("a")
    link.href = dataURL
    link.download = "canvas.png"
    link.click()
}

function submitImage() {
    canvas.toBlob((image) => {
        const input = document.getElementById("image-input")
        const file = new File([image], "image.png", { type: "image/png" })
        const dataTransfer = new DataTransfer()
        dataTransfer.items.add(file)
        input.files = dataTransfer.files
        document.getElementById("image-form").submit()
    })
}
