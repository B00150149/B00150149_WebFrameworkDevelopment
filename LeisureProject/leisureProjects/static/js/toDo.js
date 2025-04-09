function addTask() {
    const input = document.getElementById("todo-input");
    const task = input.value.trim();
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (task !== "") {
        fetch('/create-todo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `title=${encodeURIComponent(task)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
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
        })
        .catch(error => console.error('Error:', error));
    }
}
