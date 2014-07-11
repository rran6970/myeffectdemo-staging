$(function(){  
	$("#white-box.challenge-participants table tr td.name").on("click", showEmergencyNumber);
});

function showEmergencyNumber(e)
{
	var cell_clicked = $(this);
	cell_clicked.find("#emergency-number").show();
}