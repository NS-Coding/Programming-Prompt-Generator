function copyToClipboard() {
    var copyText = document.getElementById("promptTextarea");

    // Create a temporary textarea element
    var textarea = document.createElement("textarea");
    textarea.value = copyText.value;
    // Prevent scrolling to the bottom of the page
    textarea.style.position = "fixed";
    textarea.style.top = 0;
    textarea.style.left = 0;
    textarea.style.width = "2em";
    textarea.style.height = "2em";
    textarea.style.padding = 0;
    textarea.style.border = "none";
    textarea.style.outline = "none";
    textarea.style.boxShadow = "none";
    textarea.style.background = "transparent";

    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();

    try {
        var successful = document.execCommand('copy');
        if (successful) {
            alert("Prompt copied to clipboard!");
        } else {
            alert("Failed to copy prompt.");
        }
    } catch (err) {
        alert("Failed to copy prompt.");
        console.error('Copy to clipboard failed:', err);
    }

    document.body.removeChild(textarea);
}

function downloadPrompt() {
    var promptText = document.getElementById("promptTextarea").value;
    var blob = new Blob([promptText], { type: "text/plain;charset=utf-8" });
    var url = URL.createObjectURL(blob);

    var a = document.createElement("a");
    a.href = url;
    a.download = "prompt.txt";
    document.body.appendChild(a);
    a.click();

    // Clean up
    setTimeout(function() {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);  
    }, 0);
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
