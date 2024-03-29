function create_ul(items, prefix_link=0) {
    if (0 === prefix_link) {f = (x => x)}
    else if (1 === prefix_link){f = (x => `<a href=${x[1]}">${x[0]}</a>`)}
    else {
        f = function (x) {
          return ""
            + `${x[0]} <div align="right"><button href="${x[1]}" onclick="redirect_to('${x[1]}')" align="left">`
            + `Записаться на приём от ${x[2]}р.</button>`
            + `<button type="button" align="left" onclick="react_on_doctor_button('${x[3]}', '${x[0]}')">`
            +`Обратиться в чате</button> <div id='${x[0]}' hidden>`
            + `<p>${x[3]}</p> <a>Здравствуйте! Чем я могу Вам помочь?</a></div></div>`
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

function build_block(parent_id, title, items, foot, prefix_link=0){
    diag = document.getElementById(parent_id);
    // diag.innerHtml = '';
    diag.innerHTML = `<div><header><h1>${title}</h1><p>${foot || ""}</p></header></div>`.trim();
    ul = document.createElement('ul');
    diag.firstChild.appendChild(create_ul(items, prefix_link));
    diag.hidden = false;
}

function hide(items, is_hidden){
    items.forEach(function (item) {
        item.hidden = is_hidden;
    })
}

hide(["medicine", "chatroom", "diagnosis"], true);

function uniq_arr(arr, field){
    dct = Object();
    arr.forEach(
        function (item) {
            dct[item[field]] = item
        }
    );
    return Object.values(dct)
}

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
        uniq_arr(result.map(x => x['doctors']).flat(1), 0),
        "",
        2
    );
    build_block(
        "medicine",
        "Рекомендуем вам лекарства *",
        result.map(x => x['treatments']).flat(1),
        "* информация только для ознакомления и не является рекомендацией врача",
        1,
    );
    window.location.href = '#diagnosis';
}

function react_on_doctor_button(name, spec){
    el = document.getElementById(spec);
    el.hidden = ! el.hidden;
    // alert(`<header>${name}</header><p>${spec}</p> <a>Здравствуйте! Чем я могу Вам помочь?</a>>`);
}

function redirect_to(href){
    window.location.href = href;
}
