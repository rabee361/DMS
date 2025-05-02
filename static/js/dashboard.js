/* globals Chart:false */

(() => {
  'use strict'

  // Graphs
  const initializeChart = () => {
    const ctx = document.getElementById('myChart')
    if (!ctx) return;

    // eslint-disable-next-line no-unused-vars
    const myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [
          'Sunday',
          'Monday',
          'Tuesday',
          'Wednesday',
          'Thursday',
          'Friday',
          'Saturday'
        ],
        datasets: [{
          data: [
            15339,
            21345,
            18483,
            24003,
            23489,
            24092,
            12034
          ],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }]
      },
      options: {
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            boxPadding: 3
          }
        }
      }
    })
  }

  // Initialize Date Range Picker (if jQuery is available)
  const initializeDateRangePicker = () => {
    const dateRangeInput = $('input[name="daterange"]');
    if (dateRangeInput.length) {
      dateRangeInput.daterangepicker({
        opens: 'left',
        locale: {
          format: 'YYYY-MM-DD'
        },
        autoApply: true,
        showDropdowns: true
      }, function(start, end, label) {
        console.log("Selected date range: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
      });
    }
  }

  // Initialize Native Date Pickers - no jQuery required
  const initializeNativeDatePickers = () => {
    // For absence form
    const startDateInput = document.getElementById('id_start');
    const endDateInput = document.getElementById('id_end');
    
    if (startDateInput) {
      // Set attributes for date input
      startDateInput.setAttribute('type', 'date');
      startDateInput.addEventListener('change', function() {
        // Set minimum date for end date picker
        if (endDateInput && this.value) {
          endDateInput.min = this.value;
        }
      });
    }
    
    if (endDateInput) {
      // Set attributes for date input
      endDateInput.setAttribute('type', 'date');
      if (startDateInput && startDateInput.value) {
        endDateInput.min = startDateInput.value;
      }
    }
  }

  // Sidebar functionality
  const initializeSidebar = () => {
    // Handle sidebar toggle on mobile
    const sidebarToggle = document.querySelector('[data-bs-toggle="offcanvas"]');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', function() {
        document.querySelector('.sidebar').classList.toggle('show');
      });
    }

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(event) {
      const sidebar = document.querySelector('.sidebar');
      const toggle = document.querySelector('[data-bs-toggle="offcanvas"]');
      if (sidebar && toggle && window.innerWidth < 768 && 
          !sidebar.contains(event.target) && 
          !toggle.contains(event.target)) {
        sidebar.classList.remove('show');
      }
    });
  }

  // Handle submenu animations
  const initializeSubmenus = () => {
    const submenuToggles = document.querySelectorAll('.has-submenu > .nav-link');
    
    submenuToggles.forEach(toggle => {
      toggle.addEventListener('click', function(e) {
        const submenuIcon = this.querySelector('.submenu-icon');
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        
        // Animate the chevron icon
        if (submenuIcon) {
          submenuIcon.style.transform = isExpanded ? 'rotate(0deg)' : 'rotate(-180deg)';
        }
      });
    });
  }

  // Set active state based on current URL
  const setActiveNavItem = () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    
    navLinks.forEach(link => {
      if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
        // If in submenu, expand parent
        const parentSubmenu = link.closest('.submenu');
        if (parentSubmenu) {
          parentSubmenu.classList.add('show');
          const parentToggle = parentSubmenu.previousElementSibling;
          if (parentToggle) {
            parentToggle.setAttribute('aria-expanded', 'true');
          }
        }
      }
    });
  }

  // Initialize form template selection
  const initializeTemplateSelection = () => {
    const templateOptions = document.querySelectorAll('.template-option');
    
    templateOptions.forEach(option => {
      const radioInput = option.querySelector('input[type="radio"]');
      const preview = option.querySelector('.template-preview');
      
      if (preview && radioInput) {
        // Make the template preview clickable
        preview.addEventListener('click', () => {
          // Check the radio button
          radioInput.checked = true;
          
          // Trigger change event to ensure form validation works
          const changeEvent = new Event('change', { bubbles: true });
          radioInput.dispatchEvent(changeEvent);
        });
        
        // Add keyboard accessibility
        preview.setAttribute('tabindex', '0');
        preview.addEventListener('keydown', (e) => {
          // Select with Enter or Space key
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            radioInput.checked = true;
            
            // Trigger change event
            const changeEvent = new Event('change', { bubbles: true });
            radioInput.dispatchEvent(changeEvent);
          }
        });
      }
    });
  }

  // Initialize file input enhancement
  const initializeFileInputs = () => {
    const fileInputs = document.querySelectorAll('.form-control-file');
    
    fileInputs.forEach(input => {
      // Create a container for the file preview
      const previewContainer = document.createElement('div');
      previewContainer.className = 'file-preview';
      previewContainer.style.display = 'none';
      
      // Set up the preview content
      previewContainer.innerHTML = `
        <img src="" alt="File Preview">
        <div class="file-info">
          <div class="file-name"></div>
          <div class="file-size"></div>
        </div>
        <button type="button" class="file-remove" aria-label="Remove file">×</button>
      `;
      
      // Insert the preview after the input
      input.parentNode.insertBefore(previewContainer, input.nextSibling);
      
      // Add change event to the file input
      input.addEventListener('change', function() {
        const file = this.files[0];
        const preview = this.parentNode.querySelector('.file-preview');
        const previewImage = preview.querySelector('img');
        const fileName = preview.querySelector('.file-name');
        const fileSize = preview.querySelector('.file-size');
        
        if (file) {
          // Show the preview
          preview.style.display = 'flex';
          
          // Set file name and size
          fileName.textContent = file.name;
          fileSize.textContent = formatFileSize(file.size);
          
          // Create preview for image files
          if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
              previewImage.src = e.target.result;
              previewImage.style.display = 'block';
            };
            reader.readAsDataURL(file);
          } else {
            // For non-image files, show a generic icon
            previewImage.src = '/static/images/file-icon.png';
            previewImage.style.display = 'block';
          }
        } else {
          // Hide the preview if no file is selected
          preview.style.display = 'none';
        }
      });
      
      // Add click event to the remove button
      const removeButton = previewContainer.querySelector('.file-remove');
      removeButton.addEventListener('click', function() {
        const fileInput = this.closest('.form-group').querySelector('.form-control-file');
        fileInput.value = '';
        this.closest('.file-preview').style.display = 'none';
        
        // Trigger change event to ensure form validation works
        const changeEvent = new Event('change', { bubbles: true });
        fileInput.dispatchEvent(changeEvent);
      });
    });
  }

  // Helper function to format file size
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  // Document ready handler
  document.addEventListener('DOMContentLoaded', function() {
    initializeChart();
    initializeSidebar();
    initializeSubmenus();
    setActiveNavItem();
    initializeNativeDatePickers();
    initializeTemplateSelection();
    initializeFileInputs();
    
    // Initialize jQuery-dependent features if jQuery is available
    if (typeof $ !== 'undefined') {
      initializeDateRangePicker();
    }
  });
})();

