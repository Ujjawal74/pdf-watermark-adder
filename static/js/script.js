document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('pdf_files');
    const fileList = document.getElementById('file-list');
    
    fileInput.addEventListener('change', function(e) {
        fileList.innerHTML = '';
        
        if (this.files.length === 0) {
            return;
        }
        
        if (this.files.length === 1) {
            const file = this.files[0];
            addFileItem(file);
        } else {
            Array.from(this.files).forEach(file => {
                addFileItem(file);
            });
        }
    });
    
    function addFileItem(file) {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const icon = document.createElement('i');
        icon.className = 'bi bi-file-earmark-pdf';
        
        const nameSpan = document.createElement('span');
        nameSpan.className = 'file-item-name';
        nameSpan.textContent = file.name;
        
        const sizeSpan = document.createElement('span');
        sizeSpan.className = 'file-item-size';
        sizeSpan.textContent = formatFileSize(file.size);
        
        fileItem.appendChild(icon);
        fileItem.appendChild(nameSpan);
        fileItem.appendChild(sizeSpan);
        
        fileList.appendChild(fileItem);
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Drag and drop functionality
    const fileUploadLabel = document.querySelector('.file-upload-label');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileUploadLabel.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        fileUploadLabel.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        fileUploadLabel.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        fileUploadLabel.classList.add('highlight');
    }
    
    function unhighlight() {
        fileUploadLabel.classList.remove('highlight');
    }
    
    fileUploadLabel.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        
        // Trigger change event manually
        const event = new Event('change');
        fileInput.dispatchEvent(event);
    }
    
    // Form validation
    const form = document.querySelector('.needs-validation');
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        
        form.classList.add('was-validated');
    }, false);
});