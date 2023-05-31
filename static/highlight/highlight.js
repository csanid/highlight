// Resize content field according to input 
$(document).ready(function() {
    function resize() {
        $(this).css('height', 'auto');
        $(this).css('height', this.scrollHeight + 'px');

        // $('#noteModal').animate({
        //     scrollTop: $('#noteModal').height() 
        // }, 'slow');
 
        // let modalHeight = $('#noteModal .modal-content').outerHeight();
        // if (modalHeight > $(window).height()) {
            // let modalBottom = $('#noteModal .modal-dialog').offset().top + modalHeight;
            // $('html, body').scrollTop(modalBottom);
        // }
        // if (this.clientHeight < this.scrollHeight) {            
            // const target = $('#submitButton').offset().top - $(window).height() + $('#submitButton').outerHeight();
            // $('html, body').scrollTop(target);
            // window.scrollTo(0, document.body.scrollHeight);
            // $('html, body').animate({
            //     scrollTop: $(document).height() - $(window).height()
            // }, 500);
        // }
    }
    $('#noteModal').on('shown.bs.modal', function() {
        resize.call($('#content')[0]);
    });
    $('#content').on('input', resize);    
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

// Handle form submission
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
                    console.log('Success');
                    console.log(data);
                    window.location.href = "";
                } else {
                    console.log('Error in server validation');
                    console.log(data.errors)
                    showValidationErrors(data.errors);
                }
            },
            error: function (data) {
                console.log('Error');
                console.log(data);
            },
        });        
    });

    function showValidationErrors(errors) {

    }

});   

// Reset form when modal is closed
$(document).ready(function() {
    $('#noteModal').on('hidden.bs.modal', function() {
        $('#modalTitle').text("New note");
        $('#noteForm')[0].reset();
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