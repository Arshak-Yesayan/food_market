const profile_btn = document.querySelector("#profile-btn");
const edit_btn = document.querySelector("#edit-btn");
const container = document.querySelector(".container");

var no_edit = document.getElementById('no-edit');
var edit = document.getElementById('edit');

function editing(task) {
    if( task == 'edit' ) {
        no_edit.style.visibility = 'hidden';
        edit.style.visibility = 'visible';
    }
    else if( task == 'no_edit' ) {
        edit.style.visibility = 'hidden';
        no_edit.style.visibility = 'visible';
    }
}

edit_btn.addEventListener("click", () => {
    container.classList.add("edit-mode");
    editing('edit');
});

profile_btn.addEventListener("click", () => {
    container.classList.remove("edit-mode");
    editing('no_edit');
});

editing('no_edit');