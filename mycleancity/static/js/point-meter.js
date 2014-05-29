$(function(){  
	var clean_creds = parseInt($("#point-meter #clean-creds").html());

	// 75px = 250 Clean Creds
	height = 0;

	if (clean_creds <= 250)
	{
		var difference = 75;
		var max = 250;

		var divisor = parseFloat(max/difference).toFixed(4);
		console.log(divisor);

		height = clean_creds/divisor;
	}
	else if (clean_creds <= 1000)
	{
		var difference = 67;
		var max = 1000;

		var divisor = parseFloat(max/difference).toFixed(4);
		
		height = clean_creds/divisor;
		height += difference;
	}
	else if (clean_creds <= 3000)
	{
		var difference = 67;
		var max = 3000;

		var divisor = parseFloat(max/difference).toFixed(4);
		
		height = clean_creds/divisor;
		height += (difference + 75);
	}
	else if (clean_creds <= 5000)
	{
		var difference = 67;
		var max = 5000;

		var divisor = parseFloat(max/difference).toFixed(4);
		
		height = clean_creds/divisor;
		height += (difference + 140);
	}
	else if (clean_creds <= 10000)
	{
		var difference = 67;
		var max = 10000;

		var divisor = parseFloat(max/difference).toFixed(4);
		
		height = clean_creds/divisor;
		height += (difference + 208);
	}
	else if (clean_creds <= 15000)
	{
		var difference = 67;
		var max = 15000;

		var divisor = parseFloat(max/difference).toFixed(4);
		
		height = clean_creds/divisor;
		height += (difference + 285);
	}
	else if (clean_creds > 15000)
	{
		height = 419
	}

	$("#point-meter .meter-filling").animate({
		height: height
	}, 2000);
});