$(document).ready(function() {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
    });

    // custom call back functions
        $('.wind-submit').click(function () {
        $(".custom-success").css("display","none")
        $(".custom-loader").css("display","inline")
      //  alert("came to wind alert")
        var wind_speed = $("#wind-speed").val()
         var wind_dir = $("#wind-dir").val()
         var plant = $(".custom-plant-selecetion").val()
         var turbines = $(".custom-turbine-selection").val()
         var turbine_status = 0
         if($('input[name="custom-turbine-status"]:checked').val())
         {
            turbine_status = 1
         }
         console.log(plant)
         console.log(turbines)
         console.log(turbine_status)

        //alert(wind_speed)
        var data = {"plant":plant,"turbines":turbines.toString(),"turbine_status":turbine_status,"iot":"wind","wind_speed":wind_speed,"wind_dir":wind_dir,csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()}
        var HOME_URL = window.location.origin
                    $.ajax(
                    {
                    type:'POST',
                    data:data,
                    url: HOME_URL+"/wind_solar_data_ingestion",
                    success: function(result){
                        data = JSON.parse(result)

                        console.log(data)
                        console.log(data.data)
                        if(data.data == true)
                        {
                        $(".custom-loader").css("display","none")
                        $(".custom-success").css("display","inline")

                        }
                    }
                    });


        });

        $('.solar-submit').click(function () {
        $(".custom-success-solar").css("display","none")
        $(".custom-loader-solar").css("display","inline")

        var solar_plant = $(".custom-solar-plant-selecetion").val()
         var inverter = $(".custom-inverter-selection").val()
         var inverter_status = 0
         if($('input[name="custom-inverter-status"]:checked').val())
         {
            inverter_status = 1
         }

        var poa = $("#solar-poa").val()
         var ghi = $("#solar-ghi").val()
        var data = {"solar_plant":solar_plant,"inverters":inverter.toString(),"inverter_status":inverter_status,"iot":"solar","poa":poa,"ghi":ghi,csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()}
        var HOME_URL = window.location.origin
                    $.ajax(
                    {
                    type:'POST',
                    data:data,
                    url: HOME_URL+"/wind_solar_data_ingestion",
                    success: function(result){
                        data = JSON.parse(result)

                        console.log(data)
                        console.log(data.status)
                        if(data.data == true)
                        {
                        $(".custom-loader-solar").css("display","none")
                        $(".custom-success-solar").css("display","inline")

                        }
                    }
                    });
    });


 $(".custom-plant-selecetion").change(function(){
   var self = $(this)
   var plant = self.val()
//   alert(window.location)
//   window.href=window.location

window.location = window.location.origin+"?plant="+plant
var currentScroll = $(".scroll-pos").val();
//alert(currentScroll)
$(window).scrollTop(currentScroll);

})


 $(".custom-solar-plant-selecetion").change(function(){
   var self = $(this)
   var plant = self.val()
//   alert(window.location)
//   window.href=window.location

window.location = window.location.origin+"?solar_plant="+plant
var currentScroll = $(".scroll-pos").val();
//alert(currentScroll)
$(window).scrollTop(currentScroll);

})




//custom call back function end here
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        loop: true,
        nav: false,
        dots: true,
        items: 1,
        dotsData: true,
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            }
        }
    });


    // Portfolio isotope and filter
    var portfolioIsotope = $('.portfolio-container').isotope({
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
    });
    $('#portfolio-flters li').on('click', function () {
        $("#portfolio-flters li").removeClass('active');
        $(this).addClass('active');

        portfolioIsotope.isotope({filter: $(this).data('filter')});
    });
    
})(jQuery);

