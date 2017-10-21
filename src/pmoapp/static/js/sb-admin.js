(function($) {
  "use strict"; // Start of use strict

  // Configure tooltips for collapsed side navigation
  $('.navbar-sidenav [data-toggle="tooltip"]').tooltip({
    template: '<div class="tooltip navbar-sidenav-tooltip" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>'
  })

  // Toggle the side navigation
  $("#sidenavToggler").click(function(e) {
    e.preventDefault();
    $("body").toggleClass("sidenav-toggled");
    $(".navbar-sidenav .nav-link-collapse").addClass("collapsed");
    $(".navbar-sidenav .sidenav-second-level, .navbar-sidenav .sidenav-third-level").removeClass("show");
  });

  // Force the toggled class to be removed when a collapsible nav link is clicked
  $(".navbar-sidenav .nav-link-collapse").click(function(e) {
    e.preventDefault();
    $("body").removeClass("sidenav-toggled");
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .navbar-sidenav, body.fixed-nav .sidenav-toggler, body.fixed-nav .navbar-collapse').on('mousewheel DOMMouseScroll', function(e) {
    var e0 = e.originalEvent,
      delta = e0.wheelDelta || -e0.detail;
    this.scrollTop += (delta < 0 ? 1 : -1) * 30;
    e.preventDefault();
  });

  // Scroll to top button appear
  $(document).scroll(function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Configure tooltips globally
  $('[data-toggle="tooltip"]').tooltip()

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(event) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    event.preventDefault();
  });

  // Call the dataTables jQuery plugin
  $(document).ready(function() {
    $('#dataTable').DataTable();
  });

})(jQuery); // End of use strict

// Chart.js scripts
// -- Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// !Report collapse panel Deputy PM
var reportPanelDPM = document.getElementById('reportPanelDPM');
function whatClicked1(evt) { //Change arrow
      $(".panel-collapse#filterPanelDPM").on("hide.bs.collapse", function () {
        $("#panelArrowDPM").removeClass("fa-chevron-down").addClass("fa-chevron-right");
		//$(".card-header").find("#tickCross1").removeClass("fa-times-circle").addClass("fa-check-square"); //CODE HERE TEMPORARY, CHANGE RED CROSS TO GREEN TICK to be used in checking if textarea #DeputyPMtxt is empty 
    });

    $(".panel-collapse#filterPanelDPM").on("show.bs.collapse", function () {
        $("#panelArrowDPM").removeClass("fa-chevron-right").addClass("fa-chevron-down");
		//$(".card-header").find("#tickCross1").removeClass("fa-check-square").addClass("fa-times-circle"); //CODE HERE TEMPORARY, CHANGE GREEN TICK TO RED CROSS to be used in checking if textarea #DeputyPMtxt is empty 
    });
}
reportPanelDPM.addEventListener("click", whatClicked1, false);

// !Report collapse panel MOFA
var reportPanelMOFA = document.getElementById('reportPanelMOFA');
function whatClicked2(evt) { //Change arrow
      $(".panel-collapse#filterPanelMOFA").on("hide.bs.collapse", function () {
        $("#panelArrowMOFA").removeClass("fa-chevron-down").addClass("fa-chevron-right");
    });

    $(".panel-collapse#filterPanelMOFA").on("show.bs.collapse", function () {
        $("#panelArrowMOFA").removeClass("fa-chevron-right").addClass("fa-chevron-down");
    });
}
reportPanelMOFA.addEventListener("click", whatClicked2, false);

// !Report collapse panel MOHA
var reportPanelMOHA = document.getElementById('reportPanelMOHA');
function whatClicked3(evt) { //Change arrow
      $(".panel-collapse#filterPanelMOHA").on("hide.bs.collapse", function () {
        $("#panelArrowMOHA").removeClass("fa-chevron-down").addClass("fa-chevron-right");
    });

    $(".panel-collapse#filterPanelMOHA").on("show.bs.collapse", function () {
        $("#panelArrowMOHA").removeClass("fa-chevron-right").addClass("fa-chevron-down");
    });
}
reportPanelMOHA.addEventListener("click", whatClicked3, false);

// !Report collapse panel MDEF
var reportPanelMDEF = document.getElementById('reportPanelMDEF');
function whatClicked4(evt) { //Change arrow
      $(".panel-collapse#filterPanelMDEF").on("hide.bs.collapse", function () {
        $("#panelArrowMDEF").removeClass("fa-chevron-down").addClass("fa-chevron-right");
    });

    $(".panel-collapse#filterPanelMDEF").on("show.bs.collapse", function () {
        $("#panelArrowMDEF").removeClass("fa-chevron-right").addClass("fa-chevron-down");
    });
}
reportPanelMDEF.addEventListener("click", whatClicked4, false);

// !Report collapse panel PM
var reportPanelPM = document.getElementById('reportPanelPM');
function whatClicked5(evt) { //Change arrow
      $(".panel-collapse#filterPanelPM").on("hide.bs.collapse", function () {
        $("#panelArrowPM").removeClass("fa-chevron-down").addClass("fa-chevron-right");
    });

    $(".panel-collapse#filterPanelPM").on("show.bs.collapse", function () {
        $("#panelArrowPM").removeClass("fa-chevron-right").addClass("fa-chevron-down");
    });
}
reportPanelPM.addEventListener("click", whatClicked5, false);


