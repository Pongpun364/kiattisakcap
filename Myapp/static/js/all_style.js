$(function () {
    $(window).on('scroll', function () {
        if ( $(window).scrollTop() > 10 ) {
            $('.navbar.fixed-top').addClass('active ');
            $('.navbar.fixed-top').removeClass('bg-dark');
            $('.logopic').addClass('logo-white');
            $('.logopic').removeClass('logo');
       
        } else {
            $('.navbar.fixed-top').addClass('bg-dark ');
            $('.navbar.fixed-top').removeClass('active');
            $('.logopic').addClass('logo');
            $('.logopic').removeClass('logo-white');
        }
    });
});