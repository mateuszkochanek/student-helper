var courseId = 0;

function showEditGradeView(pk) {
    courseId = pk;
    var div = document.getElementById('editGradeDiv')
    const visibility = div.style.visibility;
    div.style.visibility = (visibility === "visible" ? 'hidden' : "visible");
}

function saveNewGrade() {
    const newGrade = document.getElementById('newGrade');

    if (parseFloat(newGrade.value) && newGrade.value > 0) {
        if (document.location.href.substring(document.location.href.length - 9) === 'avgGrade/') {
            document.location.href += courseId + "/" + newGrade.value;
        } else {
            document.location.href = document.location.href.split("avgGrade")[0] + "avgGrade/" + courseId + "/" + newGrade.value;
        }
    }
}
