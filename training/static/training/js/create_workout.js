const allExercises = JSON.parse(document.getElementById("exercises-data").textContent);

function openCreateTemplateModal() {
    document.getElementById("create-template-modal").style.display = "flex";
}

function closeCreateTemplateModal() {
    document.getElementById("create-template-modal").style.display = "none";
}

function createTemplate() {
    const name = document.getElementById("new-template-name").value.trim();
    const description = document.getElementById("new-template-description").value.trim();

    if (!name) {
        alert("Please enter a template name.");
        return;
    }

    fetch("/api/create_template/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken'),  // make sure to include CSRF token
        },
        body: JSON.stringify({ name, description, exercise_ids: selectedExerciseIds }),
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            // Close modal
            closeCreateTemplateModal();

            // Optionally reset input fields
            document.getElementById("new-template-name").value = "";
            document.getElementById("new-template-description").value = "";
            selectedExerciseIds = [];

            // Update the templates list on the page
            addNewTemplateToDOM(data.template);

        } else {
            alert("Error: " + (data.error || "Unknown error"));
        }
    })
    .catch(err => alert("Request failed: " + err));
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

// Helper function to get CSRF cookie (you may already have this)
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
