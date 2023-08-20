const site = document.getElementById('sites').dataset.value;
const client = document.getElementById('clients').dataset.value;
const prints = document.getElementById('prints').dataset.value;
const total = document.getElementById('total').dataset.value;

var y2Values = [parseInt(site), parseInt(client), parseInt(prints)];

    
new Chart("BreakDown", {
	type: "doughnut",
	data: {
	  labels: ["Site", "Client", "Prints"],
	  datasets: [
		{
		  backgroundColor: ["#7933FC", "#B6FC33", "#33FCDD"],
		  data: y2Values,
		},
	  ],
	},
	options: {
	  elements: {
		arc: {
		  borderWidth: 0, 
		},
	  },
	  cutout: "80%",
	  plugins: {
		legend: {
		  display: false,
		},
	  },
	},
});

var y1Values = [20000 - parseInt(total), parseInt(total)];

    
new Chart("Totals", {
type: "doughnut",
data: {
		labels: ["Remaining Storage","Total Stored"],
		datasets: [{
			backgroundColor: ["#7933FC", "#B6FC33"],
			data: y1Values
		}]
	},
	options: {
		elements: {
		  arc: {
			borderWidth: 0, 
		  },
		},
		cutout: "80%",
		plugins: {
		  legend: {
			display: false,
		  },
		},
	},
});

