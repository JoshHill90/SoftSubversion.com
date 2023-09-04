
const card1 = document.getElementById('card-1');
const card2 = document.getElementById('card-2');
const card3 = document.getElementById('card-3');
const userNameList = [];
const userEmailList = [];
const goodCodeList = [];


function loginInfo() {
	card1.style.opacity = "1";
	card2.style.opacity = '0';
	card3.style.opacity = '0';
	card1.style.transform  =  "translateY(0%)";
	card2.style.transform  = "translateY(-100%)";
	card3.style.transform  = "translateY(-100%)";

};
function userInfo() {
	let loginCheck = validateLoginForm();
	if (loginCheck == false){
		return false;
	} else {
		card1.style.opacity = "0";
		card2.style.opacity = '1';
		card3.style.opacity = '0';
		card1.style.transform =  "translateY(-100%)" ;
		card2.style.transform  =  "translateY(0%)";
		card3.style.transform  =  "translateY(-100%)";
	}

};
function contactInfo() {
	card1.style.opacity = "0";
	card2.style.opacity = '0';
	card3.style.opacity = '1';
	card1.style.transform  =  "translateY(-100%)" ;
	card2.style.transform  =  "translateY(-100%)";
	card3.style.transform  =  "translateY(0%)";
};

document.addEventListener('DOMContentLoaded', function() {
	loginInfo();
});

async function fetchNameList() {
	const response = await fetch("/static/json/NameList.json");
	if (response.ok) {
		const data = await response.json();
		exportData(data);
		
		if (window.fetchedData) {
			for (let usernames in window.fetchedData['name_list']) {
				userNameList.push(usernames);	
			}
			for (let emailList in window.fetchedData['email_list']) {
				userEmailList.push(emailList);	
			}
			for (let goodKey in window.fetchedData['code_list']) {
				goodCodeList.push(goodKey);	
			}
			

		} else {
			console.log("No data available yet.");
		}
	} else {
		console.log("Error in retrieval");
	}
};

function exportData(data) {
    window.fetchedData = data;
}

function validateLoginForm() {
	
	let fUserName = document.forms["regForm"]["username"].value;
	let fPassword1 = document.forms["regForm"]["password1"].value;
	let fPassword2 = document.forms["regForm"]["password2"].value;
	let fHexKey = document.forms["regForm"]["hexkey"].value;
	for (let nameListed in userNameList) {
		if (fUserName == "" || fUserName == nameListed ) {
			alert("Name must be filled out");
			return false;
		  };
	}

	if (fPassword2 == ""|| fPassword2 != fPassword1) {
		alert("Password did not match or contain the correct charaters");
		return false;
	};
	if (fHexKey == "") {
		alert("please enter a valid Key");
		return false;
	};
	for (let goodKeys in goodCodeList) {
		if (fHexKey != goodKeys){
			alert("This key is in valid or has already been used")
		}
	}

};

function validateUserForm() {
	let fFirstName = document.forms["regForm"]["first_name"].value;
	let fLastName = document.forms["regForm"]["last_name"].value;
	let fContentMethod = document.forms["regForm"]["contact_method"].value;
	let femail = document.forms["regForm"]["email"].value;

	if (fFirstName == "") {
		alert("First name must be filled out");
		return false;
	};
	if (fLastName == "") {
		alert("Last name must be filled out");
		return false;
	};
	if (fContentMethod == "-") {
		alert("Plase make a selection");
		return false;
	};
	if (femail == "") {
		alert("please enter a valid email address")
		return false;
	};
	for (let emails in userEmailList){
		if (femail == emails){
			alert('Email already exist in this system')
		}
	}
	if (!femail.includes('@') ){
		alert('Please enter a vlaid email')
		return false;
	};

	
};

