// Resize content field of modal and scroll down page 
$(document).ready(function() {
    function resize() { 
        $(this).css('height', 'auto');
        $(this).css('height', this.scrollHeight + 'px');

        // $('#noteModal').animate({
        //     scrollTop: $('#noteModal').height() 
        // }, 'slow');
    }
    $('#noteModal').on('shown.bs.modal', function() {
    // $('#card').on('click', function() {
        resize.call($('#content')[0]);
    });
});

// Set action for form when "New note" button is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#addButton').onclick = () => {
        document.querySelector('#noteForm').action = `/highlight/add`;
    };
});

// Open modal when a card is clicked and set form action to editing existing note  
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

// Handle server-side validation for note form 
document.addEventListener('DOMContentLoaded', function() {
    $('#noteForm').on('submit', function (event) {
        event.preventDefault();
        const form = $('#noteForm');
        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            data: form.serialize(),
            success: function (data) {
                if (data.success) {
                    $('#noteModal').modal('hide');
                    window.location.href = "";
                } else {
                    $('.errors').html(data['error']);
                    showFormErrors(data.errors);
                }
            },
            error: function (data) {
                console.log('Error');
                console.log(data);
            },
        });        
    });

    // Show error messages    
    function showFormErrors(errors) {
        $('#noteForm').find('.error-message').remove();
        for (let key in errors) {
            let error = errors[key][0];
            let field = $('#noteForm').find('#div_id_' + key);
            field.addClass('is-invalid');
            field.after('<p class="error-message">' + error + '</p>');
            console.log('key: ' + key + ' field:' + field + ' error:' + error);
        }
    }
});   

// Reset form when modal is closed
$(document).ready(function() {
    $('#noteModal').on('hidden.bs.modal', function() {
        $('#modalTitle').text("New note");
        $('#noteForm')[0].reset();
        $('#noteForm').find('.error-message').remove();
        $('#content').css('height', 'auto');
    });
});

// Set text and action for delete confirmation dialog
$(document).ready(function() {
    $('#deleteDialog').on('show.bs.modal', function(event) {
        $('#title').text($(event.relatedTarget).data('title'));
        $('#deleteConfirmBtn').attr('href', $(event.relatedTarget).data('url'));
    });
}); 