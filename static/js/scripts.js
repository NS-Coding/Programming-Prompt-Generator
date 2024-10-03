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

// Initialize the preamble when the page loads
document.addEventListener('DOMContentLoaded', function() {
    updatePreamble();
});
