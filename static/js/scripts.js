function copyToClipboard() {
    var copyText = document.getElementById("promptTextarea");
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices

    navigator.clipboard.writeText(copyText.value)
        .then(() => {
            alert("Prompt copied to clipboard!");
        })
        .catch(err => {
            alert("Failed to copy prompt.");
        });
}

// Function to update the preamble when the prompt type changes
function updatePreamble() {
    var promptTypeSelect = document.getElementById("prompt_type");
    var preambleTextarea = document.getElementById("preamble_edit");
    var selectedPromptType = promptTypeSelect.value;

    if (selectedPromptType in prompts) {
        var preamble = prompts[selectedPromptType]['preamble'];
        preambleTextarea.value = preamble;
    } else {
        preambleTextarea.value = '';
    }
}

// Autocomplete for Programming Language
const languageInput = document.getElementById('language');
const suggestions = document.getElementById('language-suggestions');

languageInput.addEventListener('input', function() {
    const query = this.value.toLowerCase();
    suggestions.innerHTML = '';
    if (query.length > 0) {
        const matches = languages.filter(lang => lang.toLowerCase().includes(query));
        matches.forEach(match => {
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');
            listItem.textContent = match;
            listItem.addEventListener('click', function() {
                languageInput.value = match;
                suggestions.innerHTML = '';
            });
            suggestions.appendChild(listItem);
        });
    }
});

document.addEventListener('click', function(event) {
    if (!languageInput.contains(event.target)) {
        suggestions.innerHTML = '';
    }
});

document.addEventListener('DOMContentLoaded', function() {
    updatePreamble();
});
