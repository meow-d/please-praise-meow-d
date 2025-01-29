const canvas = document.getElementById("draw-canvas")

const ctx = canvas.getContext("2d")
ctx.lineWidth = 4
ctx.lineCap = 'round'

let prevX = null
let prevY = null
let isPainting = false

window.addEventListener("mouseup", (e) => isPainting = false)
canvas.addEventListener("mousedown", (e) => {
    isPainting = true
    draw(e)
})
canvas.addEventListener("mousemove", draw)

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
        const input = document.getElementById("image-input");
        const file = new File([image], "image.png", { type: "image/png" });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        input.files = dataTransfer.files;
        document.getElementById("image-form").submit();
    })
}
