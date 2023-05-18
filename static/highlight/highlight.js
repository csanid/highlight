// Set action for form when "Add note" button is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#addButton').onclick = () => {
        document.querySelector('#noteForm').action = `/highlight/add`;
    };
});

// Open form when a card is clicked and set its action to editing existing note  
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#card').forEach(card => {
        card.onclick = async function() {
            const note_id = this.dataset.id;                      
            const modal = new bootstrap.Modal('#noteModal');
            modal.show();             
            document.querySelector('#noteForm').action = `/highlight/edit/${note_id}`;
            get_note(note_id);
        }        
    });
}); 

// Reset form when modal is closed
$(document).ready(function () {
    $('#noteModal').on('hidden.bs.modal', function () {
        $(this).find('form').trigger('reset');
    });
});

// Retrieve note data from database
async function get_note(id) {
    const url = `/highlight/notes/${id}`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        populate_form(data);                               
    } catch (error) {
        console.log('Error:', error);
    }
}
      
// Populate note form with data received from server
function populate_form(data) {     
    const form = document.querySelector('#noteForm');    
    document.querySelector('#modalTitle').innerHTML = data.title;
    form.title.value = data.title;
    form.author.value = data.author;
    form.book_title.value = data.book_title;
    form.publisher.value = data.publisher;
    form.year.value = data.year;
    form.content.value = data.content;
}

// Set text and action for delete confirmation dialog
$(document).ready(function () {
    $('#deleteDialog').on('show.bs.modal', function(event) {
        $("#title").text($(event.relatedTarget).data('title'));
        $("#deleteConfirmBtn").attr('href', $(event.relatedTarget).data('url'));
    });
}); 

/* document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#card').forEach(card => {
        card.onclick = async function() {
            const note_id = this.dataset.id;                      
            const modal = new bootstrap.Modal('#noteModal');
            modal.show();             
            document.querySelector('#noteForm').action = `/highlight/edit/${note_id}`;
            const url = `/highlight/notes/${note_id}`;
            try {
                const response = await fetch(url);
                const data = await response.json();
                populate_form(data);                               
            } catch (error) {
                console.log('Error:', error);
            }
        }        
    });
});        */

/* document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#card').forEach(card => {
        card.onclick = async function() {
            const id = this.dataset.id;
            const url = `/highlight/notes/${id}`;
            try {
                const response = await fetch(url);
                const data = await response.json();
                populate_form(data);                
            } catch (error) {
                console.log('Error:', error);
            }
        }
    });
});         

function populate_form(data) {
    const modal = new bootstrap.Modal('#noteModal');
    modal.show();    
    const form = document.querySelector('#noteForm');          
    const submitButton = document.querySelector('#submitButton');
    submitButton.dataset.note_id = data.id;    
    form.title.value = data.title;
    form.author.value = data.author;
    form.book_title.value = data.book_title;
    form.publisher.value = data.publisher;
    form.year.value = data.year;
    form.content.value = data.content;
}
 */