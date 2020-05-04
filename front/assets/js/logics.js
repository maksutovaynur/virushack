function build_ul(items, parent_id, title){
    diag = document.getElementById(parent_id);
    dv = document.createElement('div');
    hdr = document.createElement('h1');
    hdr.textContent = title;
    ul = document.createElement('ul');
    items.forEach(function (item) {
        let li = document.createElement('li');
        ul.appendChild(li);
        li.innerHTML += item;
    });
    diag.innerHTML = '';

    diag.appendChild(dv);
    dv.appendChild(hdr);
    dv.appendChild(ul);
}



async function VIVA_find_function(event){
    text = document.getElementById('complaint-text').value;
    let response = await fetch(
        `/api/diseases?text=${text}`
    );
    if (!response.ok) return;
    let result = (await response.json())["result"];

    build_ul(result.map(x => x['disease']), "diagnosis", "Вероятные диагнозы:");
    build_ul(
        result.map(x => x['doctor']),
        "chatroom",
        "Вам стоит отбратиться к следующим специалистам:");


}
