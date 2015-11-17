$(document).ready(function() {
    if ($(window).width() >= 768) {
        // hide the menu button
        $(".lines-button-wrapper").remove();
    }
    if ($("#sidebar-location-select").val() == "dining_halls") {
        $("#sidebar-meal-select").parent().show();
    } else {
        $("#sidebar-meal-select").parent().hide();
    }
    /*
    // Init iScroll
    var myScroll;
    setTimeout(function() {
        myScroll = new IScroll('#scrollWrapper', {
            probeType: 3,
            mouseWheel: true,
            tap: true,
            scrollbars: true,
            bounce: true
        });
    }, 300);
    // Init feedify
    $(function() {
        $('.feedify').feedify();
    });
    */
    // Init hideseek
    $('#search').hideseek({
        highlight: true,
        ignore: ".ignore",
    });
    // check to see if iOS mobile app
    /*
    var isiPhone = navigator.userAgent.indexOf('iPhone') != -1
    if (isiPhone && ("standalone" in window.navigator) && !window.navigator.standalone) {
        // Init modal
        $('#iOSModal').modal({ show: false});
        // Show it
        $('#iOSModal').modal('show');
    }
    */
});

// open/close the menu
$('.lines-button').on('tap', function() {
    e.preventDefault();
    $(this).toggleClass("open");
    // if the sidebar was just opened
    if ($(this).hasClass("open")) {
        setTimeout(function() {
            $(".lines-button-wrapper").css("left", "250px");
        }, 300);
    } else {
        setTimeout(function() {
            $(".lines-button-wrapper").css("left", "15px");
        }, 300);
    }
    // after animating the menu button, open the sidebar
    setTimeout(function(){
        $("#wrapper").toggleClass("toggled");
    }, 300);
});
// when the menu is open, tap the page to close the menu
$('.container').on('tap', function() {
    // if the menu is open
    if ($("#wrapper").hasClass("toggled")) {
        // close the menu
        $(".lines-button").toggleClass("open");
        setTimeout(function(){
            $("#wrapper").toggleClass("toggled");
            $(".lines-button-wrapper").css("left", "15px");
        }, 300);
    }
});

// Don't show breakfast/lunch/dinner/late night selection when looking at
// dining halls
$("#sidebar-location-select").change(function () {
    if ($(this).val() == "dining_halls") {
        $("#sidebar-meal-select").parent().slideDown();
    } else {
        $("#sidebar-meal-select").parent().slideUp();
    }
});

// On search input
$('#search').bind('input', function() {
    var value = $(this).val();
    // If there's a search query, use hideseek hidden mode and hide
    // location names and padding
    if (value.length == 1) {
        $('#search').hideseek({
            highlight: true,
            ignore: ".ignore",
            hidden_mode: true
        });
        $(".feedify-item-header").hide();
        $(".feedify-item-body").css({
            "padding-bottom": "0",
            "border-bottom": "none"
        });
    }
    if (value.length >= 1 && value != "Search") {
        // if something is found, show the location name
        setTimeout(function(){
            $(".feedify-item-body").each(function() {
                if ($(this).children("li:visible").length > 0) {
                    $(this).closest(".feedify-item").children(".feedify-item-header").slideDown();
                }
            });
            $(".feedify-item-body").each(function() {
                if ($(this).children("li:visible").length == 0) {
                    $(this).closest(".feedify-item").children(".feedify-item-header").slideUp();
                }
            });
        }, 600);
    } else {
        // if there's no search query, show everything again
        $('#search').hideseek({
            highlight: true,
            ignore: ".ignore",
            hidden_mode: false
        });
        $(".feedify-item-header").show();
        $(".feedify-item-body").css({
            "padding-bottom": "20px",
            "border-bottom": "1px solid #ccc"
        });
        $(".feedify-item-body > li").show();
    }
});
