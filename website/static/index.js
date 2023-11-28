function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId})
    }).then((_res) => {
        window.location.href = "/"
    })
}

function deletePatient(patientId) {
    fetch('/delete_Patient', {
        method: 'POST',
        body: JSON.stringify({patientId: patientId})
    }).then((_res) => {
        window.location.href = "/patients"
    })
}


// function editPatient(patientId) {
//     fetch('/fetch_patient', {
//         method: 'POST',
//         body: JSON.stringify({patientId: patientId})
//     })
//     .then((response) => {
//         return response.json();
//     })
//     .then((data) => {
//         console.log(data);
//         window.location = '/edit_patient_redirect'
//     });
// }

