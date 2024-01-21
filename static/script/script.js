let updateItemBtns = document.querySelectorAll("#updateItem");

updateItemBtns.forEach((btn) => {
  btn.addEventListener("click", updateCart);
});

document.querySelectorAll('.alert .close').forEach(function(closeButton) {
  closeButton.addEventListener('click', function() {
    var alert = this.closest('.alert');
    if (alert) {
      alert.classList.add('d-none');
    }
  });
});

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
      if(data.page == 'cart'){
        location.reload()

      }else{
        items = document.querySelectorAll("#num_of_items");
        items.forEach((item) => {
          item.innerText = data.items;
        });

      }
    })
    .catch((err) => {
      console.log(err);
    });
}