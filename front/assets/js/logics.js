function create_ul(items, prefix_link=0) {
    if (0 === prefix_link) {f = (x => x)}
    else if (1 === prefix_link){f = (x => `<a href=${x[1]}">${x[0]}</a>`)}
    else {
        f = function (x) {
          return `${x[0]} <button href="${x[1]}" onclick="redirect_to('${x[1]}')">Записаться на приём от ${x[2]}р.`
              + '</button><button type="button" onclick="react_on_doctor_button(event)">Обратиться в чате</button>'
        }
        }
    let ul = document.createElement('ul');
    items.forEach(function (item) {
        let li = document.createElement('li');
        ul.appendChild(li);
        li.innerHTML += f(item);
    });
    return ul;
}

function build_block(parent_id, title, items, foot){
    diag = document.getElementById(parent_id);
    // diag.innerHtml = '';
    diag.innerHTML = `<div><header><h1>${title}</h1><p>${foot || ""}</p></header></div>`.trim();
    ul = document.createElement('ul');
    diag.firstChild.appendChild(create_ul(items));
    diag.hidden = false;
}

function hide(items, is_hidden){
    items.forEach(function (item) {
        item.hidden = is_hidden;
    })
}

hide(["medicine", "chatroom", "diagnosis"], true);

async function VIVA_find_function(event){
    text = document.getElementById('complaint-text').value;
    let response = await fetch(
        `/api/diseases?text=${text}`
    );
    if (!response.ok) return;
    let result = (await response.json())["result"];

    build_block(
        "diagnosis",
        "Вероятные диагнозы:",
        result.map(x => x['disease'])
    );
    build_block(
        "chatroom",
        "Вам стоит отбратиться к следующим специалистам:",
        result.map(x => create_ul(x['doctors'], 2).innerHTML),
    );
    build_block(
        "medicine",
        "Рекомендуем вам лекарства *",
        result.map(x => create_ul(x['treatments'], 1).innerHTML), //<strong>${x['disease']}</strong>
        "* информация только для ознакомления и не является рекомендацией врача"
    );
    window.location.href = '#diagnosis';
}

function react_on_doctor_button(event){

}

function redirect_to(href){
    window.location.href = href;
}
