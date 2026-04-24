"""HTML demo page for ManuGent."""

DEMO_HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ManuGent MES Agent Command Center</title>
  <style>
    :root {
      --bg: #111816;
      --panel: rgba(244, 237, 216, 0.92);
      --panel-strong: #fbf4df;
      --ink: #14201c;
      --muted: #63716a;
      --line: rgba(32, 48, 42, 0.18);
      --green: #0f7b55;
      --green-deep: #084631;
      --amber: #d98a2b;
      --red: #b43c3c;
      --blue: #315d87;
      --shadow: 0 28px 90px rgba(0, 0, 0, 0.28);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      font-family: "Aptos", "Noto Sans SC", "PingFang SC", sans-serif;
      background:
        radial-gradient(circle at 12% 8%, rgba(217, 138, 43, 0.34), transparent 28rem),
        radial-gradient(circle at 88% 4%, rgba(15, 123, 85, 0.32), transparent 26rem),
        linear-gradient(135deg, #111816 0%, #27312c 48%, #d5c39d 100%);
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background-image:
        linear-gradient(rgba(255, 255, 255, 0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.045) 1px, transparent 1px);
      background-size: 44px 44px;
      mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.7), transparent);
    }

    .shell {
      width: min(1240px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 28px 0 44px;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      color: #f8f1dc;
      margin-bottom: 18px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 800;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .mark {
      width: 38px;
      height: 38px;
      display: grid;
      place-items: center;
      color: #f9f1d7;
      background: linear-gradient(135deg, var(--green), var(--amber));
      border: 1px solid rgba(255, 255, 255, 0.28);
      box-shadow: 0 14px 34px rgba(0, 0, 0, 0.24);
    }

    .status {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: flex-end;
      font-size: 13px;
    }

    .status span {
      padding: 8px 10px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      background: rgba(255, 255, 255, 0.08);
      backdrop-filter: blur(14px);
    }

    .hero {
      position: relative;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.24);
      background:
        linear-gradient(135deg, rgba(251, 244, 223, 0.96), rgba(235, 218, 177, 0.9)),
        radial-gradient(circle at 80% 18%, rgba(15, 123, 85, 0.18), transparent 24rem);
      box-shadow: var(--shadow);
      padding: clamp(26px, 4vw, 54px);
    }

    .hero::after {
      content: "";
      position: absolute;
      right: -80px;
      top: -110px;
      width: 340px;
      height: 340px;
      border: 1px solid rgba(15, 123, 85, 0.22);
      border-radius: 50%;
      box-shadow: inset 0 0 0 42px rgba(15, 123, 85, 0.06);
    }

    .eyebrow {
      color: var(--green);
      font-size: 13px;
      font-weight: 900;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      margin-bottom: 14px;
    }

    h1 {
      max-width: 880px;
      margin: 0;
      font-family: "Aptos Display", "Noto Serif SC", serif;
      font-size: clamp(44px, 7vw, 92px);
      line-height: 0.94;
      letter-spacing: -0.07em;
    }

    .tagline {
      max-width: 780px;
      margin: 22px 0 0;
      color: #43514a;
      font-size: clamp(16px, 2vw, 20px);
      line-height: 1.8;
    }

    .hero-grid {
      display: grid;
      grid-template-columns: 1fr 360px;
      gap: 26px;
      margin-top: 28px;
      align-items: end;
    }

    .pill-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .pill {
      padding: 9px 12px;
      border: 1px solid rgba(20, 32, 28, 0.14);
      background: rgba(255, 255, 255, 0.42);
      color: #33433c;
      font-size: 13px;
      font-weight: 700;
    }

    .hero-card {
      position: relative;
      z-index: 1;
      background: rgba(20, 32, 28, 0.9);
      color: #f9f1d7;
      padding: 18px;
      border: 1px solid rgba(255, 255, 255, 0.14);
    }

    .hero-card .label {
      color: #b8c8bd;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
    }

    .hero-card .value {
      margin-top: 10px;
      font-size: 34px;
      font-weight: 900;
      letter-spacing: -0.04em;
    }

    .layout {
      display: grid;
      grid-template-columns: 410px 1fr;
      gap: 18px;
      margin-top: 18px;
    }

    .panel {
      border: 1px solid rgba(255, 255, 255, 0.22);
      background: var(--panel);
      box-shadow: var(--shadow);
      padding: 20px;
    }

    .panel.dark {
      color: #f8f1dc;
      background: rgba(15, 24, 21, 0.86);
    }

    .section-title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }

    h2 {
      margin: 0;
      font-size: 18px;
      letter-spacing: -0.02em;
    }

    .hint {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
    }

    label {
      display: block;
      margin: 14px 0 8px;
      color: #31423b;
      font-size: 13px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    input,
    textarea,
    select,
    button {
      width: 100%;
      border: 1px solid var(--line);
      color: var(--ink);
      background: rgba(255, 255, 255, 0.72);
      padding: 13px 14px;
      font: inherit;
      outline: none;
    }

    input:focus,
    textarea:focus,
    select:focus {
      border-color: rgba(15, 123, 85, 0.66);
      box-shadow: 0 0 0 4px rgba(15, 123, 85, 0.1);
    }

    textarea {
      min-height: 124px;
      resize: vertical;
      line-height: 1.6;
    }

    button {
      margin-top: 16px;
      border: 0;
      color: #fff8e8;
      background: linear-gradient(135deg, var(--green), var(--green-deep));
      font-weight: 900;
      cursor: pointer;
      box-shadow: 0 16px 34px rgba(15, 123, 85, 0.28);
    }

    button:hover { transform: translateY(-1px); }
    button:disabled { cursor: wait; filter: grayscale(0.4); opacity: 0.74; }

    .metrics {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 18px;
    }

    .metric {
      padding: 16px;
      background: rgba(255, 255, 255, 0.58);
      border: 1px solid rgba(20, 32, 28, 0.12);
    }

    .metric small {
      display: block;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .metric strong {
      display: block;
      margin-top: 8px;
      font-size: 26px;
      letter-spacing: -0.04em;
    }

    .workflow {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
      margin-bottom: 18px;
    }

    .step {
      position: relative;
      min-height: 74px;
      padding: 12px;
      color: #31423b;
      background: rgba(255, 255, 255, 0.48);
      border: 1px solid rgba(20, 32, 28, 0.12);
      font-size: 12px;
      font-weight: 800;
    }

    .step.active {
      color: #fff8e8;
      background: linear-gradient(135deg, var(--green), #1d6a84);
    }

    .step span {
      display: block;
      margin-bottom: 8px;
      opacity: 0.72;
      font-size: 11px;
    }

    .finding {
      border-left: 6px solid var(--amber);
      background: rgba(255, 247, 230, 0.88);
      padding: 18px;
      line-height: 1.75;
      font-size: 16px;
    }

    .cards {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 14px;
    }

    .evidence-card,
    .action-card {
      background: rgba(255, 255, 255, 0.64);
      border: 1px solid rgba(20, 32, 28, 0.12);
      padding: 15px;
      min-height: 120px;
    }

    .type {
      color: var(--green);
      font-size: 12px;
      font-weight: 900;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 9px;
    }

    .approval { color: var(--red); }

    .summary {
      line-height: 1.65;
      color: #26352f;
    }

    .action-card {
      display: grid;
      gap: 10px;
      margin-bottom: 10px;
      min-height: auto;
    }

    .raw {
      max-height: 420px;
      overflow: auto;
      margin: 0;
      padding: 16px;
      color: #d9f7df;
      background: #0d1512;
      border: 1px solid rgba(255, 255, 255, 0.12);
      font-size: 12px;
      line-height: 1.6;
      white-space: pre-wrap;
      word-break: break-word;
    }

    .empty {
      display: grid;
      place-items: center;
      min-height: 280px;
      color: var(--muted);
      text-align: center;
      border: 1px dashed rgba(20, 32, 28, 0.18);
      background: rgba(255, 255, 255, 0.28);
    }

    .toast {
      display: none;
      margin-top: 12px;
      padding: 12px;
      color: #fff8e8;
      background: rgba(180, 60, 60, 0.92);
    }

    .toast.show { display: block; }

    @media (max-width: 980px) {
      .hero-grid,
      .layout { grid-template-columns: 1fr; }
      .workflow { grid-template-columns: 1fr 1fr; }
    }

    @media (max-width: 680px) {
      .shell { width: min(100vw - 20px, 1240px); padding-top: 14px; }
      .topbar { align-items: flex-start; flex-direction: column; }
      .metrics,
      .cards,
      .workflow { grid-template-columns: 1fr; }
      .hero,
      .panel { padding: 18px; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header class="topbar">
      <div class="brand">
        <div class="mark">MG</div>
        <div>ManuGent Command Center</div>
      </div>
      <div class="status">
        <span>MES Agent</span>
        <span>LangGraph RCA</span>
        <span>SQLite Memory</span>
      </div>
    </header>

    <section class="hero">
      <div class="eyebrow">MES + Agent Reference Architecture</div>
      <h1>把工厂现场数据变成可解释的 Agent 决策链路</h1>
      <p class="tagline">
        ManuGent 展示一个不侵入 MES 的 Agent 中间层：受控工具调用、证据链、
        多层记忆、LangGraph 根因分析，以及面向企业系统的安全边界。
      </p>
      <div class="hero-grid">
        <div class="pill-row">
          <span class="pill">Manufacturing Tool Protocol</span>
          <span class="pill">Evidence Chain</span>
          <span class="pill">Session Memory</span>
          <span class="pill">Audit Trail</span>
          <span class="pill">External Approval Boundary</span>
        </div>
        <div class="hero-card">
          <div class="label">Demo Scenario</div>
          <div class="value">SMT-03 RCA</div>
          <div class="hint" style="color:#cbd8ce;">
            production + quality + material + equipment + memory
          </div>
        </div>
      </div>
    </section>

    <section class="layout">
      <aside class="panel">
        <div class="section-title">
          <h2>运行根因分析</h2>
          <span class="hint">无需真实 MES</span>
        </div>

        <label for="line">产线</label>
        <select id="line">
          <option value="SMT-03">SMT-03 · 贴片三线</option>
          <option value="SMT-01">SMT-01 · 对照产线</option>
          <option value="ASM-01">ASM-01 · 组装线</option>
        </select>

        <label for="range">时间窗口</label>
        <select id="range">
          <option value="24h">最近 24 小时</option>
          <option value="7d">最近 7 天</option>
          <option value="today">今天</option>
        </select>

        <label for="question">业务问题</label>
        <textarea id="question">SMT-03 最近 24 小时良率为什么下降？</textarea>

        <button id="run-button" onclick="runRca()">运行 LangGraph RCA</button>
        <div id="error" class="toast"></div>

        <div style="margin-top:18px;" class="hint">
          这个页面调用 <code>/workflows/root-cause/yield-drop</code>，展示 Agent
          如何把 MES 数据组织成证据链，而不是让 LLM 自由猜测。
        </div>
      </aside>

      <main class="panel">
        <div class="metrics">
          <div class="metric">
            <small>Confidence</small>
            <strong id="confidence">--</strong>
          </div>
          <div class="metric">
            <small>Evidence</small>
            <strong id="evidence-count">--</strong>
          </div>
          <div class="metric">
            <small>Actions</small>
            <strong id="action-count">--</strong>
          </div>
        </div>

        <div class="workflow" id="workflow">
          <div class="step"><span>01</span>Production</div>
          <div class="step"><span>02</span>Quality</div>
          <div class="step"><span>03</span>Equipment</div>
          <div class="step"><span>04</span>Evidence</div>
          <div class="step"><span>05</span>Report</div>
        </div>

        <div class="section-title">
          <h2>分析结论</h2>
          <span class="hint" id="line-context">等待运行</span>
        </div>
        <div id="finding" class="finding">
          选择产线并运行 RCA，系统会查询良率、缺陷、物料批次、设备告警和历史记忆。
        </div>

        <div class="section-title" style="margin-top:20px;">
          <h2>证据链</h2>
          <span class="hint">typed evidence</span>
        </div>
        <div id="evidence" class="empty">
          证据卡片会在分析完成后显示。
        </div>
      </main>
    </section>

    <section class="layout">
      <div class="panel">
        <div class="section-title">
          <h2>建议动作</h2>
          <span class="hint">advisory / boundary</span>
        </div>
        <div id="actions" class="empty">建议动作会在分析完成后显示。</div>
      </div>

      <div class="panel dark">
        <div class="section-title">
          <h2>原始响应</h2>
          <span class="hint" style="color:#b8c8bd;">API JSON</span>
        </div>
        <pre id="raw" class="raw">{}</pre>
      </div>
    </section>
  </div>

  <script>
    const workflowSteps = document.querySelectorAll(".step");

    function setLoading(isLoading) {
      const button = document.getElementById("run-button");
      button.disabled = isLoading;
      button.textContent = isLoading ? "分析中..." : "运行 LangGraph RCA";
      workflowSteps.forEach(step => step.classList.toggle("active", isLoading));
    }

    function setError(message) {
      const error = document.getElementById("error");
      error.textContent = message || "";
      error.classList.toggle("show", Boolean(message));
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function renderReport(data, lineId, timeRange) {
      workflowSteps.forEach(step => step.classList.add("active"));
      document.getElementById("confidence").textContent =
        `${Math.round((data.confidence || 0) * 100)}%`;
      document.getElementById("evidence-count").textContent = data.evidence.length;
      document.getElementById("action-count").textContent = data.recommendations.length;
      document.getElementById("line-context").textContent = `${lineId} · ${timeRange}`;
      document.getElementById("finding").textContent = data.finding;
      document.getElementById("raw").textContent = JSON.stringify(data, null, 2);

      document.getElementById("evidence").className = "cards";
      document.getElementById("evidence").innerHTML = data.evidence.map(item => `
        <article class="evidence-card">
          <div class="type">${escapeHtml(item.type)} · ${escapeHtml(item.source_tool)}</div>
          <div class="summary">${escapeHtml(item.summary)}</div>
        </article>
      `).join("");

      document.getElementById("actions").className = "";
      document.getElementById("actions").innerHTML = data.recommendations.map(item => `
        <article class="action-card">
          <div class="type ${item.requires_approval ? "approval" : ""}">
            ${item.requires_approval ? "企业审批边界" : "建议动作"} · ${escapeHtml(item.owner)}
          </div>
          <div class="summary">${escapeHtml(item.action)}</div>
          <div class="hint">${escapeHtml(item.rationale || "基于证据链生成")}</div>
        </article>
      `).join("");
    }

    async function runRca() {
      const lineId = document.getElementById("line").value || "SMT-03";
      const timeRange = document.getElementById("range").value || "24h";
      setError("");
      setLoading(true);

      try {
        const response = await fetch("/workflows/root-cause/yield-drop", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            line_id: lineId,
            time_range: timeRange,
            session_id: "web-demo"
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        renderReport(data, lineId, timeRange);
      } catch (error) {
        setError(`RCA workflow 调用失败：${error.message}`);
      } finally {
        setLoading(false);
      }
    }
  </script>
</body>
</html>
"""
