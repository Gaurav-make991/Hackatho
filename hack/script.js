const API_BASE_URL = "http://127.0.0.1:8000";
let currentSessionId = null;

// Helper to show toasts (seen in your analyzer.html)
function showToast(msg, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${msg}`);
    // Your existing toast logic here
}

async function analyzeLogsWorkflow(file) {
    if (!file) return;

    try {
        // 1. Upload
        showToast("Uploading logs...", "info");
        const formData = new FormData();
        formData.append("file", file);
        
        const uploadRes = await fetch(`${API_BASE_URL}/upload`, { 
            method: "POST", 
            body: formData 
        });
        const uploadData = await uploadRes.json();
        currentSessionId = uploadData.session_id;

        // 2. Anomaly Scan
        showToast("Scanning for anomalies...", "info");
        await fetch(`${API_BASE_URL}/analyze/${currentSessionId}`);

        // 3. AI Report
        showToast("Generating AI Insight...", "info");
        const reportRes = await fetch(`${API_BASE_URL}/report/${currentSessionId}`);
        const reportData = await reportRes.json();
        
        displayReport(reportData.crash_report);
        showToast("Analysis Complete!", "success");

    } catch (err) {
        showToast("Connection failed to port 8000", "error");
        console.error(err);
    }
}

function displayReport(report) {
    // Logic to update your UI elements
    const causeEl = document.querySelector('.probable-root-cause');
    if (causeEl) causeEl.textContent = report.probable_root_cause;
}