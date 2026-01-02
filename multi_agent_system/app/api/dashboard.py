from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def dashboard():
    html = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Multi-Agent Dashboard</title>
  <style>
    :root{
      --bg:#0b1020; --panel:#121a33; --panel2:#0f1730; --text:#e8ecff; --muted:#a7b0d6;
      --border:rgba(255,255,255,.08); --accent:#7c5cff; --good:#22c55e; --warn:#f59e0b;
    }
    *{box-sizing:border-box}
    body{
      margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
      background: radial-gradient(1000px 600px at 10% 10%, rgba(124,92,255,.25), transparent 60%),
                  radial-gradient(1000px 600px at 90% 30%, rgba(34,197,94,.18), transparent 60%),
                  var(--bg);
      color:var(--text);
    }
    header{
      padding:18px 22px; border-bottom:1px solid var(--border);
      display:flex; align-items:center; justify-content:space-between;
      backdrop-filter: blur(8px);
    }
    .brand{display:flex; gap:12px; align-items:center}
    .dot{width:10px;height:10px;border-radius:50%;background:var(--accent); box-shadow:0 0 20px rgba(124,92,255,.8)}
    .title{font-weight:700; letter-spacing:.3px}
    .sub{color:var(--muted); font-size:13px}
    .wrap{padding:18px; max-width:1200px; margin:0 auto}
    .grid{display:grid; grid-template-columns: 420px 1fr; gap:14px;}
    @media(max-width: 980px){ .grid{grid-template-columns:1fr} }
    .card{
      background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
      border:1px solid var(--border);
      border-radius:16px;
      overflow:hidden;
      box-shadow: 0 12px 35px rgba(0,0,0,.35);
    }
    .card-h{
      padding:14px; border-bottom:1px solid var(--border);
      display:flex; gap:10px; align-items:center; justify-content:space-between;
      background: rgba(18,26,51,.55);
    }
    .card-b{padding:12px}
    .row{
      padding:10px; border:1px solid var(--border); border-radius:12px; margin-bottom:10px; cursor:pointer;
      background: rgba(15,23,48,.7);
      transition: transform .08s ease, border-color .08s ease;
    }
    .row:hover{transform: translateY(-1px); border-color: rgba(124,92,255,.35)}
    .row .q{font-weight:600; font-size:13px; margin-bottom:6px}
    .meta{display:flex; gap:8px; flex-wrap:wrap; color:var(--muted); font-size:12px}
    .pill{padding:4px 8px; border-radius:999px; border:1px solid var(--border); background:rgba(255,255,255,.03)}
    .pill.good{border-color: rgba(34,197,94,.45)}
    .pill.warn{border-color: rgba(245,158,11,.5)}
    input, textarea{
      width:100%; padding:10px 12px; border-radius:12px;
      border:1px solid var(--border); background:rgba(15,23,48,.8);
      color:var(--text); outline:none;
    }
    textarea{min-height:84px; resize:vertical}
    input:focus, textarea:focus{border-color: rgba(124,92,255,.55)}
    .btn{
      padding:9px 11px; border-radius:12px; border:1px solid var(--border);
      background: rgba(255,255,255,.04); color: var(--text);
      cursor:pointer;
    }
    .btn:hover{border-color: rgba(124,92,255,.4)}
    .btn.primary{border-color: rgba(124,92,255,.6); background:rgba(124,92,255,.12)}
    .detail-title{font-weight:700}
    .k{color:var(--muted); font-size:12px}
    .v{font-size:13px}
    .kv{display:grid; grid-template-columns: 120px 1fr; gap:6px 10px; margin-top:10px}
    .tabs{display:flex; gap:8px; flex-wrap:wrap}
    .tab{padding:8px 10px; border-radius:12px; border:1px solid var(--border); background:rgba(255,255,255,.03); cursor:pointer}
    .tab.active{border-color: rgba(124,92,255,.6); background:rgba(124,92,255,.12)}
    pre{
      margin:0; padding:12px; border-radius:12px;
      background: rgba(0,0,0,.28);
      border:1px solid var(--border);
      overflow:auto; max-height: 420px;
      font-size:12px; line-height:1.45;
    }
    .empty{padding:14px; color:var(--muted)}
    .loading{opacity:.75}
    .split{display:flex; gap:10px; flex-wrap:wrap; margin-top:10px}
    .right-actions{display:flex; gap:8px; flex-wrap:wrap}
    .two{display:grid; grid-template-columns: 1fr 1fr; gap:10px}
    .toggle{display:flex; gap:10px; align-items:center; color:var(--muted); font-size:13px}
    .toggle input{width:auto}
  </style>
