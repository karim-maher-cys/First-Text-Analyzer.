import html
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from transformers import pipeline
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="SentinEL // Privacy-First Text Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Custom CSS & Futuristic Cyber-Glass Styling
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Import futuristic & tech fonts */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap');

:root {
    --bg-dark: #0a0e1a;
    --card-bg: rgba(15, 23, 42, 0.75);
    --card-border: rgba(56, 189, 248, 0.15);
    --cyan-glow: #06b6d4;
    --cyan-bright: #22d3ee;
    --emerald-glow: #10b981;
    --purple-glow: #a855f7;
    --rose-glow: #f43f5e;
    --amber-glow: #f59e0b;
}

/* Base App Theme */
.stApp {
    background: radial-gradient(circle at 15% 15%, rgba(14, 165, 233, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 75%, rgba(168, 85, 247, 0.07) 0%, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.04) 0%, transparent 60%),
                #070a12 !important;
    font-family: 'Outfit', sans-serif !important;
    color: #e2e8f0;
}

/* Hide default streamlit top decoration bar */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: rgba(10, 15, 29, 0.92) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.07);
}

/* Futuristic Sidebar Card */
.sidebar-panel {
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    position: relative;
    overflow: hidden;
}

.sidebar-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #06b6d4, #a855f7, #10b981);
    animation: scanline 3s linear infinite;
}

@keyframes scanline {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Headings */
h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.02em;
    color: #f8fafc !important;
}

/* Custom Cyber Cards */
.cyber-card {
    background: var(--card-bg);
    backdrop-filter: blur(16px);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.06);
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    animation: fadeInSlide 0.5s ease-out;
}

.cyber-card:hover {
    border-color: rgba(34, 211, 238, 0.4);
    box-shadow: 0 14px 35px -8px rgba(6, 182, 212, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.12);
    transform: translateY(-2px);
}

@keyframes fadeInSlide {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Sentiment Result Cards */
.sentiment-card {
    border-radius: 16px;
    padding: 22px;
    display: flex;
    align-items: center;
    gap: 18px;
    position: relative;
    overflow: hidden;
    animation: pulseBorder 3s infinite alternate;
}

.sentiment-positive {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.08) 100%);
    border: 1px solid rgba(16, 185, 129, 0.35);
    box-shadow: 0 8px 30px rgba(16, 185, 129, 0.15);
}

.sentiment-negative {
    background: linear-gradient(135deg, rgba(244, 63, 94, 0.15) 0%, rgba(217, 70, 239, 0.08) 100%);
    border: 1px solid rgba(244, 63, 94, 0.35);
    box-shadow: 0 8px 30px rgba(244, 63, 94, 0.15);
}

.sentiment-icon {
    font-size: 2.8rem;
    filter: drop-shadow(0 0 12px currentColor);
    animation: floatIcon 3s ease-in-out infinite;
}

@keyframes floatIcon {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
}

/* Anonymized Monospace Box */
.redacted-box {
    background: #080d1a;
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 12px;
    padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    line-height: 1.7;
    color: #e2e8f0;
    white-space: pre-wrap;
    word-break: break-word;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.6);
}

/* PII Tag Badges in Highlighted Text */
.pii-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 2px 8px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.86rem;
    font-weight: 600;
    margin: 0 2px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
    animation: glowTag 2s infinite alternate;
}

