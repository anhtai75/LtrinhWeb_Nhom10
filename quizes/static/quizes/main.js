console.log('hello world')

const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')
const url = window.location.href
modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', ()=>{
    const pk = modalBtn.getAttribute('data-pk')
    const name = modalBtn.getAttribute('data-quiz')
    const numQuestions = modalBtn.getAttribute('data-questions')
    const difficulty = modalBtn.getAttribute('data-difficulty')
    const scoreToPass = modalBtn.getAttribute('data-pass')
    const time = modalBtn.getAttribute('data-time')

    modalBody.innerHTML = `
    <div class="h5 mb-3"> Bạn đã sẵn sàng thực hiện <b>${name}</b>?</div>
    <div class="text-muted">
    <ul>
        <li>Độ Khó: <b>${difficulty}</b></li>
        <li>Số Câu Hỏi: <b>${numQuestions}</b></li>
        <li>Điểm để qua: <b>${scoreToPass}</b>%</li>
        <li>Thời Gian: <b>${time} phút</b></li>
    </ul>
    </div>
    `
    startBtn.addEventListener('click', ()=>{
        window.location.href = url + pk
    })
}))
