/**
 * CrewAI Multi-Agent Research System
 * Frontend JavaScript for handling interactions and real-time updates
 */

// DOM Elements
const researchForm = document.getElementById('research-form');
const topicInput = document.getElementById('topic');
const submitBtn = document.getElementById('submit-btn');
const progressSection = document.getElementById('progress-section');
const resultsSection = document.getElementById('results-section');
const statusText = document.getElementById('status-text');
const progressBar = document.getElementById('progress-bar');
const agentActivity = document.getElementById('agent-activity');
const resultsContent = document.getElementById('results-content');
const newResearchBtn = document.getElementById('new-research-btn');

// State
let eventSource = null;
let isResearchRunning = false;

/**
 * Initialize the application
 */
function init() {
    // Form submission handler
    researchForm.addEventListener('submit', handleFormSubmit);

    // New research button handler
    newResearchBtn.addEventListener('click', resetForm);

    // Check initial status
    checkStatus();
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    const topic = topicInput.value.trim();

    if (!topic) {
        showError('Please enter a research topic');
        return;
    }

    if (isResearchRunning) {
        showError('Research is already in progress');
        return;
    }

    // Start research
    await startResearch(topic);
}

/**
 * Start research on a topic
 */
async function startResearch(topic) {
    try {
        // Update UI state
        isResearchRunning = true;
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');

        // Show progress section
        progressSection.style.display = 'block';
        resultsSection.style.display = 'none';
        agentActivity.innerHTML = '';
        progressBar.style.width = '10%';

        // Send request to backend
        const response = await fetch('/api/research', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to start research');
        }

        const data = await response.json();
        updateStatus('🚀 Research started...', 'success');

        // Start listening to progress updates
        connectToEventStream();

    } catch (error) {
        console.error('Error starting research:', error);
        showError(error.message || 'Failed to start research');
        resetUI();
    }
}

/**
 * Connect to Server-Sent Events stream for real-time updates
 */
function connectToEventStream() {
    // Close existing connection if any
    if (eventSource) {
        eventSource.close();
    }

    // Create new EventSource connection
    eventSource = new EventSource('/api/stream');

    eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleProgressUpdate(data);
        } catch (error) {
            console.error('Error parsing SSE data:', error);
        }
    };

    eventSource.onerror = (error) => {
        console.error('EventSource error:', error);
        eventSource.close();

        // Only show error if research was running
        if (isResearchRunning) {
            showError('Connection lost. Please refresh the page.');
        }
    };
}

/**
 * Handle progress updates from the server
 */
function handleProgressUpdate(data) {
    const { status, message, result } = data;

    // Ignore heartbeat messages
    if (status === 'heartbeat') {
        return;
    }

    // Update status text
    if (message) {
        updateStatus(message, status);

        // Add to activity log
        if (status === 'running' && !message.includes('Starting research')) {
            addActivityItem(message);
        }
    }

    // Update progress bar
    updateProgressBar(status);

    // Handle completion
    if (status === 'completed' && result) {
        handleResearchComplete(result);
    }

    // Handle errors
    if (status === 'error') {
        showError(message);
        resetUI();
    }
}

/**
 * Update status message
 */
function updateStatus(message, type = 'info') {
    statusText.textContent = message;

    const statusContainer = document.getElementById('status-container');
    const statusItem = statusContainer.querySelector('.status-item');

    // Update icon based on type
    const icon = statusItem.querySelector('.status-icon');
    if (type === 'completed' || type === 'success') {
        icon.textContent = '✅';
    } else if (type === 'error') {
        icon.textContent = '❌';
    } else {
        icon.textContent = '⏳';
    }
}

/**
 * Update progress bar
 */
function updateProgressBar(status) {
    if (status === 'running') {
        const currentWidth = parseInt(progressBar.style.width) || 10;
        const newWidth = Math.min(currentWidth + 15, 90);
        progressBar.style.width = `${newWidth}%`;
    } else if (status === 'completed') {
        progressBar.style.width = '100%';
    }
}

/**
 * Add activity item to the log
 */
function addActivityItem(message) {
    const activityItem = document.createElement('div');
    activityItem.className = 'activity-item';
    activityItem.textContent = message;
    agentActivity.appendChild(activityItem);

    // Scroll to latest activity
    activityItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Handle research completion
 */
function handleResearchComplete(result) {
    // Update progress bar to 100%
    progressBar.style.width = '100%';
    updateStatus('✅ Research completed successfully!', 'completed');

    // Show results after a brief delay
    setTimeout(() => {
        progressSection.style.display = 'none';
        resultsSection.style.display = 'block';
        resultsContent.textContent = result;

        // Reset UI state
        resetUI();
    }, 1500);

    // Close event stream
    if (eventSource) {
        eventSource.close();
    }
}

/**
 * Show error message
 */
function showError(message) {
    updateStatus(`❌ Error: ${message}`, 'error');

    // You could also add a toast notification here
    console.error(message);
}

/**
 * Reset UI state
 */
function resetUI() {
    isResearchRunning = false;
    submitBtn.disabled = false;
    submitBtn.classList.remove('loading');
}

/**
 * Reset form for new research
 */
function resetForm() {
    topicInput.value = '';
    progressSection.style.display = 'none';
    resultsSection.style.display = 'none';
    agentActivity.innerHTML = '';
    progressBar.style.width = '0%';
    resetUI();
    topicInput.focus();
}

/**
 * Check current status on page load
 */
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();

        if (data.status === 'running') {
            // Research is already running, connect to stream
            progressSection.style.display = 'block';
            isResearchRunning = true;
            submitBtn.disabled = true;
            connectToEventStream();
        } else if (data.status === 'completed' && data.result) {
            // Show previous results
            resultsSection.style.display = 'block';
            resultsContent.textContent = data.result;
        }
    } catch (error) {
        console.error('Error checking status:', error);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (eventSource) {
        eventSource.close();
    }
});
