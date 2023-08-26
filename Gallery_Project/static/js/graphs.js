

const site = document.getElementById('sites').dataset.value;
const client = document.getElementById('clients').dataset.value;
const prints = document.getElementById('prints').dataset.value;
const total = document.getElementById('total').dataset.value;

const clientNameList = [];
const clientcountList = [];

var y2Values = [parseInt(site), parseInt(client), parseInt(prints)];
var y1Values = [20000 - parseInt(total), parseInt(total)];

fetch("/static/json/clientData.json", {
	methiod: "GET"
})
	.then(response  => {
		if (response .ok) {
			return response.json();
		} else {
			console.log("Error in retrieval");
		}
	})
	.then(data => {
		exportData(data);
		
		if (window.fetchedData) {
			for (const id in window.fetchedData) {
                const clientId = window.fetchedData[id];
                const clientName = clientId.name;
				clientNameList.push(clientName);
                const clientCount = clientId.count;
				clientcountList.push(clientCount);
                
                console.log(`Name: ${clientName}, Count: ${clientCount}`);
			}
        } else {
            console.log("No data available yet.");
        }
	})
    .catch(error => {
        console.log("ERROR:", error);
	});

function exportData(data) {
	window.fetchedData = data;
};

    
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


new Chart('clientImageChart1', {
    type: 'bar',
    data: {
      labels: clientNameList,
      datasets: [{
        label: '# of Votes',
        data: clientcountList,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });