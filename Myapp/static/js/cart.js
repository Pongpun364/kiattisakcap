var updateBtns = document.getElementsByClassName('addto-cart')


for(var i = 0; i < updateBtns.length; i++){
updateBtns[i].addEventListener('click',function(e){
    console.log("Click ...")
  
    var productid = $(this).siblings().val()
    // var action = this.dataset.action
    console.log('previousElementSibling:',productid)
    console.log('USER: ', user)
    if ( user === 'AnonymousUser'){
        addcookieItem(productid)
        htmx.trigger(htmx.find("#anonymous-add"), "Updated")
   
    }
   
})
}





function addcookieItem(productid){
    console.log('not loged in ...')
    /*cart = {
        1:{'quantity':5},
        9:{'quantity':2},
        8:{'quantity':4},
        7:{'quantity':5},
        2:{'quantity':5},
      } */
    if(cart[productid] == undefined ){
        cart[productid] = {'quantity': 1}
    }else{
        cart[productid]['quantity'] += 1
    }
    
    console.log('cart' ,cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain;path=/'
    
}


// function addcookieItem(productid,action){
//     console.log('not loged in ...')
//     /*cart = {
//         1:{'quantity':5},
//         9:{'quantity':2},
//         8:{'quantity':4},
//         7:{'quantity':5},
//         2:{'quantity':5},
//       } */

//     if (action == 'add'){
//         if(cart[productid] == undefined ){
//             cart[productid] = {'quantity': 1}
//         }else{
//             cart[productid]['quantity'] += 1
//         }
//     }

//     if (action == 'remove'){

//         cart[productid]['quantity'] -= 1       
//         if(cart[productid]['quantity'] <= 0){
//             console.log('remove item')
//             delete cart[productid]
//         }
            
//     }
    
    
    
//     console.log('cart' ,cart)
//     document.cookie = 'cart=' + JSON.stringify(cart) + ';domain;path=/'
//     location.reload()

// }

















// function updateCart(productid,action){
//     console.log(' user is logged in, sending data ...')

//     var url = '/updatecart/'

//     fetch(url,{
//         method: 'POST',
//         headers:{
//             'Content-Type':'application/json',
//             'X-CSRFToken':csrftoken,

//         },
//         body: JSON.stringify({'productid': productid, 'action': action})
//     }).then((response)=> {
//         return response.json()
//     }).then((data)=> {
//         console.log(data);
//     })


//     let myDiv = document.getElementById('idf')
//     var url = '/mycart/'


//     fetch(url)
//     .then((response)=> {
//         console.log("response success")
//         return response.text();

//     }).then((data)=>{
        
//         var parser = new DOMParser();
//         var doc = parser.parseFromString(data, 'text/html');
//         var target = doc.querySelector('#idf');
//         console.log(target)
//         myDiv.innerHTML = target.innerHTML;
        
//         htmx.process(document.body);
        
     
       
//     })



    // .then((response)=> {
    //     return response.json()
    // })
    // .then((data)=> {
    //     location.reload()
    // })

// };

// console.log('data: ',data)

// console.log('Hello World')