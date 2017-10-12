// !Report collapse panel Deputy PM
var reportPanel1 = document.getElementById('reportPanel1');
function whatClicked1(evt) { //Change arrow
      $(".panel-collapse#filterPanel1").on("hide.bs.collapse", function () {
        $("#panelArrow1").removeClass("fa-chevron-down").addClass("fa-chevron-right");
		//$(".card-header").find("#tickCross1").removeClass("fa-times-circle").addClass("fa-check-square"); //CODE HERE TEMPORARY, CHANGE RED CROSS TO GREEN TICK to be used in checking if textarea #DeputyPMtxt is empty 
    });

    $(".panel-collapse#filterPanel1").on("show.bs.collapse", function () {
        $("#panelArrow1").removeClass("fa-chevron-right").addClass("fa-chevron-down");
		//$(".card-header").find("#tickCross1").removeClass("fa-check-square").addClass("fa-times-circle"); //CODE HERE TEMPORARY, CHANGE GREEN TICK TO RED CROSS to be used in checking if textarea #DeputyPMtxt is empty 
    });
}
reportPanel1.addEventListener("click", whatClicked1, false);

// !Report collapse panel MOFA
var reportPanel2 = document.getElementById('reportPanel2');
function whatClicked2(evt) { //Change arrow
      $(".panel-collapse#filterPanel2").on("hide.bs.collapse", function () {
        $("#panelArrow2").removeClass("fa-chevron-down").addClass("fa-chevron-right"); 
    });

    $(".panel-collapse#filterPanel2").on("show.bs.collapse", function () {
        $("#panelArrow2").removeClass("fa-chevron-right").addClass("fa-chevron-down"); 
    });
}
reportPanel2.addEventListener("click", whatClicked2, false);

// !Report collapse panel MOHA
var reportPanel3 = document.getElementById('reportPanel3');
function whatClicked3(evt) { //Change arrow
      $(".panel-collapse#filterPanel3").on("hide.bs.collapse", function () {
        $("#panelArrow3").removeClass("fa-chevron-down").addClass("fa-chevron-right"); 
    });

    $(".panel-collapse#filterPanel3").on("show.bs.collapse", function () {
        $("#panelArrow3").removeClass("fa-chevron-right").addClass("fa-chevron-down"); 
    });
}
reportPanel3.addEventListener("click", whatClicked3, false);

// !Report collapse panel MINDEF
var reportPanel4 = document.getElementById('reportPanel4');
function whatClicked4(evt) { //Change arrow
      $(".panel-collapse#filterPanel4").on("hide.bs.collapse", function () {
        $("#panelArrow4").removeClass("fa-chevron-down").addClass("fa-chevron-right"); 
    });

    $(".panel-collapse#filterPanel4").on("show.bs.collapse", function () {
        $("#panelArrow4").removeClass("fa-chevron-right").addClass("fa-chevron-down"); 
    });
}
reportPanel4.addEventListener("click", whatClicked4, false);

// !Report collapse panel PM
var reportPanel5 = document.getElementById('reportPanel5');
function whatClicked5(evt) { //Change arrow
      $(".panel-collapse#filterPanel5").on("hide.bs.collapse", function () {
        $("#panelArrow5").removeClass("fa-chevron-down").addClass("fa-chevron-right"); 
    });

    $(".panel-collapse#filterPanel5").on("show.bs.collapse", function () {
        $("#panelArrow5").removeClass("fa-chevron-right").addClass("fa-chevron-down"); 
    });
}
reportPanel5.addEventListener("click", whatClicked5, false);


