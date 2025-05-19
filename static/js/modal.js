/**
 * Modal Manager - Handles delete confirmation modal functionality
 */
document.addEventListener('DOMContentLoaded', function() {
  // Cache DOM elements
  const modal = document.getElementById('deleteModal');
  const modalItemName = document.getElementById('deleteItemName');
  const modalForm = document.getElementById('deleteForm');
  const closeButtons = document.querySelectorAll('.modal-close, .modal-cancel');
  
  // Initialize the modal if it exists
  if (modal) {
    // Handle all delete buttons
    initDeleteButtons();
    
    // Close modal when clicking close buttons
    closeButtons.forEach(button => {
      button.addEventListener('click', closeModal);
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
      if (event.target === modal) {
        closeModal();
      }
    });
    
    // Close modal when pressing Escape key
    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape' && modal.classList.contains('show')) {
        closeModal();
      }
    });
  }
  
  /**
   * Initialize delete buttons with click handlers
   */
  function initDeleteButtons() {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    
    deleteButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        const id = this.getAttribute('data-id');
        const name = this.getAttribute('data-name');
        const url = this.getAttribute('data-url') || this.href;
        
        // Set the form action and item name in the modal
        if (modalForm) modalForm.setAttribute('action', url);
        if (modalItemName) modalItemName.textContent = name || id;
        
        // Show the modal
        openModal();
      });
    });
  }
  
  /**
   * Open modal with animation
   */
  function openModal() {
    if (!modal) return;
    
    // Prevent body scrolling
    document.body.classList.add('modal-open');
    
    // Display modal
    modal.style.display = 'block';
    
    // Trigger reflow for animation
    void modal.offsetWidth;
    
    // Add show class for animation
    modal.classList.add('show');
  }
  
  /**
   * Close modal with animation
   */
  function closeModal() {
    if (!modal) return;
    
    // Remove show class to start hiding animation
    modal.classList.remove('show');
    
    // Wait for animation to complete before hiding
    setTimeout(function() {
      modal.style.display = 'none';
      document.body.classList.remove('modal-open');
    }, 300);
  }
  
  /**
   * Show toast notification with message
   * @param {string} message - Message to display in toast
   * @param {string} type - Type of toast (success, error)
   */
  window.showToast = function(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    const toastContent = toast.querySelector('.toast-content');
    if (toastContent) toastContent.textContent = message;
    
    // Set toast type class
    toast.className = 'toast-notification';
    toast.classList.add(type);
    toast.classList.add('show');
    
    // Auto hide after 3 seconds
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3000);
  }
});
  