const form = document.getElementById('form-control');
const mail = document.getElementById('email');
const password = document.getElementById('password1');
const confpass = document.getElementById('password2');

form.addEventListener('submit',function(e){
    e.preventDefault();

    checkInputs();
});

function checkInputs(){
    const mailValue=mail.value.trim();
    const passValue=password.value.trim();
    const passConfValue=confpass.value.trim();

    setSuccessFor(mail);

}

function setErrorFor(input){
    const field = input.parentElement;
    field.className = 'field-error span.fa-exclamation-circle';
}

function setSuccessFor(input){
    const field = input.parentElement;
    field.className = 'field-success span.fa-check-circle';
}