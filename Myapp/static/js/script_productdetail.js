
//if add to cart btn clicked
$('.cart-btn').on('click', function (){
    // const mq = window.matchMedia( "(max-width: 575px)" );
    
    // if (mq.matches) {
    //   // window width is less than 575px
    //   /*$("").remove()*/
    // } else {
    //   // window width is at least 500px
      
    // }
    var cart = $('.cart-nav');
    console.log("script_productdetail detected !!!")
    
    // find the img of that card which button is clicked by user
  // find the img of that card which button is clicked by user
  let imgtodrag = $(".xzoom-container").find("img").eq(0);
  position = $(this).offset()
  if (imgtodrag) {
    // duplicate the img
    var imgclone = imgtodrag.clone().offset({
      top: position.top,
      left: position.left
    }).css({
        'opacity': '0.8',
        'position': 'absolute',
        'height': '150px',
        'width': '150px',
        'z-index': '1031'
      }).appendTo($('body')).animate({
        'top': cart.offset().top + 20,
        'left': cart.offset().left + 30,
        'width': 75,
        'height': 75
      }, 1000, 'easeInOutExpo');
  
  
      imgclone.animate({
        'width': 0,
        'height': 0
      }, function(){
        $(this).detach()
      });
    }
  });
  