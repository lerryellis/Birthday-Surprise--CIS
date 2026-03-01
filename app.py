import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# ============================================================
#  PATH HELPER — resolves relative to THIS script's directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_file(relative_path):
    """
    Case-insensitive file finder.
    Tries the exact path first, then scans the folder for a
    case-insensitive match (handles hero_bg.JPG vs hero_bg.jpg etc.)
    Returns the full absolute path if found, else None.
    """
    full = os.path.join(BASE_DIR, relative_path)
    if os.path.exists(full):
        return full

    # Try case-insensitive scan of the target directory
    folder   = os.path.dirname(full)
    filename = os.path.basename(full).lower()
    if os.path.isdir(folder):
        for entry in os.listdir(folder):
            if entry.lower() == filename:
                return os.path.join(folder, entry)
    return None

def img_src(relative_path):
    """
    Returns (data_uri_string, status_message).
    data_uri is '' if the file cannot be found/read.
    """
    path = find_file(relative_path)
    if path is None:
        return "", f"❌  NOT FOUND — looked for: {os.path.join(BASE_DIR, relative_path)}"

    ext  = path.rsplit(".", 1)[-1].lower()
    mime = {"jpg":"image/jpeg","jpeg":"image/jpeg",
            "png":"image/png","gif":"image/gif",
            "webp":"image/webp"}.get(ext, "image/png")
    try:
        with open(path, "rb") as f:
            raw = f.read()
        data = base64.b64encode(raw).decode()
        size_kb = len(raw) // 1024
        return f"data:{mime};base64,{data}", f"✅  Loaded — {path}  ({size_kb} KB)"
    except Exception as e:
        return "", f"❌  Read error — {path}: {e}"

# ============================================================
#  LOAD IMAGES  (edit filenames here if yours differ)
# ============================================================
HERO_BG,      HERO_STATUS      = img_src("images/hero_bg.jpg")
PORTAL_BG,    PORTAL_STATUS    = img_src("images/portal_bg.jpg")
SCREENSHOT_1, SS1_STATUS       = img_src("images/screenshot1.png")
SCREENSHOT_2, SS2_STATUS       = img_src("images/screenshot2.png")
SCREENSHOT_3, SS3_STATUS       = img_src("images/screenshot3.png")

# ============================================================
#  LOAD PAYLOAD
# ============================================================
_exe_path = find_file("birthday_surprise.exe")
if _exe_path:
    with open(_exe_path, "rb") as f:
        download_href = "data:application/octet-stream;base64," + base64.b64encode(f.read()).decode()
    exe_status = f"✅  Payload found — {_exe_path}"
else:
    download_href = "#"
    exe_status = f"❌  birthday_surprise.exe not found in {BASE_DIR}"

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Simulation | PixelForge",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding: 0; max-width: 100%;}
        iframe {border: none;}
    </style>
""", unsafe_allow_html=True)

# ============================================================
#  🔍 DEBUG PANEL — expand this in your browser to diagnose
#     image loading issues. Remove or hide once images work.
# ============================================================
with st.expander("🔍 Image Diagnostics (expand to debug)", expanded=not HERO_BG):
    st.code(f"""
Working directory : {os.getcwd()}
Script directory  : {BASE_DIR}
images/ folder    : {os.path.join(BASE_DIR, 'images')}
images/ exists    : {os.path.isdir(os.path.join(BASE_DIR, 'images'))}
images/ contents  : {os.listdir(os.path.join(BASE_DIR, 'images')) if os.path.isdir(os.path.join(BASE_DIR, 'images')) else 'N/A'}

