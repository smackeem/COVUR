let updateItemBtns = document.querySelectorAll('#updateItem')

let removeBtn = document.querySelectorAll('#remove')

updateItemBtns.forEach((btn)=>{
    btn.addEventListener("click", updateCart)
})

function updateCart(e){
    e.preventDefault()
    let product_id = this.dataset.product
    let action = this.dataset.action
    if(user == 'AnonymousUser'){
        console.log('Anon')
    }else{
        let url = '/add/'
        fetch(url,
        {method: 'POST',
    headers:{
        'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken},
        body: JSON.stringify({'product': product_id, 'action': action})
    }).then((response) => {
        return response.json()
    }).then((data)=>{
        console.log('data', data)
        items = document.querySelectorAll('#num_of_items')
        items.forEach((item)=>{
            item.innerText = data
        })
    }).catch((err)=>{
        console.log(err)
    })
    }
}

