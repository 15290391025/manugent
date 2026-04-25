"""HTML demo page for ManuGent."""

DEMO_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ManuGent MES Agent</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/p5.min.js"></script>
  <style>
    :root {
      --bg: #08090a;
      --surface: rgba(15, 16, 17, 0.78);
      --surface-strong: rgba(25, 26, 27, 0.94);
      --line: rgba(255, 255, 255, 0.08);
      --line-strong: rgba(255, 255, 255, 0.16);
      --text: #f7f8f8;
      --muted: #8a8f98;
      --soft: #d0d6e0;
      --violet: #7170ff;
      --green: #27a644;
      --amber: #ffb84d;
      --red: #ff6b6b;
      --shadow: 0 28px 90px rgba(0, 0, 0, 0.45);
    }

    * {
      box-sizing: border-box;
    }

    html {
      background: var(--bg);
    }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      background:
        radial-gradient(circle at 20% -10%, rgba(113, 112, 255, 0.24), transparent 32rem),
        radial-gradient(circle at 80% 0%, rgba(39, 166, 68, 0.12), transparent 28rem),
        linear-gradient(180deg, #08090a 0%, #0f1011 58%, #08090a 100%);
      font-family: Inter, "Noto Sans SC", system-ui, sans-serif;
      font-feature-settings: "cv01", "ss03";
      overflow-x: hidden;
    }

    #factory-field {
      position: fixed;
      inset: 0;
      z-index: 0;
      pointer-events: none;
      opacity: 0.78;
    }

    .shell {
      position: relative;
      z-index: 1;
      width: min(1200px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 24px 0 48px;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 74px;
      color: var(--soft);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 14px;
      font-weight: 600;
      letter-spacing: -0.02em;
    }

    .mark {
      width: 26px;
      height: 26px;
      display: grid;
      place-items: center;
      border: 1px solid var(--line-strong);
      border-radius: 8px;
      color: white;
      background: rgba(113, 112, 255, 0.22);
      box-shadow: 0 0 24px rgba(113, 112, 255, 0.28);
      font-family: "JetBrains Mono", ui-monospace, monospace;
      font-size: 12px;
    }

    .top-meta {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .top-meta span {
      padding: 6px 9px;
      border: 1px solid var(--line);
      border-radius: 999px;
      color: var(--muted);
      background: rgba(255, 255, 255, 0.025);
      font-size: 12px;
    }

    .hero {
      max-width: 900px;
      margin: 0 auto 22px;
      text-align: center;
    }

    h1 {
      margin: 0;
      font-size: clamp(46px, 8vw, 90px);
      font-weight: 500;
      line-height: 0.96;
      letter-spacing: -0.075em;
      color: #f7f8f8;
      text-wrap: balance;
    }

    .subtitle {
      max-width: 670px;
      margin: 22px auto 0;
      color: var(--muted);
      font-size: 17px;
      line-height: 1.8;
      letter-spacing: -0.01em;
    }

    .ask {
      max-width: 850px;
      margin: 32px auto 0;
      border: 1px solid var(--line-strong);
      border-radius: 26px;
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.025)),
        rgba(15, 16, 17, 0.8);
      box-shadow: var(--shadow), inset 0 1px 0 rgba(255, 255, 255, 0.06);
      backdrop-filter: blur(20px);
      overflow: hidden;
    }

    .input-row {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      align-items: end;
      padding: 12px;
    }

    textarea {
      width: 100%;
      min-height: 82px;
      max-height: 190px;
      resize: vertical;
      border: 0;
      outline: 0;
      color: var(--text);
      background: transparent;
      padding: 16px 18px;
      font: inherit;
      font-size: 17px;
      line-height: 1.7;
    }

    textarea::placeholder {
      color: #62666d;
    }

    .run {
      width: 74px;
      height: 56px;
      border: 0;
      border-radius: 18px;
      color: white;
      background: linear-gradient(135deg, #5e6ad2, #7170ff);
      cursor: pointer;
      font: 700 14px Inter, sans-serif;
      box-shadow: 0 16px 34px rgba(113, 112, 255, 0.28);
    }

    .run:disabled {
      cursor: wait;
      opacity: 0.56;
    }

    .prompts {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      padding: 0 14px 14px;
    }

    .chip {
      border: 1px solid var(--line);
      border-radius: 999px;
      color: var(--muted);
      background: rgba(255, 255, 255, 0.025);
      padding: 7px 10px;
      cursor: pointer;
      font: 500 12px Inter, sans-serif;
    }

    .chip:hover {
      color: var(--soft);
      border-color: rgba(113, 112, 255, 0.35);
      background: rgba(113, 112, 255, 0.08);
    }

    .answer {
      display: grid;
      gap: 16px;
      margin-top: 28px;
    }

    .panel {
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--surface);
      box-shadow: 0 18px 60px rgba(0, 0, 0, 0.28);
      backdrop-filter: blur(20px);
      overflow: hidden;
    }

    .panel-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      padding: 16px 18px;
      border-bottom: 1px solid var(--line);
    }

    .panel-head h2 {
      margin: 0;
      color: var(--text);
      font-size: 14px;
      font-weight: 600;
      letter-spacing: -0.01em;
    }

    .meta {
      color: var(--muted);
      font-size: 12px;
      text-align: right;
    }

    .summary {
      padding: 22px;
      color: #e9ecef;
      font-size: clamp(20px, 2.2vw, 29px);
      font-weight: 400;
      line-height: 1.55;
      letter-spacing: -0.045em;
    }

    .line-wrap {
      padding: 22px;
    }

    .line-stage {
      position: relative;
      display: grid;
      grid-template-columns: repeat(6, minmax(130px, 1fr));
      gap: 12px;
    }

    .line-stage::before {
      content: "";
      position: absolute;
      left: 5%;
      right: 5%;
      top: 44px;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(113, 112, 255, 0.5), transparent);
    }

    .station {
      position: relative;
      min-height: 190px;
      padding: 15px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.052), rgba(255, 255, 255, 0.02)),
        #111214;
      overflow: hidden;
    }

    .station::before {
      content: "";
      position: absolute;
      inset: -1px;
      border-radius: 18px;
      opacity: 0;
      pointer-events: none;
      background: radial-gradient(circle at 65% 10%, rgba(113, 112, 255, 0.32), transparent 8rem);
      transition: opacity 0.25s ease;
    }

    .station.issue {
      border-color: rgba(255, 107, 107, 0.48);
      box-shadow: inset 0 0 0 1px rgba(255, 107, 107, 0.08);
    }

    .station.issue::before {
      opacity: 1;
      background: radial-gradient(circle at 75% 8%, rgba(255, 107, 107, 0.26), transparent 8rem);
    }

    .station.signal {
      border-color: rgba(255, 184, 77, 0.4);
    }

    .station.signal::before {
      opacity: 1;
      background: radial-gradient(circle at 75% 8%, rgba(255, 184, 77, 0.2), transparent 8rem);
    }

    .station.ok {
      border-color: rgba(39, 166, 68, 0.18);
    }

    .station-content {
      position: relative;
      z-index: 1;
    }

    .station-index {
      color: var(--muted);
      font-family: "JetBrains Mono", ui-monospace, monospace;
      font-size: 11px;
    }

    .station-name {
      margin-top: 10px;
      color: var(--text);
      font-size: 20px;
      font-weight: 600;
      letter-spacing: -0.04em;
    }

    .station-desc {
      margin-top: 7px;
      min-height: 38px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.55;
    }

    .state {
      display: inline-flex;
      margin-top: 11px;
      padding: 5px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.05);
    }

    .state.issue {
      color: #ffd6d6;
      background: rgba(255, 107, 107, 0.16);
    }

    .state.signal {
      color: #ffe2b2;
      background: rgba(255, 184, 77, 0.14);
    }

    .state.ok {
      color: #c8f6d2;
      background: rgba(39, 166, 68, 0.12);
    }

    .node-note {
      margin-top: 12px;
      color: var(--soft);
      font-size: 12px;
      line-height: 1.58;
    }

    .details {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    .list {
      display: grid;
      gap: 10px;
      padding: 16px;
    }

    .item {
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.028);
    }

    .item-type {
      margin-bottom: 7px;
      color: var(--violet);
      font-family: "JetBrains Mono", ui-monospace, monospace;
      font-size: 11px;
      text-transform: uppercase;
    }

    .item-type.boundary {
      color: var(--red);
    }

    .item-text {
      color: var(--soft);
      font-size: 13px;
      line-height: 1.65;
    }

    .empty {
      padding: 46px 18px;
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
      border: 1px solid rgba(255, 107, 107, 0.32);
      border-radius: 14px;
      color: #ffecec;
      background: rgba(80, 24, 24, 0.92);
      box-shadow: 0 16px 50px rgba(0, 0, 0, 0.3);
    }

    .toast.show {
      display: block;
    }

    @media (max-width: 1040px) {
      .line-stage {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .line-stage::before {
        display: none;
      }
    }

    @media (max-width: 760px) {
      .topbar {
        align-items: flex-start;
        flex-direction: column;
        margin-bottom: 48px;
      }

      .input-row,
      .details {
        grid-template-columns: 1fr;
      }

      .run {
        width: 100%;
      }

      .line-stage {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div id="factory-field"></div>

  <main class="shell">
    <header class="topbar">
      <div class="brand">
        <div class="mark">M</div>
        <div>ManuGent</div>
      </div>
      <div class="top-meta">
        <span>MES Agent</span>
        <span>LangGraph RCA</span>
        <span>Line Digital Twin</span>
      </div>
    </header>

    <section class="hero">
      <h1>Ask the line. See the root cause.</h1>
      <p class="subtitle">
        用一句自然语言询问 MES，系统把良率、质量、物料、设备与历史记忆
        编排成证据链，并把异常定位到整条产线的具体节点。
      </p>
    </section>

    <section class="ask">
      <div class="input-row">
        <textarea
          id="question"
          placeholder="例如：SMT-03 最近 24 小时良率为什么下降？"
        >SMT-03 最近 24 小时良率为什么下降？</textarea>
        <button id="run-button" class="run" onclick="runRca()">分析</button>
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
          输入 MES 现场问题后，产线会被点亮，异常证据和建议会挂到对应工序节点。
        </div>
      </article>
    </section>
  </main>

  <div id="error" class="toast"></div>

  <script>
    window.manuState = { active: false, issueNodes: [] };

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
      button.textContent = isLoading ? "分析中" : "分析";
      window.manuState.active = isLoading;
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
      const issueNodes = [];
      const html = stations.map(station => {
        const result = stationStatus(station, evidence);
        const stateText = {
          ok: "链路正常",
          signal: "指标波动",
          issue: "问题关联"
        }[result.status];
        const note = result.related[0]?.summary || "当前问题未直接指向该节点。";
        if (result.status === "issue") issueNodes.push(station.id);

        return `
          <div class="station ${result.status}" data-station="${station.id}">
            <div class="station-content">
              <div class="station-index">${station.code}</div>
              <div class="station-name">${station.name}</div>
              <div class="station-desc">${station.desc}</div>
              <div class="state ${result.status}">${stateText}</div>
              <div class="node-note">${escapeHtml(note)}</div>
            </div>
          </div>
        `;
      }).join("");
      window.manuState.issueNodes = issueNodes;
      return html;
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
            <h2>AI 分析结论</h2>
            <span class="meta">${escapeHtml(lineId)} · ${escapeHtml(timeRange)}
              · ${confidence}% confidence</span>
          </div>
          <div class="summary">${escapeHtml(data.finding)}</div>
        </article>

        <article class="panel">
          <div class="panel-head">
            <h2>产线数字孪生视图</h2>
            <span class="meta">异常证据会落到具体工序节点</span>
          </div>
          <div class="line-wrap">
            <div class="line-stage">${renderLineMap(data)}</div>
          </div>
        </article>

        <section class="details">
          <article class="panel">
            <div class="panel-head">
              <h2>证据链</h2>
              <span class="meta">${(data.evidence || []).length} records</span>
            </div>
            <div class="list">${renderEvidence(data)}</div>
          </article>
          <article class="panel">
            <div class="panel-head">
              <h2>建议动作</h2>
              <span class="meta">${(data.recommendations || []).length} actions</span>
            </div>
            <div class="list">${renderActions(data)}</div>
          </article>
        </section>
      `;
      window.manuState.active = true;
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
        window.manuState.active = false;
      } finally {
        setLoading(false);
      }
    }

    document.getElementById("question").addEventListener("keydown", event => {
      if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
        runRca();
      }
    });

    let streams = [];

    function setup() {
      const canvas = createCanvas(windowWidth, windowHeight);
      canvas.parent("factory-field");
      pixelDensity(1);
      for (let i = 0; i < 46; i++) {
        streams.push({
          x: random(width),
          y: random(height),
          speed: random(0.35, 1.2),
          size: random(1.2, 2.8),
          phase: random(TAU)
        });
      }
    }

    function draw() {
      clear();
      noFill();
      stroke(113, 112, 255, 14);
      strokeWeight(1);
      for (let x = -40; x < width + 40; x += 70) line(x, 0, x + 120, height);
      for (let y = 80; y < height; y += 86) line(0, y, width, y + 18);

      const activeBoost = window.manuState.active ? 1.8 : 1;
      for (const stream of streams) {
        stream.x += stream.speed * activeBoost;
        stream.y += sin(frameCount * 0.012 + stream.phase) * 0.16;
        if (stream.x > width + 20) {
          stream.x = -20;
          stream.y = random(height);
        }

        const glow = window.manuState.active ? 120 : 58;
        noStroke();
        fill(113, 112, 255, glow);
        circle(stream.x, stream.y, stream.size);
        fill(39, 166, 68, glow * 0.42);
        circle(stream.x - 18, stream.y + 9, stream.size * 0.7);
      }

      if (window.manuState.issueNodes.length) {
        const pulse = 40 + sin(frameCount * 0.06) * 28;
        fill(255, 107, 107, pulse);
        noStroke();
        circle(width * 0.74, height * 0.22, 160 + pulse);
      }
    }

    function windowResized() {
      resizeCanvas(windowWidth, windowHeight);
    }
  </script>
</body>
</html>
"""
