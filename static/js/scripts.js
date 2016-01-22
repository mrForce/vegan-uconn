$(document).ready(function() {
    if ($(window).width() >= 768) {
        // hide the menu button
        $(".lines-button-wrapper").remove();
        // move the header to the correct location and center the text
        $("#top-header").css({
            "left": "250px",
            "width": "calc(100% - 250px)"
        });
    }
    if ($("#sidebar-location-select").val() == "dining_halls") {
        $("#sidebar-meal-select").parent().show();
    } else {
        $("#sidebar-meal-select").parent().hide();
    }
    // check to see if iOS mobile app
    var isiPhone = navigator.userAgent.indexOf('iPhone') != -1
    if (isiPhone && ("standalone" in window.navigator) && !window.navigator.standalone) {
        // Init modal
        $('#iOS-modal-button').show();
    }

});

// open/close the menu
$('.lines-button').click(function() {
    $(this).toggleClass("open");
    // if the sidebar was just opened
    if ($(this).hasClass("open")) {
        setTimeout(function() {
            $(".lines-button-wrapper").css("left", "250px");
            $("#top-header").css("left", "250px");
        }, 300);
    } else {
        setTimeout(function() {
            $(".lines-button-wrapper").css("left", "0");
            $("#top-header").css("left", "0");
        }, 300);
    }
    // after animating the menu button, open the sidebar
    setTimeout(function(){
        $("#wrapper").toggleClass("toggled");
    }, 300);
});
// when the menu is open, tap the page to close the menu
$('.container').click( function() {
    // if the menu is open
    if ($("#wrapper").hasClass("toggled")) {
        // close the menu
        $(".lines-button").toggleClass("open");
        setTimeout(function(){
            $("#wrapper").toggleClass("toggled");
            $(".lines-button-wrapper").css("left", "0");
            $("#top-header").css("left", "0");
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
function insertParam(key, value, url) {
    key = encodeURIComponent(key); value = encodeURIComponent(value);

    if (!url) {
        url = document.location.search;
    }
    var kvp = url.substr(1).split('&');
    if (kvp == '') {
        return '?' + key + '=' + value;
    }
    else {
        var i = kvp.length; var x; while (i--) {
            x = kvp[i].split('=');
            if (x[0] == key) {
                x[1] = value;
                kvp[i] = x.join('=');
                break;
            }
        }
        if (i < 0) { kvp[kvp.length] = [key, value].join('='); }
        return "?" + kvp.join('&');
    }
};
// Get user's location
$("#sidebar-sort-by").change(function() {
    if ($(this).val() == "distance") {
        if (navigator.geolocation) {
            try {
                navigator.geolocation.getCurrentPosition(function(position) {
                    $("#getting-location-alert").slideDown();
                    newURL = insertParam("pos", position.coords.latitude + "and" + position.coords.longitude);
                    newURL = insertParam("sort", "distance", newURL);
                    location.assign(newURL);
                });
            }
            catch(err) {
                alert("Could not get location: " + err);
            }
        } else {
            alert("Sorry, geolocation isn't supported by your browser.");
        }
    }
});
