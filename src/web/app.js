const API_URL = window.location.origin;

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const resultsSection = document.getElementById('resultsSection');
const loading = document.getElementById('loading');
const severityFilter = document.getElementById('severityFilter');

let currentResult = null;

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

severityFilter.addEventListener('change', () => {
    if (currentResult) {
        renderIssues(currentResult);
    }
});

async function handleFile(file) {
    resultsSection.style.display = 'none';
    loading.style.display = 'block';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        if (data.success) {
            currentResult = data.result;
            renderResults(data.result);
        } else {
            alert(`Analysis failed: ${data.error}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        loading.style.display = 'none';
    }
}

function renderResults(result) {
    resultsSection.style.display = 'block';
    
    document.getElementById('totalEntries').textContent = result.total_entries.toLocaleString();
    document.getElementById('errorCount').textContent = result.error_count.toLocaleString();
    document.getElementById('warningCount').textContent = result.warning_count.toLocaleString();
    document.getElementById('scanTime').textContent = `${result.scan_time_ms}ms`;
    
    renderIssues(result);
    renderTags(result);
}

function renderIssues(result) {
    const issuesList = document.getElementById('issuesList');
    const filter = severityFilter.value;
    
    let issues = result.issues;
    if (filter !== 'all') {
        issues = issues.filter(i => i.severity === filter);
    }
    
    if (issues.length === 0) {
        issuesList.innerHTML = '<p class="no-issues">No issues found</p>';
        return;
    }
    
    issuesList.innerHTML = issues.map(issue => `
        <div class="issue-item">
            <span class="issue-severity ${issue.severity.toLowerCase()}">${issue.severity}</span>
            <div class="issue-info">
                <div class="issue-category">${issue.category}</div>
                <div class="issue-message">${issue.message}</div>
            </div>
            <span class="issue-count">${issue.count}x</span>
        </div>
    `).join('');
}

function renderTags(result) {
    const tagsCloud = document.getElementById('tagsCloud');
    
    tagsCloud.innerHTML = result.top_tags.map(([tag, count]) => `
        <span class="tag">
            ${tag}
            <span class="tag-count">${count.toLocaleString()}</span>
        </span>
    `).join('');
}

async function checkHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        console.log('API Status:', data.status);
    } catch (error) {
        console.error('API not available:', error);
    }
}

checkHealth();
