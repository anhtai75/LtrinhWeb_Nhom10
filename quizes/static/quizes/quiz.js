console.log("hello world quiz")
const url = window.location.href

const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
let data
let timer = null
const timerBox = document.getElementById('timer-box')
let submitted = false
const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60

    // 🔹 Khi Submit, bộ đếm dừng ngay lập tức
    const stopTimer = () => {
        if (timer) {
            clearInterval(timer)
            timer = null
            timerBox.innerHTML = "<b>00:00</b>"
        }
    }

    // 🚀 Thêm EventListener trực tiếp trong Timer
    quizForm.addEventListener('submit', (e) => {
        stopTimer()
        e.preventDefault()
        if (!submitted) {
            submitted = true
            sendData()
        }
        return;
    })

    timer = setInterval(() => {
        if (submitted) {
            stopTimer()
            return
        }

        seconds--
        if (seconds < 0) {
            seconds = 59
            minutes--
        }

        const displayMinutes = minutes.toString().padStart(2, '0')
        const displaySeconds = seconds.toString().padStart(2, '0')

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`

        if (minutes === 0 && seconds === 0) {
            stopTimer()
            if (!submitted) {
                submitted = true
                alert('Đã hết giờ làm bài')
                sendData()
            }
        }
    }, 1800)
}

// 🟢 Nhận dữ liệu từ Server
$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response) {
        const data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)) {
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer => {
                    quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `
                })
            }
        })
        activateTimer(response.time)
    },
    error: function(error) {
        console.log(error)
    }
})

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = { 'csrfmiddlewaretoken': csrf[0].value }

    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response) {
            quizForm.classList.add('not-visible')

            scoreBox.innerHTML = `${response.passed ? 'Chúc mừng bạn!!! ' : 'Bạn trượt mất rồi :( '}Điểm của bạn là ${response.score.toFixed(1)}/10`

            response.results.forEach(res => {
                const resDiv = document.createElement("div")
                const qsuestion = res.question
                const answer = res.answered
                const correct = res.correct_answer

                resDiv.classList.add('container', 'p-3', 'text-light', 'h6')
                resDiv.innerHTML += `<b>${question}</b>`

                if (answer === null) {
                    resDiv.classList.add('bg-danger')
                    resDiv.innerHTML += ' - Chưa trả lời'
                } else if (answer === correct) {
                    resDiv.classList.add('bg-success')
                    resDiv.innerHTML += ` | Đã Trả Lời: ${answer}`
                } else {
                    resDiv.classList.add('bg-danger')
                    resDiv.innerHTML += ` | Câu trả lời đúng: ${correct}`
                    resDiv.innerHTML += ` | Đã Trả Lời: ${answer}`
                }

                resultBox.append(resDiv)
            })
        },
        error: function(error) {
            console.log(error)
        }
    })
}