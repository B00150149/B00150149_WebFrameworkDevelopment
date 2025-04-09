function addTask() {
    const input = document.getElementById("todo-input");
    const task = input.value.trim();

    if (task !== "") {
        const list = document.getElementById("todo-list");

        const li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between align-items-center";
        li.innerHTML = `
            ${task}
            <button class="btn btn-sm btn-danger" onclick="this.parentElement.remove()">✕</button>
        `;

        list.appendChild(li);
        input.value = "";
    }
}
