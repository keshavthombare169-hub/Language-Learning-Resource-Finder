import streamlit as st
import json
from resource_finder import resource_finder_agent
from curator import curator_agent
from plan_writer import plan_writer_agent
from judge import judge_agent

st.set_page_config(
    page_title="Language Learning Resource Finder",
    page_icon="🌐",
    layout="centered"
)

st.markdown("""
<style>
    .agent-box {
        background: #f8f9fa;
        border-left: 4px solid #4CAF50;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
    }
    .agent-title {
        font-weight: 600;
        font-size: 0.85rem;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }
    .score-good { color: #2e7d32; font-weight: 600; }
    .score-ok   { color: #e65100; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.title("🌐 Language Learning Resource Finder")
st.caption("3 AI agents + Tavily Search + LLM-as-Judge · Powered by Gemini (free tier)")

with st.expander("ℹ️ How this works", expanded=False):
    st.markdown("""
**Agent 1 — Resource Finder** calls Tavily Search to find real, current resources online.  
**Agent 2 — Curator** reads those results and picks the 3 best for your level.  
**Agent 3 — Plan Writer** drafts a personalised 30-day kickstart plan.  
**LLM-as-Judge** scores the output on 3 rubric dimensions and gives a verdict.

All agents call the **Gemini 1.5 Flash** model (free tier). Tavily has a free tier too.
    """)

# ── Input form ───────────────────────────────────────────────────────────────
with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        language = st.text_input("Target language", value="Japanese", placeholder="e.g. French, Hindi, Spanish")
    with col2:
        level = st.selectbox("Your current level", ["Beginner", "Intermediate"])
    submitted = st.form_submit_button("🚀 Run agents", use_container_width=True)

# ── Agent pipeline ────────────────────────────────────────────────────────────
if submitted:
    if not language.strip():
        st.error("Please enter a language.")
        st.stop()

    language = language.strip()

    # ── Agent 1 ──────────────────────────────────────────────────────────────
    with st.status("Agent 1 — Resource Finder is searching the web…", expanded=True) as s1:
        st.write("Calling Tavily Search for apps, YouTube channels, podcasts & courses…")
        try:
            resources_raw, tavily_results = resource_finder_agent(language, level)
            s1.update(label="✅ Agent 1 — Resource Finder done", state="complete")
        except Exception as e:
            s1.update(label="❌ Agent 1 failed", state="error")
            st.error(f"Resource Finder error: {e}")
            st.stop()

    st.markdown('<div class="agent-box"><div class="agent-title">🔍 Agent 1 · Resource Finder</div>', unsafe_allow_html=True)
    st.markdown(resources_raw)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("📡 Raw Tavily search results", expanded=False):
        for r in tavily_results:
            st.markdown(f"- **{r.get('title','')}** — {r.get('url','')}")

    # ── Agent 2 ──────────────────────────────────────────────────────────────
    with st.status("Agent 2 — Curator is selecting the best resources…", expanded=True) as s2:
        try:
            curated = curator_agent(language, level, resources_raw)
            s2.update(label="✅ Agent 2 — Curator done", state="complete")
        except Exception as e:
            s2.update(label="❌ Agent 2 failed", state="error")
            st.error(f"Curator error: {e}")
            st.stop()

    st.markdown('<div class="agent-box"><div class="agent-title">🎯 Agent 2 · Curator</div>', unsafe_allow_html=True)
    st.markdown(curated)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Agent 3 ──────────────────────────────────────────────────────────────
    with st.status("Agent 3 — Plan Writer is drafting your 30-day plan…", expanded=True) as s3:
        try:
            plan = plan_writer_agent(language, level, curated)
            s3.update(label="✅ Agent 3 — Plan Writer done", state="complete")
        except Exception as e:
            s3.update(label="❌ Agent 3 failed", state="error")
            st.error(f"Plan Writer error: {e}")
            st.stop()

    st.markdown('<div class="agent-box"><div class="agent-title">📅 Agent 3 · 30-Day Plan</div>', unsafe_allow_html=True)
    st.markdown(plan)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Judge ─────────────────────────────────────────────────────────────────
    with st.status("LLM-as-Judge is evaluating quality…", expanded=True) as sj:
        try:
            judgment = judge_agent(language, level, curated, plan)
            sj.update(label="✅ LLM-as-Judge done", state="complete")
        except Exception as e:
            sj.update(label="❌ Judge failed", state="error")
            st.error(f"Judge error: {e}")
            st.stop()

    st.markdown("---")
    st.subheader("⚖️ LLM-as-Judge Evaluation")

    rubric = judgment.get("rubric", {})
    col1, col2, col3 = st.columns(3)
    for col, (key, label) in zip(
        [col1, col2, col3],
        [("resource_quality", "Resource Quality"),
         ("plan_structure",   "Plan Structure"),
         ("personalization",  "Personalization")]
    ):
        score = rubric.get(key, 0)
        color = "score-good" if score >= 75 else "score-ok"
        col.metric(label, f"{score}/100")

    st.progress(int(sum(rubric.values()) / max(len(rubric), 1)) / 100)

    verdict = judgment.get("verdict", "")
    improvements = judgment.get("improvements", [])

    st.info(f"**Verdict:** {verdict}")
    if improvements:
        with st.expander("💡 Suggested improvements"):
            for tip in improvements:
                st.markdown(f"- {tip}")

    st.success("✅ All agents completed successfully!")
    st.caption("Built for Semester IV · Introduction to Agentic AI Systems")
