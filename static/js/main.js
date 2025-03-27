document.addEventListener('DOMContentLoaded', function() {
    // File drag and drop area
    const dropArea = document.querySelector('.drag-area');
    const fileInput = document.querySelector('#file-input');
    const browseBtn = document.querySelector('#browse-btn');
    const uploadForm = document.querySelector('#upload-form');
    const spinner = document.querySelector('.processing-spinner');
    
    // Export functionality
    const exportBtn = document.querySelector('#export-btn');
    
    // Initialize the UI
    initializeUI();
    
    function initializeUI() {
        // File upload event listeners
        if (dropArea) {
            ['dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropArea.addEventListener(eventName, preventDefaults, false);
            });
            
            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            // Highlight drop area when drag over
            dropArea.addEventListener('dragover', function() {
                this.classList.add('active');
            });
            
            // Remove highlight when drag leave
            dropArea.addEventListener('dragleave', function() {
                this.classList.remove('active');
            });
            
            // Handle file drop
            dropArea.addEventListener('drop', function(e) {
                this.classList.remove('active');
                fileInput.files = e.dataTransfer.files;
                updateFileName();
            });
            
            // Open file selector when browse button is clicked
            if (browseBtn) {
                browseBtn.addEventListener('click', function() {
                    fileInput.click();
                });
            }
            
            // Update file name display when file is selected
            if (fileInput) {
                fileInput.addEventListener('change', updateFileName);
            }
            
            // Show spinner when form is submitted
            if (uploadForm) {
                uploadForm.addEventListener('submit', function() {
                    spinner.style.display = 'block';
                    dropArea.style.display = 'none';
                });
            }
        }
        
        // Export functionality
        if (exportBtn) {
            exportBtn.addEventListener('click', exportResults);
        }
    }
    
    // Update file name display when a file is selected
    function updateFileName() {
        const fileName = fileInput.files[0]?.name || 'No file selected';
        const fileNameElement = document.querySelector('#file-name');
        if (fileNameElement) {
            fileNameElement.textContent = fileName;
            fileNameElement.style.display = 'block';
        }
        
        // Enable/disable submit button based on file selection
        const submitBtn = document.querySelector('#submit-btn');
        if (submitBtn) {
            submitBtn.disabled = !fileInput.files.length;
        }
    }
    
    // Export results as JSON
    function exportResults() {
        fetch('/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'format=json'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Export failed');
            }
            return response.json();
        })
        .then(data => {
            // Create a JSON file and trigger download
            const jsonData = JSON.stringify(data, null, 2);
            const blob = new Blob([jsonData], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = 'medical_document_analysis.json';
            document.body.appendChild(a);
            a.click();
            
            // Clean up
            setTimeout(() => {
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }, 100);
        })
        .catch(error => {
            console.error('Error exporting results:', error);
            alert('Failed to export results. Please try again.');
        });
    }
});
