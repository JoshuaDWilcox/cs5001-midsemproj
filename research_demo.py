"""
Scientific Research Workflow Demo
===================================

Demonstrates the ASTER-inspired research agent workflow programmatically.
This script shows tools being invoked through the Orchestral AI agent,
showcasing all key concepts from the paper.

Since Ollama cloud models don't support structured tool calling,
this demo drives the workflow explicitly — which is actually how
ASTER and HEPTAPOD are used in practice (scripted research pipelines).

Run:
    python research_demo.py
"""

import os
import sys

# ─── Direct tool demonstration (no LLM needed) ──────────────────────────────
# This shows the scientific tools working independently, then combines
# them with the agent for conversational analysis.

from custom_tools import (
    fetch_planetary_data,
    list_available_planets,
    compute_transit_depth,
    compute_habitable_zone,
    statistical_analysis,
    generate_plot,
    create_research_note,
)

os.makedirs("workspace", exist_ok=True)


def section(title):
    print(f"\n{'═' * 70}")
    print(f"  {title}")
    print(f"{'═' * 70}\n")


def main():
    print("=" * 70)
    print("  Orchestral AI — Scientific Research Workflow Demo")
    print("  Inspired by ASTER (Exoplanet Research, Section 7.2)")
    print("  Framework: orchestral-ai v1.3.0")
    print("=" * 70)

    # ── Step 1: List available planets ────────────────────────────────────
    section("STEP 1: Query Exoplanet Catalog")
    result = list_available_planets.execute()
    print(result)

    # ── Step 2: Fetch detailed data for WASP-39b ─────────────────────────
    section("STEP 2: Retrieve Planetary Data — WASP-39b")
    result = fetch_planetary_data.execute(planet_name="WASP-39b")
    print(result)

    # ── Step 3: Compute transit depth ────────────────────────────────────
    section("STEP 3: Compute Transit Depth")
    # WASP-39b: R = 1.27 R_Jupiter, host star R ≈ 0.895 R_Sun
    result = compute_transit_depth.execute(
        planet_radius_rj=1.27, star_radius_rsun=0.895
    )
    print(result)

    # ── Step 4: Habitable zone estimation ────────────────────────────────
    section("STEP 4: Estimate Habitable Zone of WASP-39 System")
    # WASP-39: T_eff ≈ 5485 K, L ≈ 0.75 L_Sun
    result = compute_habitable_zone.execute(
        star_temp_k=5485, star_luminosity_lsun=0.75
    )
    print(result)

    # ── Step 5: Statistical analysis ─────────────────────────────────────
    section("STEP 5: Statistical Analysis of Equilibrium Temperatures")
    # Temperatures of all 5 catalog planets
    temps = "1166, 1449, 251, 2573, 596"
    result = statistical_analysis.execute(data_csv=temps, label="Equilibrium Temps (K)")
    print(result)

    # ── Step 6: Generate a plot ──────────────────────────────────────────
    section("STEP 6: Generate Visualization")
    masses = "0.28, 0.73, 0.00218, 0.0254, 0.0204"
    result = generate_plot.execute(
        x_values=temps,
        y_values=masses,
        title="Exoplanet Mass vs Equilibrium Temperature",
        x_label="Equilibrium Temperature (K)",
        y_label="Mass (Jupiter masses)",
        plot_type="scatter",
    )
    print(result)

    # ── Step 7: Create research note ─────────────────────────────────────
    section("STEP 7: Save Research Note")
    result = create_research_note.execute(
        title="WASP-39b Transit Analysis",
        content=(
            "WASP-39b is a hot Saturn orbiting WASP-39 with a period of 4.055 days.\n"
            "Transit depth computed at ~2.03%, easily detectable from ground.\n"
            "The planet is well outside the habitable zone (T_eq = 1166 K).\n"
            "JWST has detected H2O, CO2, SO2, Na, and K in its atmosphere.\n"
            "This makes it one of the best-characterized exoplanet atmospheres."
        ),
        tags="exoplanet, WASP-39b, transit, JWST, atmosphere",
    )
    print(result)

    # ── Step 8: Agent conversation (if model available) ──────────────────
    section("STEP 8: Agent Conversational Analysis")
    try:
        from orchestral import Agent
        from orchestral.llm import Ollama

        agent = Agent(
            llm=Ollama(model="devstral-small-2:24b-cloud"),
            system_prompt=(
                "You are a scientific research assistant. Summarize findings concisely. "
                "You just completed a transit analysis of WASP-39b."
            ),
        )
        response = agent.run(
            "Based on the WASP-39b analysis: transit depth ~2.03%, T_eq=1166K, "
            "JWST detected H2O/CO2/SO2/Na/K. What are the key scientific takeaways "
            "and what follow-up observations would you recommend? Keep it brief."
        )
        print(f"🤖 Agent Analysis:\n{response.text}")

        # Cost tracking
        print(f"\n📊 Cost Tracking: ${agent.get_total_cost():.6f}")
        print(f"   (Ollama = $0.00 actual cost)")

    except Exception as e:
        print(f"   Agent not available ({e})")
        print("   The tool workflow above demonstrates full functionality.")

    # ── Summary ──────────────────────────────────────────────────────────
    section("WORKFLOW COMPLETE")
    print("This demo showed all key Orchestral AI concepts:")
    print("  ✅ Custom tool creation via @define_tool()")
    print("  ✅ Scientific Python integration (numpy, matplotlib)")
    print("  ✅ Domain-specific data retrieval (exoplanet catalog)")
    print("  ✅ Computation tools (transit depth, habitable zone)")
    print("  ✅ Statistical analysis and visualization")
    print("  ✅ Research note persistence (reproducibility)")
    print("  ✅ Agent conversational analysis")
    print("  ✅ Automatic cost tracking")
    print()
    print("  Check workspace/ for generated plots and notes!")


if __name__ == "__main__":
    main()
