const allExercises = JSON.parse(document.getElementById("exercises-data").textContent);

function openCreateTemplateModal() {
    document.getElementById("create-template-modal").style.display = "flex";
}

function closeCreateTemplateModal() {
    document.getElementById("create-template-modal").style.display = "none";
}

function createTemplate() {
    const name = document.getElementById("new-template-name").value;
    const description = document.getElementById("new-template-description").value;

    const exercises = [];
    document.querySelectorAll("#selected-exercises .exercise-item").forEach(editor => {
        const exerciseId = parseInt(editor.dataset.exerciseId);
        const sets = [];

        editor.querySelectorAll(".set-row").forEach(row => {
            const inputs = row.querySelectorAll("input");
            const kg = parseFloat(inputs[0].value) || 0;
            const reps = parseInt(inputs[1].value) || 0;
            const rest = inputs[2].value || "00:00";  // mm:ss

            sets.push({ kg, reps, rest });
        });

        exercises.push({ exerciseId: exerciseId, sets });
    });

    const payload = {
        name,
        description,
        exercises,
    };

    const csrftoken = getCookie('csrftoken');

    fetch("api/create_template/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(payload),
    })
    .then(res => res.json())
    .then(data => {
        console.log("Response from API:", data);
        if(data.success) {
            alert("Template created!");
            location.reload();
        } else {
            alert("Error: " + (data.error || "Unknown error"));
        }
    })
    .catch(err => {
        console.error("Fetch error:", err);
        alert("Request failed.");
    });
}


// Helper to add a new template card dynamically
function addNewTemplateToDOM(template) {
    const container = document.getElementById("my-templates");

    // Create new template element (match your existing HTML structure)
    const div = document.createElement("div");
    div.className = "template-item";
    div.style.cursor = "pointer";
    div.onclick = () => openModal(template.id);
    div.innerHTML = `<strong>${template.name}</strong><br>${template.description}`;

    // Append to container
    container.appendChild(div);

    // Find the "My Templates" header by text content without using :contains
    const headers = document.querySelectorAll('h3');
    const countEl = Array.from(headers).find(h3 => h3.textContent.trim().startsWith("My Templates"));

    if (countEl) {
        // Extract current count number using regex
        const currentCountMatch = countEl.textContent.match(/\d+/);
        const currentCount = currentCountMatch ? parseInt(currentCountMatch[0]) : 0;
        // Update the count in the header text
        countEl.textContent = `My Templates (${currentCount + 1})`;
    }
}

// Generic cookie getter (Django-recommended)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
