function confirmDelete(entryId) {
    var confirmation = confirm("Are you sure you want to delete this journal entry?");
    
    if (confirmation) {
        // If user confirms, redirect to the Flask route for deletion
        window.location.href = "/remove/" + entryId;
    } else {
        // If user cancels, do nothing or provide feedback
        console.log("Deletion canceled");
    }
}