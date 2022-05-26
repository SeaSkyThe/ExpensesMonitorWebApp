const usernameField = document.querySelector('#usernameField')
const feedbackArea = document.querySelector('.invalid_feedback')
usernameField.addEventListener('keyup', (e) => {
	const usernameVal = e.target.value;
	


	//using Fetch API to request Python services 
	if(usernameVal.length > 0){
		fetch('/authentication/validate_username', {
			body: JSON.stringify({ username: usernameVal }),
			method: "POST",

		})
		.then((res) => res.json())
		.then((data) =>{
			console.log('data ', data);
			if(data.username_error){ //If returned a user_name error
				usernameField.classList.add('is-invalid'); //Adding bootstrap class 'invalid'
				feedbackArea.style.display = 'block'; 
				feedbackArea.innerHTML = `<p>${data.username_error}</p>`; //Show error message

			}
			else{
				usernameField.classList.remove('is-invalid');
				feedbackArea.style.display = 'none';
			}
		});

	}
	


});