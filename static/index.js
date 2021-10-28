

function getMessage() {
    let xhr = new XMLHttpRequest();
    let mes = document.getElementById("message").value;
    let dial = document.getElementById("dial");
    let label = document.createElement('label');
    label.innerHTML = `<label>Вы:${mes}</label>`;
    dial.append(label);
    let form = new FormData();
    form.append("mes", mes);
    xhr.open("POST", "http://127.0.0.1:5000/chat");
    xhr.send(form);

    xhr.onload = function () {
        js = JSON.parse(xhr.response)
        if (js["ans"] == undefined) {
            res.innerHTML = js["error"]
        } else {
            let label2 = document.createElement('label');
            label2.innerHTML = `<label>Бот:${js["ans"]}</label>`;
            dial.append(label2);
        }
    }
    
}