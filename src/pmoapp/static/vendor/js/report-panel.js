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


