let updateItemBtns = document.querySelectorAll("#updateItem");

let checkoutBtn = document.querySelector("#checkout-button");

updateItemBtns.forEach((btn) => {
  btn.addEventListener("click", updateCart);
});
 checkoutBtn.addEventListener("click", checkoutCart)

function updateCart(e) {
  e.preventDefault();
  let product_id = this.dataset.product;
  let action = this.dataset.action;
  let url = "/add/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ product: product_id, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data", data);
      items = document.querySelectorAll("#num_of_items");
      items.forEach((item) => {
        item.innerText = data;
      });
    })
    .catch((err) => {
      console.log(err);
    });
}

function checkoutCart(e){
    e.preventDefault()
    
}