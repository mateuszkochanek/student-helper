var courseId = 0;
var editType = "";

function showEditGradeView(pk) {
    editType = "grade";
    showEditView(pk);
}

function showEditECTSView(pk) {
    editType = "ects";
    showEditView(pk);
}

function showEditView(pk) {
    courseId = pk;
    var div = document.getElementById('editDiv');
    div.style.visibility = "visible";
}

function save() {
    const newValue = document.getElementById('newValue');
    if (isValueCorrect(newValue.value) && areVariablesSet())
        changePath(newValue.value);
}

function isValueCorrect(newValue) {
    if (newValue.length <= 0)
        return false;
    if (editType === "grade" && !isNaN(newValue) && newValue >= 0)
        return true;
    if (editType === "ects" && Number.isInteger(Number(newValue)) && newValue >= 0)
        return true;
    return false;
}

function areVariablesSet() {
    return Number.isInteger(Number(courseId)) && courseId > 0 && (editType === "grade" || editType === "ects")
}

function changePath(newValue) {
    if (isPathClear()) {
        setNewPath(newValue);
    } else {
        clearAndSetNewPath(newValue);
    }
}

function isPathClear() {
    return document.location.href.substring(document.location.href.length - 9) === 'avgGrade/';
}

function setNewPath(newValue) {
    document.location.href += editType + "/" + courseId + "/" + newValue;
}

function clearAndSetNewPath(newValue) {
    document.location.href =
        document.location.href.split("avgGrade")[0]
        + "avgGrade/"
        + editType
        + "/"
        + courseId
        + "/"
        + newValue;
}

function cancel() {
    courseId = 0;
    editType = "";
    document.getElementById('editDiv').style.visibility = "hidden";
    document.getElementById('newValue').value = "";
}
