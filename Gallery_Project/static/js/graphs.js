const clientNameList = [];
const clientcountList = [];
var y2Values = [];
var y1Values = [];

async function fetchDataAndCreateCharts() {
    try {
        const response = await fetch("/static/json/clientData.json");
        if (response.ok) {
            const data = await response.json();
            exportData(data);
            
            if (window.fetchedData) {
                for (const id in window.fetchedData['clientImageList']) {
                    const clientId = window.fetchedData.clientImageList[id];
                    const clientName = clientId.clientsName;
                    clientNameList.push(clientName);
                    const clientCount = clientId.clientsCount;
                    clientcountList.push(clientCount);
                }
                const prints = window.fetchedData.print_Image_data.printImageCount;
                const site = window.fetchedData.site_Image_data.siteImageCount;
                const client = window.fetchedData.client_Image_data.clientImageCount;
                const total = window.fetchedData.total_Image_data.totalImageCount;
                y2Values.push(site, client, prints);
                y1Values.push(20000 - total, total);
				
                createCharts();
            } else {
                console.log("No data available yet.");
            }
        } else {
            console.log("Error in retrieval");
        }
    } catch (error) {
        console.log("ERROR:", error);
    }
}

function exportData(data) {
    window.fetchedData = data;
}

function createCharts() {
    
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
			  display: true,
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
				display: true,
			  },
			},
		},
	});
	
	
	new Chart('clientImageChart1', {
		type: 'bar',
		data: {
		  labels: clientNameList,
		  datasets: [{
			label: 'Number of Client images',
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
	breakdownChart.update();
	totalsChart.update();
	clientImageChart.update();
}

fetchDataAndCreateCharts();
