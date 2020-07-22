const btnSubmit = document.getElementById('submit');

btnSubmit.addEventListener('click', submit);

function submit() {
    let http = new XMLHttpRequest();
    http.open("POST", "/sendmessage", true);
    http.setRequestHeader("Content-type","application/x-www-form-urlencoded");

    let name = document.getElementById("name");
    let telephone = document.getElementById("telephone");
    let email = document.getElementById("email");
    let message = document.getElementById("message");
    let honeypot = document.getElementById("address");

    if (honeypot.value.length > 0) {
        // The honeypot is only visible to robots
        alert("Stop mucking about!");
        return;
    }

    let valid = validate(name, telephone, email, message);
    if (!valid) {
        return;
    }

    btnSubmit.classList.remove('show');
    btnSubmit.classList.add('hide');

    let spinner = document.getElementById('spinner');
    spinner.classList.add('show');
    spinner.classList.remove('hide');

    let params = "name=" + name.value + "&telephone=" + telephone.value + "&email=" + email.value +
        "&message=" + message.value + "&honeypot=" + honeypot.value;

    http.send(params);
    http.onload = function() {
        spinner.classList.remove('show');
        spinner.classList.add('hide');

        let tick = document.getElementById('tick');
        tick.classList.add('show');
        tick.classList.remove('hide');
    }
}

function validate(name, telephone, email, message) {
    let regexName = /^[a-zA-Z\\s]+/;
    let regexPhone = /[0-9]{11}/;
    let regexEmail = /^\S+@\S+$/;

    let valid = true;

    let value = name.value;
    if (value == null || value === "") {
        notValid(name);
        valid = false;
    } else if (!regexName.test(value)) {
        notValid(name);
        valid = false;
    } else {
        isValid(name);
    }

    value = telephone.value;
    if (value == null || value === "") {
        notValid(telephone);
        valid = false;
    } else if (!regexPhone.test(value)) {
        notValid(telephone);
        valid = false;
    } else {
        isValid(telephone);
    }

    value = email.value;
    if (value == null || value === "") {
        notValid(email);
        valid = true;
    } else if (!regexEmail.test(value)) {
        notValid(email);
        valid = false;
    } else {
        isValid(email);
    }

    value = message.value;
    if (value == null || value === "") {
        notValid(message);
        valid = false;
    } else {
        isValid(message);
    }

    return valid;
}

function isValid(element) {
    element.parentElement.classList.remove('danger');
}

function notValid(element) {
    element.parentElement.classList.add('danger');
}