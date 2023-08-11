document.addEventListener('DOMContentLoaded', function() {
    
    // Button for return
    document.querySelector('#back-button').addEventListener('click', () => {
        history.back();
    });

    
    

    
    
    const csrftoken = getCookie('csrftoken');
    // A function that handles quantity change
    const selectElements = document.querySelectorAll('.quantity-select');
    selectElements.forEach(selectElement => {
        selectElement.addEventListener('change', (event) => {
            event.preventDefault(); 
        const quantity = event.target.value;
        const productId = event.target.dataset.productId;
        const size = event.target.dataset.size;
        const color = event.target.dataset.color;
        const data = {quantity: quantity, size: size, color: color};
        fetch(`/add_to_cart/${productId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            //console.log('Success:', data);
            // update the cart total or display a message here

            var total_price = document.getElementById(`total_price_${productId}_${size}_${color}`);
            total_price.innerHTML = `EGP ${data.total}`;
            var cart_total = document.getElementById('cart_total');
            cart_total.innerHTML = `EGP ${data.cart_total_before_discount}`;
            document.getElementById('discount').innerHTML = `EGP ${data.discount}`;

            document.getElementById('cart_total_discount').innerHTML = `EGP ${data.cart_total}`;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});








if (document.querySelector('#remove-coupon-btn')) {
    
    document.querySelector('#remove-coupon-btn').addEventListener('click', removeCoupon);
}
});



//ADD to cart PUT

const csrftoken = getCookie('csrftoken');
function addToCart(productId) {
    fetch(`/add_to_cart/${productId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({quantity: 0})
    })
    .then(response => response.json())
    .then(data => {
        // find the link element
        const link = document.querySelector(`a[onclick="addToCart('${productId}')"]`);
        // create the check mark element
        const checkMark = document.createElement('span');
        checkMark.className = 'check-mark';
        checkMark.innerHTML = '✔';
        // create the text element
        const text = document.createElement('span');
        text.className = 'text';
        text.innerHTML = 'Added To Cart';
        // append the check mark and text elements to the link
        link.innerHTML = '';
        link.appendChild(checkMark);
        link.appendChild(text);
        // add the 'added' class to the link to trigger the transition effect
        link.classList.add('added');
        
        // remove the added elements, return the text inside the link to its original state, and deactivate the link after 2.5 seconds
        setTimeout(() => {
            link.innerHTML = '+ Add To Cart';
            link.classList.remove('added');
            link.style.cursor = 'default';
            link.style.textDecoration = 'none';
            link.style.color = 'white';
        }, 3000);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}




// A function to apply promo codes through a put request
function Apply_promo_function() {

    const apply_promo_button = document.getElementById('apply-promo-code')
    const input = document.querySelector('#promo_code');
    const data = { promo_code: input.value };

    fetch('/apply_coupon/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        //console.log('Success:', data);
        if (data.error != false) {
            // create error message element
    let errorMessage = document.createElement('div');
    errorMessage.id = 'error-message';
    errorMessage.textContent = data.error;
    errorMessage.style.color = 'red';

    // check if error message is already shown
    let existingErrorMessage = document.querySelector('#error-message');
    if (!existingErrorMessage) {
        // insert error message into main_coupon_div
        document.querySelector('#main_coupon_div').appendChild(errorMessage);
        
        // fade out error message when user clicks anywhere on the page
        document.addEventListener('click', () => {
            errorMessage.classList.add('fade-away');
            errorMessage.addEventListener('transitionend', () => {
                errorMessage.remove();
            });
        });
    }
        }
        else{
        document.getElementById('discount').innerHTML = `EGP ${data.discount}`;

    document.getElementById('cart_total_discount').innerHTML = `EGP ${data.cart_total}`;

    // check if coupon div already exists
    let couponDiv = document.querySelector('#coupon-div');
    if (couponDiv) {
        // update coupon div with new code
        couponDiv.innerHTML = `<p>Coupon applied: ${input.value}<button id="remove-coupon-btn" title="remove code">x</button></p>`;
    } else {
        // create and insert new coupon div
        couponDiv = document.createElement('div');
        couponDiv.id = 'coupon-div';
        couponDiv.innerHTML = `<p>Coupon applied: ${input.value}<button id="remove-coupon-btn" title="remove code">x</button></p>`;
        document.querySelector('#main_coupon_div').appendChild(couponDiv);
    }

    // apply fade-in effect to coupon div
    couponDiv.classList.add('fade-in');
    document.querySelector('#remove-coupon-btn').addEventListener('click', removeCoupon);
        }
    })
};



// Remove coupon code function
function removeCoupon() {

    fetch('/remove_coupon/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data.error) {
            // update cart total
            document.querySelector('#cart_total').textContent = data.cart_total;
            document.querySelector('#cart_total_discount').textContent = data.cart_total;
        }
        //remove the discount 
        document.getElementById('discount').innerHTML = `EGP 0.00`;
        // remove coupon div
        let couponDiv = document.querySelector('#coupon-div');
        if (couponDiv) {
        couponDiv.classList.add('fade-away');
        couponDiv.addEventListener('transitionend', () => {
            couponDiv.remove();
        });
    }
    });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function removeFromCart(event, product_id, product_size, product_color ) {
    event.preventDefault();
    // Get the value of the CSRF token
    const csrftoken = getCookie('csrftoken');
    var row = document.getElementById("x" + product_id + product_size + product_color);
    const size = row.dataset.size;
    //console.log(size);
    const color = row.dataset.color;
    // Send a PUT request to the server to remove the item from the cart
    fetch(`/cart/remove/${product_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            // Include the CSRF token as a header
            'X-CSRFToken': csrftoken, 

        },
        body: JSON.stringify({
            color: color,
            size: size
        })
    })
    .then(response => response.json())
    .then(data => {
        //console.log("success : " + data)
        // Update the page to reflect the changes
        // For example, you could update the cart total and remove the item from the cart display
    row.style.transition = "opacity 1s";
    row.style.opacity = 0;
    
    var cart_total = document.getElementById('cart_total_discount');
    cart_total.innerHTML = `EGP ${data.cart_total}`;
    
    setTimeout(function() {
        row.parentNode.removeChild(row);
    }, 1000);
        var cart_total = document.getElementById('cart_total').innerHTML = `EGP ${data.cart_total_before_discount}`;
        var cart_total = document.getElementById('discount').innerHTML = `EGP ${data.discount}`;
        var cart_summary = document.getElementById('cart_summary');
        const cart_count = cart_summary.dataset.cart;
        //console.log(data.cart_total_before_discount);
        if (data.cart_total_before_discount == '0.00') {
          cart_summary.classList.add('fade-away');
            cart_summary.addEventListener('transitionend', () => {
                cart_summary.remove();
            });
        }

    });
}

// ADD to and REMOVE from fav fucntions

function addToFavorites(product_id) {
    // Get the value of the CSRF token
    const csrftoken = getCookie('csrftoken');
    fetch('/add_to_favorites/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({product_id: product_id})
    })
    .then(response => response.json())
    .then(data => {
        //console.log('Success:', data);
        // update the cart total or display a message here
        //console.log(data);
    
        // create the alert element
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show';
        alert.role = 'alert';
        alert.innerHTML = `<strong>Success!</strong> ${data.product_name} Added to Favorites. <br> <a href="/favorites">View Favorites</a>`;
        
        // set the position, top, and z-index properties of the alert element
        alert.style.position = 'fixed';
        alert.style.top = '50px';  // adjust this value to position the alert lower on the screen
        alert.style.zIndex = 9999;  // set a high z-index value to make the alert appear on top of other elements
        
        // create the close button

        
        // append the alert to the page
        document.body.prepend(alert);
        
        // remove the alert after 10 seconds
        setTimeout(() => {
            alert.remove();
        }, 10000);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  }
  
  function removeFromFavorites(product_id) {
    // Get the value of the CSRF token
    const csrftoken = getCookie('csrftoken');
    fetch('/remove_from_favorites/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({product_id: product_id})
      
    });
    var fav = document.getElementById("x" + product_id);
    if (fav) {
        fav.classList.add('fade-away');
          fav.addEventListener('transitionend', () => {
              fav.remove();
          });
      }
  }

  document.addEventListener('DOMContentLoaded', () => {
    const heartIcons = document.querySelectorAll('.product__hover a');
    heartIcons.forEach(icon => {
      icon.addEventListener('click', event => {
        event.preventDefault();
        event.stopPropagation();
        // Handle heart icon click here
      });
    });
  });

document.addEventListener('DOMContentLoaded', function() {
      // Get the modal element
    // Get the modal element

var modal = document.getElementsByClassName('modal-body');

// Get the tabs inside the modal
var tabs = document.querySelectorAll('.sizetab');
document.querySelector('#sizechart').addEventListener('click', () => {
    var img = document.querySelector('.modal-img');
    img.src = staticUrl + "s.png";

}
)
// Use the forEach method to loop through the tabs and add an event listener for the 'click' event
tabs.forEach(function(tab) {
  tab.addEventListener('click', function(event) {
    // Get the data attribute of the clicked tab
    //console.log("clicked");
    //console.log(tabValue);
    // Get the image element inside the modal
    var img = document.querySelector('.modal-img');
    
    var tabValue = event.target.dataset.value;
    img.src = staticUrl + tabValue;

  });
});
});
window.addEventListener('scroll', function() {
    var arrowContainer = document.querySelector('.arrow-container');
    if (window.pageYOffset > 0) {
        arrowContainer.style.display = 'none';
    } else {
        arrowContainer.style.display = 'block';
    }
});