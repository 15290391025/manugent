"""Minimal HTML demo page for ManuGent."""

DEMO_HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ManuGent MES Agent Demo</title>
  <style>
    :root {
      --ink: #162016;
      --muted: #5d6b5c;
      --paper: #f8f3e7;
      --panel: #fffaf0;
      --line: #d9c9a5;
      --green: #1f6b4a;
      --orange: #bf6a2a;
      --red: #9d2f2f;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Georgia, "Noto Serif SC", "Songti SC", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at 20% 0%, rgba(191, 106, 42, 0.18), transparent 32rem),
        linear-gradient(135deg, #f8f3e7 0%, #ecdfc3 100%);
    }
    main {
      width: min(1180px, calc(100vw - 32px));
      margin: 32px auto;
      display: grid;
      gap: 20px;
    }
    .hero {
      border: 1px solid var(--line);
      background: rgba(255, 250, 240, 0.86);
      padding: 28px;
      box-shadow: 0 18px 60px rgba(41, 31, 15, 0.12);
    }
    h1 { margin: 0 0 8px; font-size: clamp(32px, 5vw, 64px); letter-spacing: -0.04em; }
    .tagline { color: var(--muted); font-size: 18px; max-width: 760px; line-height: 1.7; }
    .grid { display: grid; grid-template-columns: 0.95fr 1.3fr; gap: 20px; }
    .card {
      border: 1px solid var(--line);
      background: rgba(255, 250, 240, 0.9);
      padding: 20px;
      min-height: 180px;
    }
    label { display: block; font-weight: 700; margin-bottom: 8px; }
    input, textarea, button {
      width: 100%;
      border: 1px solid var(--line);
      background: #fffdf7;
      color: var(--ink);
      padding: 12px;
      font: inherit;
    }
    textarea { min-height: 110px; resize: vertical; }
    button {
      margin-top: 12px;
      background: var(--green);
      color: white;
      border: 0;
      cursor: pointer;
      font-weight: 700;
    }
    button:hover { filter: brightness(0.95); }
    .pill {
      display: inline-block;
      padding: 5px 10px;
      border: 1px solid var(--line);
      margin: 4px 4px 4px 0;
      color: var(--muted);
      background: #fffdf7;
      font-size: 13px;
    }
    .finding {
      padding: 16px;
      border-left: 5px solid var(--orange);
      background: #fff7e8;
      line-height: 1.7;
    }
    .evidence {
      display: grid;
      gap: 10px;
      margin-top: 14px;
    }
    .evidence-item {
      border: 1px solid var(--line);
      padding: 12px;
      background: #fffdf7;
    }
    .type { color: var(--green); font-weight: 700; text-transform: uppercase; font-size: 12px; }
    .approval { color: var(--red); font-weight: 700; }
    pre {
      white-space: pre-wrap;
      word-break: break-word;
      background: #1d211b;
      color: #f8f3e7;
      padding: 14px;
      overflow: auto;
      max-height: 260px;
    }
    @media (max-width: 840px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>ManuGent</h1>
      <div class="tagline">
        MES Agent 参考架构：用受控工具、证据链、记忆和企业审批边界，
        把传统 MES 数据变成可解释、可审计的制造业智能助手。
      </div>
      <div>
        <span class="pill">MES Tool Protocol</span>
        <span class="pill">Root Cause Workflow</span>
        <span class="pill">Evidence Chain</span>
        <span class="pill">Memory / Audit</span>
        <span class="pill">Approval Boundary</span>
      </div>
    </section>
    <section class="grid">
      <div class="card">
        <label for="line">产线</label>
        <input id="line" value="SMT-03" />
        <label for="question" style="margin-top:14px;">问题</label>
        <textarea id="question">SMT-03 最近 24 小时良率为什么下降？</textarea>
        <button onclick="runRca()">运行 RCA Workflow</button>
      </div>
      <div class="card">
        <h2>结论</h2>
        <div id="finding" class="finding">点击左侧按钮运行演示。</div>
        <h2>证据链</h2>
        <div id="evidence" class="evidence"></div>
      </div>
    </section>
    <section class="grid">
      <div class="card">
        <h2>建议动作</h2>
        <div id="actions"></div>
      </div>
      <div class="card">
        <h2>原始 JSON</h2>
        <pre id="raw">{}</pre>
      </div>
    </section>
  </main>
  <script>
    async function runRca() {
      const lineId = document.getElementById("line").value || "SMT-03";
      const response = await fetch("/workflows/root-cause/yield-drop", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          line_id: lineId,
          time_range: "24h",
          session_id: "web-demo"
        })
      });
      const data = await response.json();
      document.getElementById("raw").textContent = JSON.stringify(data, null, 2);
      document.getElementById("finding").textContent =
        `${data.finding} 置信度：${data.confidence}`;
      document.getElementById("evidence").innerHTML = data.evidence.map(item => `
        <div class="evidence-item">
          <div class="type">${item.type} · ${item.source_tool}</div>
          <div>${item.summary}</div>
        </div>
      `).join("");
      document.getElementById("actions").innerHTML = data.recommendations.map(item => `
        <div class="evidence-item">
          <div class="${item.requires_approval ? "approval" : "type"}">
            ${item.requires_approval ? "审批边界" : "建议"} · ${item.owner}
          </div>
          <div>${item.action}</div>
        </div>
      `).join("");
    }
  </script>
</body>
</html>
"""
