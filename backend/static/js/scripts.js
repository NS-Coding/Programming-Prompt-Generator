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
