const templatesData = JSON.parse(document.getElementById('templates-data').textContent);

function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    section.style.display = section.style.display === "none" ? "grid" : "none";
}

function openModal(id) {
    window.currentTemplateId = id;

    const data = templatesData.find(t => t.id === id);
    if (!data) return;

    document.getElementById("modal-title").innerText = data.name;
    document.getElementById("modal-description").innerText = data.description || "No description.";

    const exercisesHTML = data.exercises?.map(ex =>
        `<div class="exercise-item">
            <strong>${ex.sets} x ${ex.name}</strong><br>
            <small>${ex.primary_muscle || 'No muscle specified'}</small>
        </div>`
    ).join('') || "<p>No exercises defined.</p>";

    document.getElementById("modal-exercises").innerHTML = exercisesHTML;
    document.getElementById("template-modal").style.display = "flex";
}

function closeModal() {
    document.getElementById("template-modal").style.display = "none";
}

function startWorkout() {
    closeModal();
    const templateId = window.currentTemplateId;
    if (!templateId) {
        alert("No workout selected!");
        return;
    }
    window.location.href = `/start/${templateId}/`;
}