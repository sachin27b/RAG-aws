// app.js — place in app/static/js/app.js
// Minimal, dependency-free frontend to call Flask endpoints.

const uploadForm = document.getElementById("uploadForm");
const pdfFileInput = document.getElementById("pdfFile");
const chunkSizeInput = document.getElementById("chunkSize");
const uploadLog = document.getElementById("uploadLog");

const ingestBtn = document.getElementById("ingestBtn");
const ingestLog = document.getElementById("ingestLog");
const pollStopBtn = document.getElementById("pollStopBtn");

const queryForm = document.getElementById("queryForm");
const queryText = document.getElementById("queryText");
const topKInput = document.getElementById("topK");
const answerText = document.getElementById("answerText");
const contextText = document.getElementById("contextText");

let pollIntervalId = null;

// helper
function appendLog(el, msg) {
  const time = new Date().toLocaleTimeString();
  el.textContent = `[${time}] ${msg}\n` + el.textContent;
}

// Upload handler
uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const file = pdfFileInput.files[0];
  if (!file) {
    appendLog(uploadLog, "No file selected.");
    return;
  }

  appendLog(uploadLog, `Starting upload: ${file.name}`);

  const form = new FormData();
  form.append("file", file);
  // include chunkSize so backend can adapt (optional)
  form.append("chunk_size", chunkSizeInput.value || "50");

  try {
    const resp = await fetch("/upload", {
      method: "POST",
      body: form
    });

    if (!resp.ok) {
      const err = await resp.json();
      appendLog(uploadLog, `Upload failed: ${err.error || resp.statusText}`);
      return;
    }

    const data = await resp.json();
    appendLog(uploadLog, `Upload succeeded: ${data.message || "OK"}`);
  } catch (err) {
    appendLog(uploadLog, `Upload error: ${err.message}`);
  }
});

// Ingest handler (starts job and polls until COMPLETE/FAILED)
ingestBtn.addEventListener("click", async () => {
  appendLog(ingestLog, "Requesting ingestion start...");
  ingestBtn.disabled = true;
  pollStopBtn.hidden = false;

  try {
    const resp = await fetch("/ingest", {
      method: "POST"
    });

    if (!resp.ok) {
      const err = await resp.json();
      appendLog(ingestLog, `Start failed: ${err.error || resp.statusText}`);
      ingestBtn.disabled = false;
      pollStopBtn.hidden = true;
      return;
    }

    const data = await resp.json();
    appendLog(ingestLog, `Job started: ${data.job_id || "unknown"} — Status: ${data.status}`);

    // If backend returns status already (some implementations wait), show it
    if (data.status && (data.status === "COMPLETE" || data.status === "FAILED")) {
      appendLog(ingestLog, `Final status: ${data.status}`);
      ingestBtn.disabled = false;
      pollStopBtn.hidden = true;
      return;
    }

    // If backend returns a job_id and is not already complete, poll the /ingest endpoint for status
    // Here, implementation expects the backend to respond with job_id and status — if your backend differs, adapt accordingly.
    // We'll poll the server every 6s by calling /ingest (the backend route in this example starts job and waits — adjust if different).
    pollIntervalId = setInterval(async () => {
      try {
        const p = await fetch("/ingest", { method: "POST" });
        if (!p.ok) return;
        const pj = await p.json();
        appendLog(ingestLog, `Polling: ${pj.status}`);
        if (pj.status === "COMPLETE" || pj.status === "FAILED") {
          appendLog(ingestLog, `Final status: ${pj.status}`);
          clearInterval(pollIntervalId);
          pollIntervalId = null;
          ingestBtn.disabled = false;
          pollStopBtn.hidden = true;
        }
      } catch (e) {
        appendLog(ingestLog, `Polling error: ${e.message}`);
      }
    }, 6000);

  } catch (err) {
    appendLog(ingestLog, `Error starting ingestion: ${err.message}`);
    ingestBtn.disabled = false;
    pollStopBtn.hidden = true;
  }
});

// Stop polling if needed
pollStopBtn.addEventListener("click", () => {
  if (pollIntervalId) {
    clearInterval(pollIntervalId);
    pollIntervalId = null;
    appendLog(ingestLog, "Polling stopped by user.");
    ingestBtn.disabled = false;
    pollStopBtn.hidden = true;
  }
});

// Query handler
queryForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const query = queryText.value.trim();
  if (!query) {
    appendLog(ingestLog, "Query is empty.");
    return;
  }

  answerText.textContent = "Waiting for answer...";
  contextText.textContent = "Loading context...";

  try {
    const resp = await fetch("/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        top_k: Number(topKInput.value || 3)
      })
    });

    if (!resp.ok) {
      const err = await resp.json();
      appendLog(ingestLog, `Query failed: ${err.error || resp.statusText}`);
      answerText.textContent = "Error — see logs";
      contextText.textContent = "-";
      return;
    }

    const data = await resp.json();
    answerText.textContent = data.answer || JSON.stringify(data, null, 2);
    // If the backend returns retrievals/context separately, display; here we try to be flexible
    if (data.context) {
      contextText.textContent = data.context;
    } else if (data.retrievals) {
      contextText.textContent = JSON.stringify(data.retrievals, null, 2);
    } else {
      contextText.textContent = "No retrievals returned.";
    }

    appendLog(ingestLog, `Query completed.`);
  } catch (err) {
    appendLog(ingestLog, `Query error: ${err.message}`);
    answerText.textContent = "Error — see logs";
    contextText.textContent = "-";
  }
});
