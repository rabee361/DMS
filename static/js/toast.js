    // Show selectable URL in modal for manual copying
    function showSelectableUrl(url) {
        // Create modal for URL display
        const modal = document.createElement('div');
        modal.className = 'url-display';
        modal.innerHTML = `
            <p>انسخ الرابط التالي:</p>
            <input type="text" value="${url}" readonly>
            <button class="close-btn">إغلاق</button>
        `;
        
        document.body.appendChild(modal);
        
        // Select the URL text for easy copying
        const input = modal.querySelector('input');
        input.focus();
        input.select();
        
        // Close modal when button is clicked
        const closeBtn = modal.querySelector('.close-btn');
        closeBtn.addEventListener('click', () => {
            document.body.removeChild(modal);
        });
    }

    // Copy button handler
    function copyButtonHandler(e) {
        e.preventDefault();
        const url = this.getAttribute('data-url');
        showSelectableUrl(url);
    }

    // Handle row clicks
    function clickHandler(event) {
        const link = event.currentTarget.getAttribute('data-link');
        if (link) {
            window.location.href = link;
        }
    }
    
    // Initialize copy buttons
    document.addEventListener('DOMContentLoaded', function() {
        const copyButtons = document.querySelectorAll('.copy-btn');
        copyButtons.forEach(button => {
            button.addEventListener('click', copyButtonHandler);
        });
    });