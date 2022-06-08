//Usename Validation

const usernameField = document.querySelector('#usernameField');
const usernameFeedbackArea = document.querySelector('.usernameFeedbackArea');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');

const emailField = document.querySelector('#emailField');
const emailFeedbackArea = document.querySelector('.emailFeedbackArea');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');

const showPasswordToggle = document.querySelector('.showPasswordToggle');
const newPasswordField = document.querySelector('#newPasswordField');
const newPasswordRepeatField = document.querySelector('#newPasswordRepeatField');

const submitBtn = document.querySelector('.submitBtn'); //Getting the submit button to disable it when an error occurs

usernameField.addEventListener('keyup', (e) => {
	const usernameVal = e.target.value;
	
	// Showing that we are checking the username - for slow internets
	usernameSuccessOutput.textContent = `Checking ${usernameVal}.`;
	usernameSuccessOutput.style.display = 'block';


	//using Fetch API to request Python services 
	if(usernameVal.length > 0){
		fetch('/authentication/validate_username', {
			body: JSON.stringify({ username: usernameVal }),
			method: "POST",

		})
		.then((res) => res.json())
		.then((data) =>{
			//console.log('data ', data);
			if(data.username_error){ //If returned a username error (says that exists), here we call it as a good thing

                if(!emailField.classList.contains('is-invalid')){ //IF the email field is invalid do not remove atribute
					submitBtn.removeAttribute("disabled");
				}

				usernameField.classList.remove('is-invalid');
				usernameField.classList.add('is-valid');

				usernameFeedbackArea.style.display = 'none';

				usernameSuccessOutput.textContent = `'${usernameVal}' is a valid username.`;	
			} 
			else{ // If does not exists, show that is valid
                submitBtn.disabled = true;

				usernameSuccessOutput.style.display = 'none'; // When an error appears, hide the sucess output message

				usernameField.classList.remove('is-valid');
				usernameField.classList.add('is-invalid'); //Adding bootstrap class 'invalid'
				usernameFeedbackArea.style.display = 'block'; 
				usernameFeedbackArea.innerHTML = `<p>'${usernameVal}' does not exists in our database.</p>`; //Show error message
			}
		});

	}
	else{ // If the form field is empty, just clear the errors
		usernameField.classList.remove('is-invalid');
		usernameField.classList.remove('is-valid');

		usernameFeedbackArea.style.display = 'none';

		usernameSuccessOutput.style.display = 'none';	
	}
	
});

//Email Validation

emailField.addEventListener('keyup', (e) => {
	const emailVal = e.target.value;
	
	// Showing that we are checking the username - for slow internets
	emailSuccessOutput.textContent = `Checking ${emailVal}`;
	emailSuccessOutput.style.display = 'block';

	
	if(emailVal.length > 0){
		fetch('/authentication/validate_email', {
			body: JSON.stringify({ email: emailVal }),
			method: "POST",

		})
		.then((res) => res.json())
		.then((data) => {
			
			if(data.email_error){ //If returned a email error

                if(data.status_code === 409){ //if the error says that the email exists
                    if(!usernameField.classList.contains('is-invalid')){ //IF the username field is invalid do not remove atribute
                        submitBtn.removeAttribute("disabled");
                    }
    
                    emailField.classList.remove('is-invalid');
                    emailField.classList.add('is-valid'); //Adding bootstrap class 'valid'
    
                    emailFeedbackArea.style.display = 'none';
                    emailSuccessOutput.textContent = `'${emailVal}' is a valid email.`;
                }
                else{
                    submitBtn.disabled = true;

                    emailSuccessOutput.style.display = 'none'; // When an error appears, hide the sucess output message
    
                    emailField.classList.remove('is-valid');
                    emailField.classList.add('is-invalid'); //Adding bootstrap class 'invalid'
    
                    emailFeedbackArea.style.display = 'block';
                    emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`; //Show error message
                }
			}
			else{ // If theres no error, show thats valid
                submitBtn.disabled = true;

				emailSuccessOutput.style.display = 'none'; // When an error appears, hide the sucess output message

				emailField.classList.remove('is-valid');
				emailField.classList.add('is-invalid'); //Adding bootstrap class 'invalid'

				emailFeedbackArea.style.display = 'block';
				emailFeedbackArea.innerHTML = `'${emailVal}' does not exist in our database`; //Show error message
			}
		});
	}
	else{ // If the form field is empty, just clear the errors
		emailField.classList.remove('is-invalid');
		emailField.classList.remove('is-valid');

		emailFeedbackArea.style.display = 'none';

		emailSuccessOutput.style.display = 'none';
	}
});


const handlePasswordToggleInput = (e) => {
	if(showPasswordToggle.textContent === "SHOW"){
		showPasswordToggle.textContent = "HIDE";
		newPasswordField.setAttribute('type', 'text');
        newPasswordRepeatField.setAttribute('type', 'text');
	} 
	else{
		showPasswordToggle.textContent = "SHOW";
		newPasswordField.setAttribute('type', 'password');
        newPasswordRepeatField.setAttribute('type', 'password');
	}
	
};

showPasswordToggle.addEventListener('click', handlePasswordToggleInput);