function executeBulkAction() {
  const bulkActionForm = document.getElementById('bulkActionForm');
  if (!bulkActionForm) {
      console.error('Bulk action form not found');
      return;
  }

  const selectedCheckboxes = document.querySelectorAll('.item-checkbox:checked');
  const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
  const action = document.getElementById('bulkAction').value;

  if (selectedIds.length === 0) {
      alert('الرجاء اختيار عنصر واحد على الأقل');
      return;
  }

  if (!action) {
      alert('الرجاء اختيار إجراء');
      return;
  }

  if (action === 'delete' && !confirm('هل أنت متأكد من حذف العناصر المحددة؟')) {
      return;
  }

  document.getElementById('selectedIds').value = JSON.stringify(selectedIds);
  document.getElementById('selectedAction').value = action;
  bulkActionForm.submit();
}

// Handle row clicks to navigate to data-link URL
function clickHandler(event) {
    const row = event.currentTarget;
    const link = row.getAttribute('data-link');
    if (link) {
        window.location.href = link;
    }
}

// Initialize bulk action functionality
document.addEventListener('DOMContentLoaded', function() {
  const selectAll = document.getElementById('selectAll');
  if (selectAll) {
      selectAll.addEventListener('change', function() {
          const checkboxes = document.querySelectorAll('.item-checkbox');
          checkboxes.forEach(checkbox => checkbox.checked = this.checked);
      });
  }

  // Initialize row checkboxes
  const rowCheckboxes = document.querySelectorAll('.item-checkbox');
  rowCheckboxes.forEach(checkbox => {
      checkbox.addEventListener('change', function() {
          const allChecked = Array.from(rowCheckboxes).every(cb => cb.checked);
          if (selectAll) {
              selectAll.checked = allChecked;
          }
      });
  });
});