.pii-badge small {
    font-size: 0.68rem;
    padding: 1px 4px;
    border-radius: 4px;
    background: rgba(0, 0, 0, 0.35);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Distinct Glowing Colors per Entity */
.pii-person {
    background: rgba(59, 130, 246, 0.22);
    color: #93c5fd;
    border-color: rgba(59, 130, 246, 0.5);
}
.pii-email_address {
    background: rgba(168, 85, 247, 0.22);
    color: #d8b4fe;
    border-color: rgba(168, 85, 247, 0.5);
}
.pii-phone_number {
    background: rgba(245, 158, 11, 0.22);
    color: #fcd34d;
    border-color: rgba(245, 158, 11, 0.5);
}
.pii-location {
    background: rgba(16, 185, 129, 0.22);
    color: #6ee7b7;
    border-color: rgba(16, 185, 129, 0.5);
}
.pii-credit_card, .pii-crypto, .pii-iban_code {
    background: rgba(244, 63, 94, 0.25);
    color: #fda4af;
    border-color: rgba(244, 63, 94, 0.6);
}
.pii-date_time {
    background: rgba(20, 184, 166, 0.22);
    color: #5eead4;
    border-color: rgba(20, 184, 166, 0.5);
}
.pii-default {
    background: rgba(6, 182, 212, 0.22);
    color: #67e8f9;
    border-color: rgba(6, 182, 212, 0.5);
}

/* Streamlit Tabs Customization */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 14px;
    padding: 6px;
    gap: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 10px 24px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    color: #94a3b8 !important;
    border: 1px solid transparent;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #38bdf8 !important;
    background: rgba(56, 189, 248, 0.08);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(168, 85, 247, 0.2)) !important;
    border: 1px solid rgba(34, 211, 238, 0.4) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.25);
}

/* Primary Button Styling */
div.stButton > button {
    background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%) !important;
    background-size: 200% auto !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    box-shadow: 0 4px 20px rgba(6, 182, 212, 0.35) !important;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    text-transform: uppercase;
    font-size: 0.9rem;
}

div.stButton > button:hover {
    background-position: right center !important;
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 30px rgba(59, 130, 246, 0.5) !important;
}

div.stButton > button:active {
    transform: translateY(1px) scale(0.99) !important;
}

/* Secondary Buttons (Presets) */
button[kind="secondary"] {
    background: rgba(30, 41, 59, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: #cbd5e1 !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

button[kind="secondary"]:hover {
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
    background: rgba(56, 189, 248, 0.1) !important;
}

/* Text Area & Input Styling */
div[data-testid="stTextArea"] textarea {
    background: rgba(11, 17, 32, 0.85) !important;
    border: 1px solid rgba(56, 189, 248, 0.2) !important;
    border-radius: 14px !important;
    color: #f1f5f9 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5) !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #06b6d4 !important;
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.35), inset 0 2px 8px rgba(0, 0, 0, 0.5) !important;
}

/* Progress bar styling */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #06b6d4, #10b981, #a855f7) !important;
    box-shadow: 0 0 12px rgba(6, 182, 212, 0.6);
}

/* Stat counter pills */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.85rem;
    font-weight: 500;
}

.stat-pill-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 8px #10b981;
    animation: pulseDot 2s infinite;
}

@keyframes pulseDot {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.4); opacity: 0.6; }
}

/* Modern Dataframe */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.08);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Interactive Cyber Canvas & Particle Mesh Header (HTML/JS)
# ---------------------------------------------------------
HERO_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        background: transparent;
        overflow: hidden;
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #fff;
    }
    #hero-container {
        position: relative;
        width: 100%;
        height: 140px;
        border-radius: 18px;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(7, 10, 18, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 32px;
    }
    #particle-canvas {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
        pointer-events: auto;
    }
    .hero-content {
        position: relative;
        z-index: 2;
        pointer-events: none;
    }
    .badge-row {
        display: flex;
        gap: 10px;
        margin-bottom: 8px;
    }
    .cyber-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        background: rgba(6, 182, 212, 0.15);
        color: #22d3ee;
        border: 1px solid rgba(34, 211, 238, 0.4);
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.2);
    }
    .hero-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 0%, #38bdf8 60%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }
    .hero-sub {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 4px;
        font-weight: 400;
    }
    .shield-art {
        position: relative;
        z-index: 2;
        width: 72px;
        height: 72px;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: none;
    }
    .shield-ring {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 2px dashed rgba(6, 182, 212, 0.4);
        animation: spinRing 12s linear infinite;
    }
    .shield-pulse {
        position: absolute;
        width: 80%;
        height: 80%;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.25) 0%, transparent 70%);
        animation: pulseShield 2s infinite alternate;
    }
    @keyframes spinRing {
        100% { transform: rotate(360deg); }
    }
    @keyframes pulseShield {
        0% { transform: scale(0.9); opacity: 0.5; }
        100% { transform: scale(1.15); opacity: 1; }
    }
