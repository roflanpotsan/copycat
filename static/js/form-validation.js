function validateTextBox(id) {
    form = document.getElementById(id);

    if (!form.checkValidity() || form.value === ''){
        form.required = true;
        form.setAttribute("class", "form-control is-invalid");
        block = document.getElementById("error-box");
        block.style.display = "block";
    }
    else{
        form.setAttribute("class", "form-control is-valid");
    }
}