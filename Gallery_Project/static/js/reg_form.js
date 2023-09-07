
const card1 = document.getElementById('card-1');
const card2 = document.getElementById('card-2');
const card3 = document.getElementById('card-3');
//-------------------------------------------------------------------------
function loginInfo() {
	moveCards(card1, card2, card3);

};
//
function userInfo() {
	validateLoginForm().then ((isValid) => {
		if (isValid){
			moveCards(card2, card1, card3);
		}
	}
)};
//
function userInfo2() {
	moveCards(card2, card1, card3);
};
//
function contactInfo() {
	validateUserForm().then ((isValid) => {
		if (isValid){
			moveCards(card3, card1, card2);
		}
	}
)};
//-------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function() {
	loginInfo();
});
//-------------------------------------------------------------------------
function moveCards (cardA, cardB, cardC) {
	cardA.style.opacity = "1";
	cardB.style.opacity = '0';
	cardC.style.opacity = '0';
	cardA.style.transform  =  "translateY(0%)";
	cardB.style.transform  = "translateY(-100%)";
	cardC.style.transform  = "translateY(-100%)";
}
//-------------------------------------------------------------------------
async function validateLoginForm() {
	const response = await fetch("/static/json/NameList.json");
        
	if (response.ok) {
		const data = await response.json();
		const userNameList = data[0].name_list;
		const goodCodeList = data[1].code_list;
		let fUserName = document.forms["regForm"]["username"].value;
		let fPassword1 = document.forms["regForm"]["password1"].value;
		let fPassword2 = document.forms["regForm"]["password2"].value;
		let fHexKey = document.forms["regForm"]["hexkey"].value;
		console.log(userNameList, goodCodeList)


		if (fUserName == "") {
			alert("Please enter a user name")
			return false;
		};

		for (let nameListed of userNameList) {
			if (fUserName == nameListed ) {
				alert("UserName already exist");
				return false;
				};
		};

		if (fPassword2 == "" || fPassword2 != fPassword1) {
			alert("Password did not match or contain the correct charaters");
			return false;
		};
	
		if (fHexKey == "") {
			alert("please enter a valid Key");
			return false;
		};
	
		for (let goodKeys of goodCodeList) {
			console.log(goodKeys)
			if (fHexKey != goodKeys){
				alert("This key is in valid or has already been used")
				return false;
			};
		};
		return true;
	} else {
		console.log("Error in retrieval");
	}
};
//
async function validateUserForm() {
	const response = await fetch("/static/json/NameList.json");
        
	if (response.ok) {
		const data = await response.json();
		const userEmailList = data[2].email_list;
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
		for (let emails of userEmailList){
			if (femail == emails){
				alert('Email already exist in this system')
				return false;
			}
		}
		if (!femail.includes('@') ){
			alert('Please enter a vlaid email')
			return false;
		};
		return true;
	} else {
		console.log("Error in retrieval");
	}
};
//-------------------------------------------------------------------------

