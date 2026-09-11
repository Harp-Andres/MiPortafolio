
document.addEventListener("DOMContentLoaded", () => {
    var dob = "19930405";
    var year = Number(dob.substr(0, 4));
    var month = Number(dob.substr(4, 2)) - 1;
    var day = Number(dob.substr(6, 2));
    var today = new Date();
    var age = today.getFullYear() - year;
    if (
        today.getMonth() < month ||
        (today.getMonth() == month && today.getDate() < day)
    ) {
        age--;
    }
    let Variable = document.getElementById("edad");
    Variable.textContent = age + " Años";
});