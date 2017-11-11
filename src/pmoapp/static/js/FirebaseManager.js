var app = angular.module('chatApp', ['firebase']);
//Only for PMO - CMO
app.controller('ChatController', function($scope, $firebaseArray) {
	
	var d = new Date();
	var today = d.getDate()+d.getMonth()+d.getYear();
	var txt = document.getElementById('txtFBMsgs'); //store id of textbox

	//Query
	
    var ref = firebase.database().ref().child(channel).child('CMO-PMO');
	
    $scope.fbmessages = $firebaseArray(ref);

    $scope.send = function() {
        if (txt.value != ""){	//check if textbox contains any message
            $scope.fbmessages.$add({
                sender: sender,
                message: $scope.messageText,
                date: Date.now()
            })

            txt.value = ""; //reset value of textbox
        }
    }
})