</head>
<body>
<header>
  <div class="brand">
    <div class="dot"></div>
    <div>
      <div class="title">Multi-Agent Dashboard</div>
      <div class="sub">Local LLM • RAG • Trace • Confidence</div>
    </div>
  </div>
  <div class="sub">FastAPI + Ollama + FAISS</div>
</header>

<div class="wrap">
  <div class="grid">
    <div class="card">
      <div class="card-h">
        <div style="width:100%">
          <div style="font-weight:700; margin-bottom:8px;">Ask a question</div>
          <textarea id="ask" placeholder="Type your question here…"></textarea>

          <div class="two" style="margin-top:10px;">
            <label class="toggle"><input type="checkbox" id="use_rag"/> Use RAG</label>
            <label class="toggle"><input type="checkbox" id="strict"/> Strict (Critic)</label>
          </div>

          <div class="split" style="margin-top:10px;">
            <button class="btn primary" onclick="runQuery()">Run</button>
            <button class="btn" onclick="fillExample()">Example</button>
            <button class="btn" onclick="clearAsk()">Clear</button>
          </div>
          <div class="sub" id="runStatus" style="margin-top:8px;"></div>
        </div>
      </div>

      <div class="card-b">
        <div style="font-weight:700; margin-bottom:8px;">Runs</div>
        <input id="search" placeholder="Search runs by query/answer… (press Enter)"/>

        <div class="split">
          <button class="btn" onclick="loadRuns()">Refresh</button>
          <button class="btn" onclick="clearSearch()">Clear</button>
        </div>

        <div id="runs" style="margin-top:12px;"></div>
      </div>
    </div>

    <div class="card">
      <div class="card-h">
        <div>
          <div class="detail-title">Run Detail</div>
          <div class="sub" id="detailSub">Select a run from the left.</div>
        </div>
        <div class="right-actions">
          <button class="btn" onclick="copyAnswer()">Copy Answer</button>
          <button class="btn" onclick="downloadRun()">Download JSON</button>
        </div>
      </div>
      <div class="card-b">
        <div class="kv">
          <div class="k">Run ID</div><div class="v" id="rid">—</div>
          <div class="k">Confidence</div><div class="v" id="conf">—</div>
          <div class="k">Mode</div><div class="v" id="mode">—</div>
          <div class="k">Query</div><div class="v" id="query">—</div>
        </div>

        <div style="margin-top:14px;" class="tabs">
          <div class="tab active" id="tabAnswer" onclick="showTab('answer')">Answer</div>
          <div class="tab" id="tabSources" onclick="showTab('sources')">Sources</div>
          <div class="tab" id="tabTrace" onclick="showTab('trace')">Trace</div>
        </div>

        <div style="margin-top:12px;" id="panelAnswer">
          <pre id="answerPre">—</pre>
        </div>

        <div style="margin-top:12px; display:none;" id="panelSources">
          <pre id="sourcesPre">—</pre>
        </div>

        <div style="margin-top:12px; display:none;" id="panelTrace">
          <pre id="tracePre">—</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
  let currentRun = null;

  function esc(s){
    return (s ?? '').toString()
      .replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
  }

  function pill(label, cls=''){
    return `<span class="pill ${cls}">${label}</span>`;
  }

  function confClass(c){
    if (c >= 0.75) return 'good';
    if (c >= 0.6) return '';
    return 'warn';
  }

  async function runQuery(){
    const q = document.getElementById('ask').value.trim();
    if (q.length < 3){
      document.getElementById('runStatus').textContent = 'Type a longer question (min 3 characters).';
      return;
    }

    const use_rag = document.getElementById('use_rag').checked;
    const strict = document.getElementById('strict').checked;

    document.getElementById('runStatus').textContent = 'Running…';
    try{
      const res = await fetch('/query', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({query: q, use_rag: use_rag, strict: strict})
      });
      const data = await res.json();
      if (!res.ok){
        document.getElementById('runStatus').textContent = 'Error: ' + (data.error || JSON.stringify(data));
        return;
      }
      document.getElementById('runStatus').textContent = 'Done. Run saved.';
      await loadRuns();
      await viewRun(data.run_id);
    } catch(e){
      document.getElementById('runStatus').textContent = 'Error: ' + e;
    }
  }

  function fillExample(){
    document.getElementById('ask').value = 'Explain multi-agent AI in simple words and give one real-world example.';
  }

  function clearAsk(){
    document.getElementById('ask').value = '';
    document.getElementById('runStatus').textContent = '';
  }

  async function loadRuns(){
    const runsDiv = document.getElementById('runs');
    runsDiv.innerHTML = `<div class="empty loading">Loading…</div>`;
    const q = document.getElementById('search').value.trim();

    let url = '/runs';
    if (q.length > 0) url = '/runs/search?q=' + encodeURIComponent(q);

    const res = await fetch(url);
    const runs = await res.json();

    if (!runs || runs.length === 0){
      runsDiv.innerHTML = `<div class="empty">No runs yet. Use the box above to run a query.</div>`;
      return;
    }

    runsDiv.innerHTML = '';
    runs.forEach(r => {
      const c = Number(r.confidence ?? 0);
      const mode = [
        r.use_rag ? pill('RAG') : pill('No-RAG'),
        r.strict ? pill('Strict') : pill('Fast')
      ].join(' ');

      const el = document.createElement('div');
      el.className = 'row';
      el.innerHTML = `
        <div class="q">${esc(r.query_preview || '—')}</div>
        <div class="meta">
          ${pill('Conf: ' + (c.toFixed ? c.toFixed(2) : c), confClass(c))}
          ${mode}
          ${r.created_at ? pill(new Date(r.created_at).toLocaleString()) : ''}
        </div>
      `;
      el.onclick = () => viewRun(r.run_id);
      runsDiv.appendChild(el);
    });
  }

  async function viewRun(id){
    document.getElementById('detailSub').textContent = 'Loading run…';
    const res = await fetch('/runs/' + id);
    const run = await res.json();
    currentRun = run;

    document.getElementById('detailSub').textContent = 'Loaded.';
    document.getElementById('rid').textContent = run.run_id || '—';
    document.getElementById('conf').textContent = (run.confidence ?? '—');
    document.getElementById('mode').textContent =
      `${run.use_rag ? 'RAG' : 'No-RAG'} • ${run.strict ? 'Strict' : 'Fast'}`;
    document.getElementById('query').textContent = run.user_query || '—';
    document.getElementById('answerPre').innerHTML = esc(run.final_answer || '—');

    const src = run.sources || [];
    if (src.length === 0){
      document.getElementById('sourcesPre').innerHTML = esc('No sources (RAG disabled or nothing retrieved).');
    } else {
      const lines = src.map((s, i) =>
        `[S${i+1}] ${s.source} (chunk ${s.chunk_id})\nScore: ${s.score}\n\n${s.text}\n`
      ).join('\n' + '-'.repeat(60) + '\n');
      document.getElementById('sourcesPre').innerHTML = esc(lines);
    }

    document.getElementById('tracePre').innerHTML = esc(JSON.stringify(run.trace || [], null, 2));
    showTab('answer');
  }

  function showTab(which){
    document.getElementById('panelAnswer').style.display = (which === 'answer') ? '' : 'none';
    document.getElementById('panelSources').style.display = (which === 'sources') ? '' : 'none';
    document.getElementById('panelTrace').style.display = (which === 'trace') ? '' : 'none';

    document.getElementById('tabAnswer').classList.toggle('active', which === 'answer');
    document.getElementById('tabSources').classList.toggle('active', which === 'sources');
    document.getElementById('tabTrace').classList.toggle('active', which === 'trace');
  }

  function clearSearch(){
    document.getElementById('search').value = '';
    loadRuns();
  }

  async function copyAnswer(){
    if (!currentRun) return;
    await navigator.clipboard.writeText(currentRun.final_answer || '');
    document.getElementById('detailSub').textContent = 'Copied answer to clipboard.';
  }

  function downloadRun(){
    if (!currentRun) return;
    const blob = new Blob([JSON.stringify(currentRun, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = (currentRun.run_id || 'run') + '.json';
    a.click();
    URL.revokeObjectURL(url);
  }

  document.getElementById('search').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') loadRuns();
  });

  loadRuns();
</script>
</body>
</html>
"""
    return html
