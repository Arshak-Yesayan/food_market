
const profile_btn = document.querySelector("#profile-btn");
const edit_btn = document.querySelector("#edit-btn");
const container = document.querySelector(".container");

edit_btn.addEventListener("click", () => {
  container.classList.add("edit-mode");
});

profile_btn.addEventListener("click", () => {
  container.classList.remove("edit-mode");
});