</style>
</head>
<body>
<div id="hero-container">
    <canvas id="particle-canvas"></canvas>
    <div class="hero-content">
        <div class="badge-row">
            <span class="cyber-badge">
                <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10b981; box-shadow:0 0 6px #10b981;"></span>
                Local Presidio Engine
            </span>
            <span class="cyber-badge" style="background:rgba(168,85,247,0.15); color:#c084fc; border-color:rgba(192,132,252,0.4);">
                Hugging Face SST-2
            </span>
            <span class="cyber-badge" style="background:rgba(16,185,129,0.15); color:#6ee7b7; border-color:rgba(110,231,183,0.4);">
                Zero-Leak Privacy
            </span>
        </div>
        <div class="hero-title">SentinEL // Privacy-First Text Analyzer</div>
        <div class="hero-sub">Real-time PII anonymization & cryptographic-grade redaction paired with deep sentiment telemetry.</div>
    </div>
    <div class="shield-art">
        <div class="shield-ring"></div>
        <div class="shield-pulse"></div>
        <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 8px #06b6d4);">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <path d="m9 12 2 2 4-4"/>
        </svg>
    </div>
</div>

<script>
const canvas = document.getElementById('particle-canvas');
const ctx = canvas.getContext('2d');
let width, height;
let particles = [];
let mouse = { x: null, y: null, maxDist: 100 };

function resize() {
    width = canvas.width = canvas.parentElement.offsetWidth;
    height = canvas.height = canvas.parentElement.offsetHeight;
}
window.addEventListener('resize', resize);
resize();

class Particle {
    constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.8;
        this.vy = (Math.random() - 0.5) * 0.8;
        this.radius = Math.random() * 1.8 + 1;
        this.baseColor = Math.random() > 0.4 ? 'rgba(34, 211, 238,' : 'rgba(168, 85, 247,';
    }
    update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;

        if (mouse.x !== null) {
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < mouse.maxDist) {
                this.x -= (dx / dist) * 1.5;
                this.y -= (dy / dist) * 1.5;
            }
        }
    }
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.baseColor + '0.7)';
        ctx.shadowColor = '#06b6d4';
        ctx.shadowBlur = 4;
        ctx.fill();
        ctx.shadowBlur = 0;
    }
}

for (let i = 0; i < 45; i++) {
    particles.push(new Particle());
}

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
});
canvas.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
});

function animate() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
            let dx = particles[i].x - particles[j].x;
            let dy = particles[i].y - particles[j].y;
            let dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 85) {
                ctx.beginPath();
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                let opacity = (1 - dist / 85) * 0.25;
                ctx.strokeStyle = `rgba(34, 211, 238, ${opacity})`;
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }
    }

    particles.forEach(p => {
        p.update();
        p.draw();
    });

    requestAnimationFrame(animate);
}
animate();
</script>
</body>
</html>
"""

components.html(HERO_HTML, height=155)


# ---------------------------------------------------------
# Model Loader Cached Function
# ---------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_models():
    with st.spinner("Initializing Deep Learning Neural Pipelines..."):
        clf = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        )
        analyzer = AnalyzerEngine()
        anonymizer = AnonymizerEngine()
    return clf, analyzer, anonymizer


clf, analyzer, anonymizer = load_models()


# ---------------------------------------------------------
# Core Helper Functions
# ---------------------------------------------------------
def redact(text, threshold):
    results = analyzer.analyze(text=text, language="en", score_threshold=threshold)
    clean = anonymizer.anonymize(text=text, analyzer_results=results).text
    return clean, results


def build_highlighted_html(original_text, results):
    """Wraps detected PII entities in styled neon cyber tags."""
    if not results:
        return f'<div class="redacted-box">{html.escape(original_text)}</div>'

    # Filter overlaps by sorting and keeping distinct intervals
    sorted_res = sorted(results, key=lambda x: x.start)
    merged_results = []
    last_end = -1
    for r in sorted_res:
        if r.start >= last_end:
            merged_results.append(r)
            last_end = r.end

    html_parts = []
    curr = 0
    for r in merged_results:
        # Unflagged segment
        if r.start > curr:
            html_parts.append(html.escape(original_text[curr : r.start]))

        entity_text = html.escape(original_text[r.start : r.end])
        etype = r.entity_type
        css_type = etype.lower()

        # Fallback class if not specialized
        supported = [
            "person",
            "email_address",
            "phone_number",
            "location",
            "credit_card",
            "date_time",
            "crypto",
            "iban_code",
        ]
        class_name = f"pii-{css_type}" if css_type in supported else "pii-default"

        tag = f"""<span class="pii-badge {class_name}" title="Confidence: {r.score:.0%}">
            {entity_text} <small>{etype}</small>
        </span>"""
        html_parts.append(tag)
        curr = r.end

    if curr < len(original_text):
        html_parts.append(html.escape(original_text[curr:]))

    return f'<div class="redacted-box">{"".join(html_parts)}</div>'


def trigger_confetti():
    """Injected JS for burst confetti celebratory animation when analysis completes."""
    confetti_script = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
    <script>
    if (window.confetti) {
        confetti({
            particleCount: 50,
            spread: 60,
            origin: { y: 0.8 },
            colors: ['#06b6d4', '#3b82f6', '#10b981', '#a855f7']
        });
    }
    </script>
    """
    components.html(confetti_script, height=0, width=0)


