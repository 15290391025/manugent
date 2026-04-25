"""HTML demo page for ManuGent."""

DEMO_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ManuGent MES Agent</title>
  <style>
    :root {
      --bg: #f7f7f8;
      --surface: #ffffff;
      --surface-soft: #f1f1f2;
      --text: #1f1f1f;
      --muted: #6f6f6f;
      --border: #e3e3e3;
      --accent: #10a37f;
      --accent-soft: #e7f5ef;
      --warning: #b7791f;
      --warning-soft: #fff6df;
      --danger: #c24141;
      --danger-soft: #fff0f0;
      --shadow: 0 18px 46px rgba(0, 0, 0, 0.08);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      background: var(--bg);
      font-family: ui-sans-serif, "Noto Sans SC", system-ui, -apple-system, sans-serif;
    }

    button,
    textarea {
      font: inherit;
    }

    .app {
      width: min(1080px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 24px 0 56px;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 78px;
      color: var(--muted);
      font-size: 14px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--text);
      font-weight: 650;
    }

    .mark {
      width: 30px;
      height: 30px;
      display: grid;
      place-items: center;
      border-radius: 9px;
      color: #fff;
      background: var(--accent);
      font-size: 14px;
      font-weight: 750;
    }

    .top-meta {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .top-meta span {
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.72);
    }

    .hero {
      max-width: 780px;
      margin: 0 auto;
      text-align: center;
    }

    h1 {
      margin: 0;
      color: var(--text);
      font-size: clamp(36px, 5.5vw, 58px);
      line-height: 1.08;
      letter-spacing: -0.055em;
      font-weight: 650;
      text-wrap: balance;
    }

    .subtitle {
      max-width: 620px;
      margin: 18px auto 0;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.7;
    }

    .composer {
      max-width: 780px;
      margin: 32px auto 0;
      border: 1px solid var(--border);
      border-radius: 26px;
      background: var(--surface);
      box-shadow: var(--shadow);
      overflow: hidden;
    }

    .input-row {
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: end;
      gap: 10px;
      padding: 10px;
    }

    textarea {
      width: 100%;
      min-height: 72px;
      max-height: 180px;
      resize: vertical;
      border: 0;
      outline: 0;
      color: var(--text);
      background: transparent;
      padding: 14px 16px;
      font-size: 16px;
      line-height: 1.65;
    }

    textarea::placeholder {
      color: #9a9a9a;
    }

    .run {
      width: 44px;
      height: 44px;
      border: 0;
      border-radius: 14px;
      color: #fff;
      background: var(--text);
      cursor: pointer;
      font-size: 18px;
      font-weight: 750;
    }

    .run:disabled {
      cursor: wait;
      opacity: 0.45;
    }

    .prompts {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      padding: 0 14px 14px;
    }

    .chip {
      border: 1px solid var(--border);
      border-radius: 999px;
      color: var(--muted);
      background: var(--surface);
      padding: 7px 10px;
      cursor: pointer;
      font-size: 13px;
    }

    .chip:hover {
      color: var(--text);
      background: var(--surface-soft);
    }

    .answer {
      display: grid;
      gap: 16px;
      margin: 34px auto 0;
      max-width: 980px;
    }

    .panel {
      border: 1px solid var(--border);
      border-radius: 22px;
      background: var(--surface);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
      overflow: hidden;
    }

    .panel-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 16px 18px;
      border-bottom: 1px solid var(--border);
    }

    .panel-head h2 {
      margin: 0;
      font-size: 15px;
      font-weight: 650;
    }

    .meta {
      color: var(--muted);
      font-size: 13px;
      text-align: right;
    }

    .summary {
      padding: 20px;
      font-size: clamp(18px, 2vw, 25px);
      line-height: 1.62;
      letter-spacing: -0.035em;
    }

    .line-wrap {
      padding: 30px 20px 24px;
      overflow-x: auto;
    }

    .line-stage {
      position: relative;
      min-width: 920px;
      display: grid;
      grid-template-columns: repeat(6, minmax(120px, 1fr));
      gap: 18px;
      padding-top: 6px;
    }

    .line-stage::before {
      content: "";
      position: absolute;
      left: 7%;
      right: 7%;
      top: 45px;
      height: 3px;
      border-radius: 999px;
      background: var(--border);
    }

    .station {
      position: relative;
      display: grid;
      justify-items: center;
      gap: 14px;
      z-index: 1;
    }

    .node-orb {
      width: 86px;
      height: 86px;
      border: 1px solid var(--border);
      border-radius: 50%;
      background:
        radial-gradient(circle at 34% 28%, rgba(255, 255, 255, 0.94), transparent 0.55rem),
        radial-gradient(circle at 68% 76%, rgba(16, 163, 127, 0.26), transparent 2.5rem),
        linear-gradient(145deg, #ffffff, #edf7f3);
      box-shadow:
        0 14px 34px rgba(0, 0, 0, 0.08),
        inset -12px -14px 24px rgba(0, 0, 0, 0.06),
        inset 10px 12px 18px rgba(255, 255, 255, 0.9);
    }

    .station.issue .node-orb {
      border-color: rgba(194, 65, 65, 0.35);
      background:
        radial-gradient(circle at 34% 28%, rgba(255, 255, 255, 0.94), transparent 0.55rem),
        radial-gradient(circle at 68% 76%, rgba(194, 65, 65, 0.3), transparent 2.5rem),
        linear-gradient(145deg, #ffffff, #fff0f0);
      box-shadow:
        0 14px 34px rgba(194, 65, 65, 0.14),
        inset -12px -14px 24px rgba(0, 0, 0, 0.05);
    }

    .station.signal .node-orb {
      border-color: rgba(183, 121, 31, 0.34);
      background:
        radial-gradient(circle at 34% 28%, rgba(255, 255, 255, 0.94), transparent 0.55rem),
        radial-gradient(circle at 68% 76%, rgba(183, 121, 31, 0.28), transparent 2.5rem),
        linear-gradient(145deg, #ffffff, #fff6df);
    }

    .node-label {
      width: 100%;
      padding: 12px;
      border: 1px solid var(--border);
      border-radius: 16px;
      background: #fff;
      text-align: center;
    }

    .station-code {
      color: var(--muted);
      font-size: 11px;
      font-weight: 650;
      letter-spacing: 0.05em;
    }

    .station-name {
      margin-top: 6px;
      color: var(--text);
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.03em;
    }

    .station-desc {
      margin-top: 6px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }

    .state {
      display: inline-flex;
      margin-top: 10px;
      padding: 5px 8px;
      border-radius: 999px;
      color: var(--accent);
      background: var(--accent-soft);
      font-size: 12px;
      font-weight: 650;
    }

    .state.issue {
      color: var(--danger);
      background: var(--danger-soft);
    }

    .state.signal {
      color: var(--warning);
      background: var(--warning-soft);
    }

    .node-note {
      margin-top: 10px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }

    .details {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    .list {
      display: grid;
      gap: 10px;
      padding: 14px;
    }

    .item {
      padding: 14px;
      border: 1px solid var(--border);
      border-radius: 16px;
      background: #fff;
    }

    .item-type {
      margin-bottom: 7px;
      color: var(--accent);
      font-size: 12px;
      font-weight: 700;
    }

    .item-type.boundary {
      color: var(--danger);
    }

    .item-text {
      color: #3f3f3f;
      font-size: 14px;
      line-height: 1.62;
    }

    .empty {
      padding: 46px 20px;
      color: var(--muted);
      text-align: center;
      line-height: 1.8;
    }

    .toast {
      display: none;
      position: fixed;
      left: 50%;
      bottom: 24px;
      z-index: 5;
      transform: translateX(-50%);
      max-width: min(520px, calc(100vw - 28px));
      padding: 12px 14px;
      border: 1px solid #ffd6d6;
      border-radius: 14px;
      color: var(--danger);
      background: #fff;
      box-shadow: var(--shadow);
    }

    .toast.show { display: block; }

    @media (max-width: 980px) {
      .line-stage {
        min-width: 0;
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
      .line-stage::before { display: none; }
      .details { grid-template-columns: 1fr; }
    }

    @media (max-width: 700px) {
      .topbar {
        align-items: flex-start;
        flex-direction: column;
        margin-bottom: 48px;
      }
      .hero { text-align: left; }
      .input-row { grid-template-columns: 1fr; }
      .run { width: 100%; }
      .line-stage { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <main class="app">
    <header class="topbar">
      <div class="brand">
        <div class="mark">M</div>
        <div>ManuGent</div>
      </div>
      <div class="top-meta">
        <span>MES Line Map</span>
        <span>LangGraph RCA</span>
        <span>Evidence Overlay</span>
      </div>
    </header>

    <section class="hero">
      <h1>问一句话，看懂整条产线。</h1>
      <p class="subtitle">
        用自然语言询问 MES，系统会把良率、缺陷、物料、设备和历史记忆
        映射到产线节点上。
      </p>
    </section>

    <section class="composer">
      <div class="input-row">
        <textarea
          id="question"
          placeholder="例如：SMT-03 最近 24 小时良率为什么下降？"
        >SMT-03 最近 24 小时良率为什么下降？</textarea>
        <button id="run-button" class="run" onclick="runRca()" aria-label="分析">
          ↑
        </button>
      </div>
      <div class="prompts">
        <button class="chip" onclick="useExample('SMT-03 最近 24 小时良率为什么下降？')">
          良率下降
        </button>
        <button class="chip" onclick="useExample('帮我分析 SMT-03 今天 AOI 缺陷集中在哪个环节')">
          AOI 缺陷
        </button>
        <button class="chip" onclick="useExample('SMT-03 最近是不是设备和物料一起影响了质量？')">
          设备 + 物料
        </button>
      </div>
    </section>

    <section id="answer" class="answer">
      <article class="panel">
        <div class="empty">
          输入一个 MES 现场问题后，系统会点亮产线节点，并给出证据链和建议动作。
        </div>
      </article>
    </section>
  </main>

  <div id="error" class="toast"></div>

  <script>
    const stations = [
      {
        id: "printer",
        code: "ST-01",
        name: "印刷",
        desc: "锡膏印刷 / 物料批次输入",
        evidenceTypes: ["material"]
      },
      {
        id: "spi",
        code: "ST-02",
        name: "SPI",
        desc: "锡膏厚度 / 早期质量信号",
        evidenceTypes: ["production", "quality", "material"]
      },
      {
        id: "mounter",
        code: "ST-03",
        name: "贴片",
        desc: "MOUNTER-03A / 吸嘴与飞达",
        evidenceTypes: ["equipment"]
      },
      {
        id: "reflow",
        code: "ST-04",
        name: "回流焊",
        desc: "温区曲线 / 焊接窗口",
        evidenceTypes: []
      },
      {
        id: "aoi",
        code: "ST-05",
        name: "AOI",
        desc: "缺陷检出 / 良率结果",
        evidenceTypes: ["quality", "production"]
      },
      {
        id: "pack",
        code: "ST-06",
        name: "包装",
        desc: "放行 / 返工 / 出货",
        evidenceTypes: []
      }
    ];

    function escapeHtml(value) {
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function inferLineId(question) {
      const match = question.match(/[A-Z]{2,5}-\\d{1,3}/i);
      return match ? match[0].toUpperCase() : "SMT-03";
    }

    function inferTimeRange(question) {
      if (question.includes("7天") || question.includes("一周")) return "7d";
      if (question.includes("今天")) return "today";
      return "24h";
    }

    function useExample(text) {
      document.getElementById("question").value = text;
      document.getElementById("question").focus();
    }

    function setLoading(isLoading) {
      const button = document.getElementById("run-button");
      button.disabled = isLoading;
      button.textContent = isLoading ? "…" : "↑";
    }

    function setError(message) {
      const error = document.getElementById("error");
      error.textContent = message || "";
      error.classList.toggle("show", Boolean(message));
    }

    function stationStatus(station, evidence) {
      const related = evidence.filter(item => station.evidenceTypes.includes(item.type));
      if (!related.length) return { status: "ok", related };
      if (related.some(item => ["quality", "equipment", "material"].includes(item.type))) {
        return { status: "issue", related };
      }
      return { status: "signal", related };
    }

    function renderLineMap(data) {
      const evidence = data.evidence || [];
      return stations.map(station => {
        const result = stationStatus(station, evidence);
        const stateText = {
          ok: "稳定",
          signal: "波动",
          issue: "异常关联"
        }[result.status];
        const note = result.related[0]?.summary || "当前问题未直接指向该节点。";

        return `
          <div class="station ${result.status}" data-station="${station.id}">
            <div class="node-orb" aria-hidden="true"></div>
            <div class="node-label">
              <div class="station-code">${station.code}</div>
              <div class="station-name">${station.name}</div>
              <div class="station-desc">${station.desc}</div>
              <div class="state ${result.status}">${stateText}</div>
              <div class="node-note">${escapeHtml(note)}</div>
            </div>
          </div>
        `;
      }).join("");
    }

    function renderEvidence(data) {
      return (data.evidence || []).map(item => `
        <div class="item">
          <div class="item-type">${escapeHtml(item.type)} · ${escapeHtml(item.source_tool)}</div>
          <div class="item-text">${escapeHtml(item.summary)}</div>
        </div>
      `).join("");
    }

    function renderActions(data) {
      return (data.recommendations || []).map(item => `
        <div class="item">
          <div class="item-type ${item.requires_approval ? "boundary" : ""}">
            ${item.requires_approval ? "生产控制边界" : "建议动作"} · ${escapeHtml(item.owner)}
          </div>
          <div class="item-text">${escapeHtml(item.action)}</div>
          <div class="item-text" style="color:var(--muted);margin-top:6px;">
            ${escapeHtml(item.rationale || "基于当前证据链生成。")}
          </div>
        </div>
      `).join("");
    }

    function renderReport(data, lineId, timeRange) {
      const confidence = Math.round((data.confidence || 0) * 100);
      document.getElementById("answer").innerHTML = `
        <article class="panel">
          <div class="panel-head">
            <h2>分析结论</h2>
            <span class="meta">${escapeHtml(lineId)} · ${escapeHtml(timeRange)}
              · ${confidence}%</span>
          </div>
          <div class="summary">${escapeHtml(data.finding)}</div>
        </article>

        <article class="panel">
          <div class="panel-head">
            <h2>产线节点</h2>
            <span class="meta">证据会落到对应工序</span>
          </div>
          <div class="line-wrap">
            <div class="line-stage">${renderLineMap(data)}</div>
          </div>
        </article>

        <section class="details">
          <article class="panel">
            <div class="panel-head">
              <h2>证据链</h2>
              <span class="meta">${(data.evidence || []).length} 条</span>
            </div>
            <div class="list">${renderEvidence(data)}</div>
          </article>
          <article class="panel">
            <div class="panel-head">
              <h2>建议动作</h2>
              <span class="meta">${(data.recommendations || []).length} 条</span>
            </div>
            <div class="list">${renderActions(data)}</div>
          </article>
        </section>
      `;
    }

    async function runRca() {
      const question = document.getElementById("question").value.trim();
      const lineId = inferLineId(question);
      const timeRange = inferTimeRange(question);

      if (!question) {
        setError("请先输入一个 MES 现场问题。");
        return;
      }

      setError("");
      setLoading(true);

      try {
        const response = await fetch("/workflows/root-cause/yield-drop", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            line_id: lineId,
            time_range: timeRange,
            session_id: "web-demo"
          })
        });

        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        renderReport(data, lineId, timeRange);
      } catch (error) {
        setError(`分析失败：${error.message}`);
      } finally {
        setLoading(false);
      }
    }

    document.getElementById("question").addEventListener("keydown", event => {
      if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
        runRca();
      }
    });
  </script>
</body>
</html>
"""
