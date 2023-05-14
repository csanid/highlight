document.addEventListener('DOMContentLoaded', function() {
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