# ---------------------------------------------------------
# Sidebar Controls & Telemetry
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
    <div class="sidebar-panel">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
            <span style="font-size:12px; font-weight:700; color:#38bdf8; letter-spacing:0.05em; text-transform:uppercase;">
                Security Perimeter
            </span>
            <span class="stat-pill-dot"></span>
        </div>
        <div style="font-size:20px; font-weight:800; color:#f8fafc; margin-bottom:4px;">
            ENCLAVE SHIELD
        </div>
        <div style="font-size:12px; color:#94a3b8;">
            Sanitizing confidential entities before neural sentiment classification.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎚️ Detection Sensitivity")
    threshold = st.slider(
        "PII Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.05,
        help="Higher thresholds only redact high-certainty entities. Lower values are stricter.",
    )

    if threshold >= 0.75:
        mode_label = "⚡ Permissive Mode (Fewer False Positives)"
        mode_color = "#38bdf8"
    elif threshold >= 0.45:
        mode_label = "⚖️ Balanced Privacy Mode (Recommended)"
        mode_color = "#10b981"
    else:
        mode_label = "🛡️ Strict Fortress Mode (Aggressive Redaction)"
        mode_color = "#f59e0b"

    st.markdown(
        f'<div style="font-size:12px; font-weight:600; color:{mode_color}; margin-top:-8px; margin-bottom:20px;">{mode_label}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        """
    <div style="font-size:11px; color:#64748b; line-height:1.6;">
        <strong style="color:#94a3b8;">Privacy Guarantees:</strong><br>
        • All computation runs 100% locally on your device.<br>
        • Zero outbound telemetry or cloud API calls.<br>
        • Sensitive text never reaches the sentiment classifier.
    </div>
    """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Main Tabs Navigation
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📝 Single Text Inspector", "📁 Batch CSV Sanitizer"])

# =========================================================
# Tab 1: Single Text Analysis
# =========================================================
with tab1:
    st.markdown("#### 🔍 Input Text for Privacy Sanitization & Analysis")

    # Sample prompt quick presets
    c_p1, c_p2, c_p3 = st.columns([1, 1, 1])
    sample_preset = None
    with c_p1:
        if st.button("💼 Sample: Executive Note"):
            st.session_state["text_input"] = (
                "Hi Sarah Jenkins, please transfer the $45,000 project fee to account 4912-8823-1029-4411. "
                "Reach out directly at sarah.j@novacorp.io or call my private cell +1-202-555-0194. Thank you so much!"
            )
    with c_p2:
        if st.button("🏥 Sample: Clinical Referral"):
            st.session_state["text_input"] = (
                "Patient Robert Chen visited the clinic in Boston on October 14th. "
                "Contact his emergency contact Mary Chen at 617-555-0144 or mary.c@medmail.com. "
                "The patient expressed extreme frustration with the delay in lab test results."
            )
    with c_p3:
        if st.button("✨ Sample: Customer Feedback"):
            st.session_state["text_input"] = (
                "I absolutely adore the new dashboard upgrade! Outstanding work by Alex Rivera and his crew. "
                "Feel free to quote me at alex.fan@cloudcorp.org."
            )

    default_val = st.session_state.get(
        "text_input",
        "Hi John Doe, please confirm the wire transfer of $12,500 to our Citibank IBAN US33CITI1234567890. "
        "You can email me back at john.doe@enterprise.com or call me at +1-415-555-2671. I look forward to working with you!",
    )

    text = st.text_area(
        label="Enter or paste text to analyze",
        value=default_val,
        height=140,
        placeholder="Type or paste any sensitive text here...",
    )

    run_col, clear_col = st.columns([1, 5])
    with run_col:
        analyze_clicked = st.button("🚀 Analyze & Sanitize", key="single_run")

    if analyze_clicked and text.strip():
        with st.spinner("Analyzing PII entities & evaluating sentiment..."):
            clean, results = redact(text, threshold)
            sent = clf(clean, truncation=True)[0]

        trigger_confetti()

        # Display Top Summary Metrics
        st.markdown("<br>", unsafe_allow_html=True)
        is_pos = sent["label"].upper() == "POSITIVE"
        sentiment_theme = "sentiment-positive" if is_pos else "sentiment-negative"
        sentiment_emoji = "✨" if is_pos else "⚠️"
        sentiment_color = "#10b981" if is_pos else "#f43f5e"

        # Sentiment & Entity Count Summary Grid
        m1, m2, m3 = st.columns([1.5, 1, 1])

        with m1:
            st.markdown(
                f"""
            <div class="sentiment-card {sentiment_theme}">
                <div class="sentiment-icon">{sentiment_emoji}</div>
                <div>
                    <div style="font-size:12px; font-weight:700; color:{sentiment_color}; text-transform:uppercase; letter-spacing:0.05em;">
                        Classified Sentiment
                    </div>
                    <div style="font-size:24px; font-weight:800; color:#ffffff;">
                        {sent["label"]} ({sent["score"]:.1%})
                    </div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:2px;">
                        Evaluated strictly on sanitized, non-sensitive tokens.
                    </div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with m2:
            st.markdown(
                f"""
            <div class="cyber-card" style="text-align:center; padding:18px;">
                <div style="font-size:12px; font-weight:700; color:#38bdf8; text-transform:uppercase;">Entities Detected</div>
                <div style="font-size:32px; font-weight:800; color:#38bdf8; margin:4px 0;">{len(results)}</div>
                <div style="font-size:11px; color:#94a3b8;">Confidence ≥ {threshold:.0%}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with m3:
            redaction_rate = (
                f"{len(clean) / max(len(text), 1):.0%}" if results else "100%"
            )
            st.markdown(
                f"""
            <div class="cyber-card" style="text-align:center; padding:18px;">
                <div style="font-size:12px; font-weight:700; color:#a855f7; text-transform:uppercase;">Text Preservation</div>
                <div style="font-size:32px; font-weight:800; color:#a855f7; margin:4px 0;">{redaction_rate}</div>
                <div style="font-size:11px; color:#94a3b8;">Original Context Retained</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Side by side: Detected Entities vs Redacted Text
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("#### 🎯 Identified PII Entities (Highlighted)")
            st.markdown(
                build_highlighted_html(text, results), unsafe_allow_html=True
            )

        with col_right:
            st.markdown("#### 🛡️ Anonymized Output (Safe for Cloud / LLMs)")
            st.markdown(
                f'<div class="redacted-box">{html.escape(clean)}</div>',
                unsafe_allow_html=True,
            )

        # Detailed PII Entity Table if entities found
        if results:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📋 Entity Telemetry Breakdown")

            pii_data = [
                {
                    "Entity Category": r.entity_type,
                    "Detected Secret": text[r.start : r.end],
                    "Confidence Score": f"{r.score:.1%}",
                    "Span Position": f"[{r.start}:{r.end}]",
                }
                for r in results
            ]
            st.dataframe(pd.DataFrame(pii_data), use_container_width=True)


# =========================================================
# Tab 2: Batch CSV Sanitizer
# =========================================================
with tab2:
    st.markdown("#### 📁 High-Throughput Batch CSV Redactor & Sentiment Classifier")
    st.markdown(
        "<p style='color:#94a3b8; font-size:13px;'>Upload any dataset containing user feedback, emails, or logs. All sensitive columns are anonymized in memory.</p>",
        unsafe_allow_html=True,
    )

    file = st.file_uploader("Upload CSV Document", type="csv")

    if file:
        df = pd.read_csv(file)
        c_opt1, c_opt2 = st.columns(2)

        with c_opt1:
            col = st.selectbox(
                "Select column containing sensitive text", df.columns
            )
        with c_opt2:
            n = st.number_input(
                "Number of rows to process",
                min_value=1,
                max_value=len(df),
                value=min(100, len(df)),
                step=10,
            )

        if st.button("⚡ Execute Batch Privacy Processing", key="csv_btn"):
            sub = df.head(int(n)).copy()
            clean_texts, pii_types = [], []

            st.markdown("##### ⚙️ Sanitizing Records...")
            bar = st.progress(0)
            status_text = st.empty()

            total_items = len(sub)
            for i, t in enumerate(sub[col].astype(str)):
                clean, res = redact(t, threshold)
                clean_texts.append(clean)
                pii_types.extend(r.entity_type for r in res)
                progress_pct = (i + 1) / total_items
                bar.progress(progress_pct)
                status_text.caption(
                    f"Processed {i + 1} of {total_items} records ({progress_pct:.0%})"
                )

            sub["clean_text"] = clean_texts

            with st.spinner("Classifying sentiment across sanitized batch..."):
                out = clf(clean_texts, truncation=True, batch_size=16)
                sub["sentiment"] = [o["label"] for o in out]
                sub["sentiment_score"] = [round(o["score"], 3) for o in out]

            trigger_confetti()
            status_text.empty()

            # Batch Results Summary Metrics
            st.markdown("<br>", unsafe_allow_html=True)
            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown(
                    f"""
                <div class="cyber-card" style="text-align:center;">
                    <div style="font-size:12px; font-weight:700; color:#38bdf8;">RECORDS PROCESSED</div>
                    <div style="font-size:32px; font-weight:800; color:#38bdf8;">{len(sub)}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with k2:
                st.markdown(
                    f"""
                <div class="cyber-card" style="text-align:center;">
                    <div style="font-size:12px; font-weight:700; color:#f43f5e;">TOTAL PII STRIPPED</div>
                    <div style="font-size:32px; font-weight:800; color:#f43f5e;">{len(pii_types)}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with k3:
                pos_count = (sub["sentiment"] == "POSITIVE").sum()
                st.markdown(
                    f"""
                <div class="cyber-card" style="text-align:center;">
                    <div style="font-size:12px; font-weight:700; color:#10b981;">POSITIVE RATIO</div>
                    <div style="font-size:32px; font-weight:800; color:#10b981;">{pos_count / len(sub):.1%}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Charts
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### 📊 Sentiment Distribution")
                st.bar_chart(sub["sentiment"].value_counts(), color="#06b6d4")
            with c2:
                st.markdown("##### 🛡️ PII Types Discovered")
                if pii_types:
                    st.bar_chart(
                        pd.Series(pii_types).value_counts(), color="#a855f7"
                    )
                else:
                    st.success("✅ Zero PII entities found in selected rows!")

            # Safe Dataframe View & Download
            st.markdown("##### 🔒 Sanitized Data Preview (Original PII Omitted)")
            safe = sub.drop(columns=[col])
            st.dataframe(safe, use_container_width=True)

            csv_bytes = safe.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Sanitized CSV (Zero PII)",
                data=csv_bytes,
                file_name="sanitized_privacy_results.csv",
                mime="text/csv",
                key="download_csv",
            )