SLOT A  hero_bg.jpg      {HERO_STATUS}
SLOT B  portal_bg.jpg    {PORTAL_STATUS}
SLOT C  screenshot1.png  {SS1_STATUS}
SLOT D  screenshot2.png  {SS2_STATUS}
SLOT E  screenshot3.png  {SS3_STATUS}
        payload          {exe_status}
    """, language="text")
    st.caption("Once all slots show ✅ you can delete this expander block.")

# ============================================================
#  HTML
# ============================================================
# Build CSS background strings safely — avoids broken CSS if
# the data URI somehow contains a stray quote or newline.
def bg_css(data_uri):
    """Return background-image CSS or empty string."""
    if not data_uri:
        return ""
    # data URIs are pure base64 — safe to embed directly
    return f"background-image:url('{data_uri}');background-size:cover;background-position:center;"

HERO_BG_CSS   = bg_css(HERO_BG)
PORTAL_BG_CSS = bg_css(PORTAL_BG)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>PixelForge Studios — The Birthday Rift</title>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DM+Mono:wght@300;400;500&family=Syne:wght@400;700;800&display=swap" rel="stylesheet"/>
<style>
  /* ── EDUCATOR BANNER ── */
  #edu-banner{{
    position:fixed;top:0;left:0;right:0;z-index:9999;
    background:#ff0040;color:#fff;
    font-family:'DM Mono',monospace;font-size:12px;font-weight:500;
    padding:8px 16px;display:flex;align-items:center;justify-content:space-between;
    border-bottom:2px solid #ff6680;
    box-shadow:0 2px 12px rgba(255,0,64,.5);
  }}
  #edu-banner .tag{{background:#fff;color:#ff0040;padding:2px 8px;border-radius:3px;
    font-weight:700;letter-spacing:.05em;margin-right:10px;font-size:11px;}}
  #edu-banner details{{display:inline;cursor:pointer;}}
  #edu-banner summary{{display:inline;list-style:none;text-decoration:underline;cursor:pointer;}}
  #edu-banner .panel{{position:absolute;top:100%;left:0;right:0;
    background:#1a0010;border-bottom:2px solid #ff0040;
    padding:16px 24px;font-size:12px;line-height:1.8;color:#ffb3c2;}}
  #edu-banner .panel ul{{margin:8px 0 0 16px;}}
  #edu-banner .panel li{{margin-bottom:4px;}}

  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
  :root{{--bg:#0b0c10;--accent:#c8ff00;--accent2:#ff5e00;--text:#e8e9ef;--muted:#6b6f7e;--card:#16171e;}}
  html{{scroll-behavior:smooth;}}
  body{{background:var(--bg);color:var(--text);font-family:'DM Mono',monospace;
    font-size:14px;line-height:1.7;padding-top:38px;overflow-x:hidden;}}
  body::after{{content:'';position:fixed;inset:0;pointer-events:none;z-index:100;
    background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.06) 2px,rgba(0,0,0,.06) 4px);}}

  /* NAV */
  nav{{display:flex;align-items:center;justify-content:space-between;
    padding:18px 48px;border-bottom:1px solid #1e2030;
    backdrop-filter:blur(12px);background:rgba(11,12,16,.85);
    position:sticky;top:38px;z-index:50;}}
  .logo{{font-family:'Press Start 2P',monospace;font-size:11px;color:var(--accent);
    text-shadow:0 0 18px var(--accent);letter-spacing:.1em;display:flex;align-items:center;gap:10px;}}
  .logo span{{color:#fff;}}
  nav ul{{display:flex;gap:32px;list-style:none;}}
  nav ul a{{color:var(--muted);text-decoration:none;font-size:12px;letter-spacing:.08em;transition:color .2s;}}
  nav ul a:hover{{color:var(--accent);}}
  .nav-btn{{background:var(--accent);color:#000;border:none;cursor:pointer;
    font-family:'DM Mono',monospace;font-size:11px;font-weight:500;letter-spacing:.08em;
    padding:8px 18px;border-radius:2px;transition:opacity .2s;}}
  .nav-btn:hover{{opacity:.85;}}

  /* HERO — SLOT A */
  .hero{{min-height:90vh;display:flex;flex-direction:column;align-items:center;
    justify-content:center;padding:60px 24px;text-align:center;position:relative;
    background-color:var(--bg);{HERO_BG_CSS}}}
  .hero-overlay{{position:absolute;inset:0;z-index:0;
    background:rgba(11,12,16,{".62" if HERO_BG else "0"});}}
  .hero-content{{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;}}
  .hero-eyebrow{{font-family:'Press Start 2P',monospace;font-size:8px;color:var(--accent2);
    letter-spacing:.15em;margin-bottom:20px;animation:blink 1.2s step-end infinite;}}
  @keyframes blink{{50%{{opacity:0;}}}}
  .hero h1{{font-family:'Syne',sans-serif;font-size:clamp(42px,8vw,96px);font-weight:800;
    line-height:1.0;letter-spacing:-.02em;
    background:linear-gradient(135deg,#fff 30%,var(--accent) 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    margin-bottom:24px;}}
  .hero p{{max-width:520px;color:var(--muted);font-size:15px;line-height:1.8;margin-bottom:40px;}}
  .hero-tags{{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-bottom:48px;}}
  .tag-pill{{font-size:10px;letter-spacing:.1em;padding:4px 12px;border:1px solid #2a2d3a;border-radius:99px;color:var(--muted);}}
  .stars{{display:flex;gap:3px;margin-bottom:48px;}}
  .star{{color:var(--accent);font-size:16px;}}

  /* GALLERY — SLOTS C D E */
  .gallery{{padding:40px 48px;display:flex;gap:12px;overflow-x:auto;}}
  .gallery img{{flex:0 0 auto;width:460px;height:260px;object-fit:cover;border-radius:4px;
    border:1px solid #1e2030;box-shadow:0 8px 32px rgba(0,0,0,.5);}}
  .gallery .placeholder{{flex:0 0 auto;width:460px;height:260px;background:#111318;
    border:2px dashed #2a2d3a;border-radius:4px;display:flex;flex-direction:column;
    align-items:center;justify-content:center;color:#3a3d4e;font-size:11px;letter-spacing:.08em;gap:10px;}}
  .gallery .placeholder span{{font-size:28px;opacity:.3;}}

  /* PORTAL — SLOT B */
  .portal-section{{position:relative;background-color:var(--bg);{PORTAL_BG_CSS}}}
  .portal-overlay{{position:absolute;inset:0;z-index:0;
    background:rgba(11,12,16,{".72" if PORTAL_BG else "0"});}}
  .portal-wrap{{padding:60px 24px;display:flex;justify-content:center;position:relative;z-index:1;}}
  .portal-card{{background:var(--card);border:1px solid #1e2030;border-radius:6px;
    padding:48px;max-width:540px;width:100%;position:relative;overflow:hidden;
    box-shadow:0 0 60px rgba(200,255,0,.04);}}
  .portal-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,var(--accent),var(--accent2),transparent);}}
  .portal-card h2{{font-family:'Syne',sans-serif;font-size:22px;font-weight:700;margin-bottom:8px;}}
  .portal-card .sub{{color:var(--muted);font-size:12px;margin-bottom:32px;line-height:1.6;}}
  label{{display:block;font-size:11px;letter-spacing:.1em;color:var(--muted);margin-bottom:6px;}}
  input[type=date]{{width:100%;background:#0b0c10;border:1px solid #2a2d3a;color:var(--text);
    padding:12px 14px;border-radius:3px;font-family:'DM Mono',monospace;font-size:13px;
    margin-bottom:24px;transition:border-color .2s;color-scheme:dark;}}
  input[type=date]:focus{{outline:none;border-color:var(--accent);}}
  .gen-btn{{width:100%;background:var(--accent);color:#000;border:none;
    font-family:'DM Mono',monospace;font-size:12px;font-weight:500;
    letter-spacing:.1em;padding:14px;border-radius:3px;cursor:pointer;transition:opacity .2s,transform .1s;}}
  .gen-btn:hover{{opacity:.9;}} .gen-btn:active{{transform:scale(.98);}} .gen-btn:disabled{{opacity:.4;cursor:not-allowed;}}
  #progress-wrap{{display:none;margin-top:20px;}}
  #progress-label{{font-size:11px;color:var(--muted);margin-bottom:8px;letter-spacing:.08em;}}
  #progress-bar-bg{{background:#1e2030;border-radius:2px;height:6px;overflow:hidden;}}
  #progress-bar{{height:6px;background:linear-gradient(90deg,var(--accent),var(--accent2));
    width:0%;transition:width .15s linear;border-radius:2px;}}
  #result{{display:none;margin-top:24px;}}
  .success-box{{background:#0d1a00;border:1px solid #2a4a00;border-radius:4px;padding:16px;margin-bottom:16px;}}
  .success-box p{{font-size:12px;color:#a8e063;line-height:1.7;}}
  .dl-btn{{display:block;width:100%;text-align:center;
    background:linear-gradient(135deg,var(--accent2),#ff8c00);
    color:#fff;font-family:'DM Mono',monospace;font-size:12px;font-weight:500;
    letter-spacing:.1em;padding:14px;border-radius:3px;cursor:pointer;text-decoration:none;transition:opacity .2s;}}
  .dl-btn:hover{{opacity:.9;}}
  .note{{font-size:10px;color:var(--muted);text-align:center;margin-top:10px;line-height:1.6;}}

  /* TACTICS */
  .tactics{{margin:0 auto 80px;max-width:860px;padding:0 24px;}}
  .tactics h3{{font-family:'Press Start 2P',monospace;font-size:9px;color:var(--accent2);letter-spacing:.12em;margin-bottom:24px;}}
  .tactic-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;}}
  .tactic-item{{background:var(--card);border:1px solid #1e2030;border-radius:4px;padding:20px;}}
  .tactic-item .num{{font-family:'Press Start 2P',monospace;font-size:8px;color:var(--accent);margin-bottom:10px;display:block;}}
  .tactic-item h4{{font-family:'Syne',sans-serif;font-weight:700;font-size:14px;margin-bottom:6px;}}
  .tactic-item p{{font-size:11px;color:var(--muted);line-height:1.7;}}
  .red{{color:#ff6680!important;}} .amber{{color:#ffb347!important;}} .green{{color:var(--accent)!important;}}

  /* FOOTER */
  footer{{border-top:1px solid #1e2030;padding:32px 48px;display:flex;align-items:center;
    justify-content:space-between;color:var(--muted);font-size:11px;letter-spacing:.06em;}}
  .pixel-deco{{font-family:'Press Start 2P',monospace;font-size:7px;color:#2a2d3a;white-space:pre;line-height:1.2;}}

  @media(max-width:600px){{
    nav{{padding:14px 20px;}} nav ul{{display:none;}}
    .portal-card{{padding:28px 20px;}}
    footer{{flex-direction:column;gap:12px;text-align:center;}}
    .gallery{{padding:24px 20px;}}
    .gallery img,.gallery .placeholder{{width:280px;height:158px;}}
  }}
</style>
</head>
<body>

<div id="edu-banner">
  <div>
    <span class="tag">⚠ SIMULATION</span>
    This is a <strong>phishing awareness demo</strong> for cybersecurity education. No real executable is delivered.
    &nbsp;·&nbsp;
    <details>
      <summary>Instructor notes ▾</summary>
      <div class="panel">
        <strong>What this demo illustrates:</strong>
        <ul>
          <li>Authority &amp; personalisation cues ("custom-generated just for you")</li>
          <li>Fake progress / loading to build perceived legitimacy</li>
          <li>Urgency + reward framing to bypass rational evaluation</li>
          <li>Trusted UI patterns (indie game sites) to lower guard</li>
          <li>Collecting PII (date of birth) under false pretenses</li>
        </ul>
        <br/>Run inside an isolated VM. The download button here is inert — wire a real (benign) payload in your lab environment only.
      </div>
    </details>
  </div>
  <span style="font-size:10px;opacity:.6;">CIS-301 · Social Engineering Lab</span>
</div>

<nav>
  <div class="logo">◈ <span>PIXEL</span>FORGE</div>
  <ul>
    <li><a href="#">Games</a></li><li><a href="#">About</a></li>
    <li><a href="#">Devlog</a></li><li><a href="#">Press Kit</a></li>
  </ul>
  <button class="nav-btn">WISHLIST ↗</button>
</nav>

<section class="hero">
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-eyebrow">▶ NOW AVAILABLE — LIMITED ALPHA</div>
    <h1>The Birthday Rift</h1>
    <p>A procedurally-generated adventure calibrated to the exact cosmic moment you were born. No two playthroughs are ever the same.</p>
    <div class="hero-tags">
      <span class="tag-pill">ROGUELITE</span><span class="tag-pill">PROCEDURAL</span>
      <span class="tag-pill">PIXEL ART</span><span class="tag-pill">SOLO DEV</span>
      <span class="tag-pill">FREE ALPHA</span>
    </div>
    <div class="stars">
      <span class="star">★</span><span class="star">★</span><span class="star">★</span>
      <span class="star">★</span><span class="star" style="color:#2a2d3a;">★</span>
    </div>
    <p style="font-size:12px;color:var(--muted);">4.1 / 5 &nbsp;·&nbsp; 2,340 itch.io ratings</p>
  </div>
</section>

<div class="gallery">
  {"<img src='" + SCREENSHOT_1 + "' alt='Screenshot 1'/>" if SCREENSHOT_1 else "<div class='placeholder'><span>🎮</span>images/screenshot1.png</div>"}
  {"<img src='" + SCREENSHOT_2 + "' alt='Screenshot 2'/>" if SCREENSHOT_2 else "<div class='placeholder'><span>🎮</span>images/screenshot2.png</div>"}
  {"<img src='" + SCREENSHOT_3 + "' alt='Screenshot 3'/>" if SCREENSHOT_3 else "<div class='placeholder'><span>🎮</span>images/screenshot3.png</div>"}
</div>

<div class="portal-section">
  <div class="portal-overlay"></div>
  <div class="portal-wrap">
    <div class="portal-card">
      <h2>Generate Your Adventure</h2>
      <p class="sub">Our engine seeds your world using your birth date and current astrological alignment. Enter your DOB below to compile your personalised build.</p>
      <label for="dob">DATE OF BIRTH</label>
      <input type="date" id="dob" value="2000-01-01" min="1920-01-01" max="2025-12-31"/>
      <button class="gen-btn" id="genBtn" onclick="startGeneration()">GENERATE MY GAME →</button>
      <div id="progress-wrap">
        <p id="progress-label">Initialising seed engine…</p>
        <div id="progress-bar-bg"><div id="progress-bar"></div></div>
      </div>
      <div id="result">
        <div class="success-box"><p id="success-msg"></p></div>
        <a class="dl-btn" href="{download_href}" download="birthday_rift_alpha.exe" id="dlBtn">
          🎁 Download birthday_rift_alpha.exe
        </a>
        <p class="note">Windows / Linux / macOS builds available · ~12 MB · v0.4.1-alpha</p>
      </div>
    </div>
  </div>
</div>

<div class="tactics">
  <h3>// ATTACK VECTORS ILLUSTRATED — INSTRUCTOR VIEW</h3>
  <div class="tactic-grid">
    <div class="tactic-item"><span class="num">01</span><h4>Personalisation Theatre</h4>
      <p>The DOB input creates an illusion of a custom product. The value is ignored — any date produces the same output. <span class="red">Social engineering hook.</span></p></div>
    <div class="tactic-item"><span class="num">02</span><h4>Fake Progress Cues</h4>
      <p>Animated progress bar + rotating status text simulate real computation, inflating perceived legitimacy. <span class="amber">Cognitive bias: sunk cost.</span></p></div>
    <div class="tactic-item"><span class="num">03</span><h4>PII Collection</h4>
      <p>Date of birth is sensitive data. Victims enter it willingly because the context seems benign. <span class="red">Real threat: identity data.</span></p></div>
    <div class="tactic-item"><span class="num">04</span><h4>Trust Scaffolding</h4>
      <p>Star ratings, itch.io references, press kit nav, and polished UI build false credibility. <span class="amber">Authority bias.</span></p></div>
    <div class="tactic-item"><span class="num">05</span><h4>Reward Framing</h4>
      <p>Birthday + gift emoji + "just for you" language exploits emotional anticipation. <span class="amber">Cognitive bias: excitement.</span></p></div>
    <div class="tactic-item"><span class="num">06</span><h4>Safe Version Marker</h4>
      <p>OS-bypass instructions intentionally omitted. In the wild, <span class="red">"Run anyway"</span> appears here. <span class="green">Removed for safety.</span></p></div>
  </div>
</div>

<footer>
  <div>
    <div style="margin-bottom:6px;">© 2024 PixelForge Studios (fictional entity · simulation only)</div>
    <div>Privacy · Terms · Press · itch.io</div>
  </div>
  <div class="pixel-deco">░░▒▒▓▓██▓▓▒▒░░
░  PIXEL FORGE  ░
░░▒▒▓▓██▓▓▒▒░░</div>
</footer>

<script>
const steps=["Initialising seed engine…","Reading cosmic alignment…","Calibrating birth year offset…",
  "Generating dungeon topology…","Compiling sprite palettes…","Linking audio seeds…",
  "Packaging personalised build…","Finalising checksums…"];
function startGeneration(){{
  const dob=document.getElementById('dob').value;
  if(!dob){{alert('Please enter a date of birth.');return;}}
  document.getElementById('genBtn').disabled=true;
  document.getElementById('progress-wrap').style.display='block';
  document.getElementById('result').style.display='none';
  let step=0,pct=0;
  const bar=document.getElementById('progress-bar'),label=document.getElementById('progress-label');
  const iv=setInterval(()=>{{
    pct+=Math.random()*14+4;if(pct>100)pct=100;
    bar.style.width=pct+'%';label.textContent=steps[step++%steps.length];
    if(pct>=100){{clearInterval(iv);showResult(dob);}}
  }},230);
}}
function showResult(dob){{
  const d=new Date(dob);
  const fmt=d.toLocaleDateString('en-GB',{{day:'numeric',month:'long',year:'numeric'}});
  const sign=getSign(d.getMonth()+1,d.getDate());
  document.getElementById('success-msg').innerHTML=
    `✔ Build compiled for <strong>${{fmt}}</strong> (${{sign}}).<br/>
     Seed hash: <code style="color:#c8ff00">${{hash(dob)}}</code><br/>
     Your dungeon contains <strong>${{rnd(12,34)}}</strong> rooms across <strong>${{rnd(3,7)}}</strong> biomes.`;
  document.getElementById('progress-wrap').style.display='none';
  document.getElementById('result').style.display='block';
}}
function getSign(m,d){{
  const s=[[1,20,'Capricorn'],[2,19,'Aquarius'],[3,21,'Pisces'],[4,20,'Aries'],
    [5,21,'Taurus'],[6,21,'Gemini'],[7,23,'Cancer'],[8,23,'Leo'],
    [9,23,'Virgo'],[10,23,'Libra'],[11,22,'Scorpio'],[12,22,'Sagittarius'],[12,31,'Capricorn']];
  for(const[sm,sd,n] of s)if(m<=sm&&d<=sd)return n;return 'Capricorn';
}}
function hash(s){{let h=5381;for(let i=0;i<s.length;i++)h=((h<<5)+h)+s.charCodeAt(i);return(h>>>0).toString(16).padStart(8,'0').toUpperCase();}}
function rnd(a,b){{return Math.floor(Math.random()*(b-a+1))+a;}}
</script>
</body>
</html>"""

components.html(html_content, height=2800, scrolling=True)