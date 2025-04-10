// Load todos when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadTodos();
});

function loadTodos() {
    fetch('/todos/')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById("todo-list");
            list.innerHTML = '';
            data.todos.forEach(todo => {
                addTodoToDOM(todo);
            });
        });
}

//to add to do on backend from the form
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
                addTodoToDOM({
                    id: data.id,
                    title: task,
                    completed: false
                });
                input.value = "";
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function addTodoToDOM(todo) {
    const list = document.getElementById("todo-list");
    const li = document.createElement("li");
    li.className = `list-group-item d-flex justify-content-between align-items-center ${todo.completed ? 'completed' : ''}`;
    li.dataset.id = todo.id;
    
    li.innerHTML = `
        <div class="form-check">
            <input type="checkbox" class="form-check-input" ${todo.completed ? 'checked' : ''} 
                   onchange="toggleTodoCompletion(${todo.id})">
            <label class="form-check-label ${todo.completed ? 'text-decoration-line-through' : ''}">
                ${todo.title}
            </label>
        </div>
        <button class="btn btn-sm btn-danger" onclick="deleteTodo(${todo.id})">✕</button>
    `;
    list.appendChild(li);
}

function deleteTodo(todoId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(`/todos/${todoId}/delete/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.querySelector(`li[data-id="${todoId}"]`).remove();
        }
    })
    .catch(error => console.error('Error:', error));
}

function toggleTodoCompletion(todoId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(`/todos/${todoId}/toggle/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const todoItem = document.querySelector(`li[data-id="${todoId}"]`);
            todoItem.classList.toggle('completed');
            const label = todoItem.querySelector('.form-check-label');
            label.classList.toggle('text-decoration-line-through');
        }
    })
    .catch(error => console.error('Error:', error));
}
