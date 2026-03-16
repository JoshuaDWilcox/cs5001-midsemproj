"""
Scientific Research Workflow Demo
===================================

Demonstrates the ASTER-inspired research agent workflow programmatically.
This script shows tools being invoked through the Orchestral AI agent,
showcasing all key concepts from the paper.

Run:
    python research_demo.py
"""

import os
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


def step(num, title, result):
    print(f"  [{num}/8] {title}")
    for line in str(result).strip().split("\n"):
        print(f"       {line}")
    print()


def main():
    print("=" * 60)
    print("  Orchestral AI — Scientific Research Workflow")
    print("  ASTER-Inspired (Section 7.2) | orchestral-ai v1.3.0")
    print("=" * 60)
    print()

    step(1, "Query Exoplanet Catalog",
         list_available_planets.execute())

    step(2, "Retrieve WASP-39b Data",
         fetch_planetary_data.execute(planet_name="WASP-39b"))

    step(3, "Compute Transit Depth",
         compute_transit_depth.execute(planet_radius_rj=1.27, star_radius_rsun=0.895))

    step(4, "Estimate Habitable Zone (WASP-39)",
         compute_habitable_zone.execute(star_temp_k=5485, star_luminosity_lsun=0.75))

    temps = "1166, 1449, 251, 2573, 596"
    step(5, "Statistical Analysis (Equilibrium Temps)",
         statistical_analysis.execute(data_csv=temps, label="Equilibrium Temps (K)"))

    masses = "0.28, 0.73, 0.00218, 0.0254, 0.0204"
    step(6, "Generate Scatter Plot",
         generate_plot.execute(
             x_values=temps, y_values=masses,
             title="Exoplanet Mass vs Equilibrium Temperature",
             x_label="Equilibrium Temperature (K)",
             y_label="Mass (Jupiter masses)", plot_type="scatter"))

    step(7, "Save Research Note",
         create_research_note.execute(
             title="WASP-39b Transit Analysis",
             content="Transit depth ~2.03%. T_eq=1166K. JWST detected H2O, CO2, SO2, Na, K.",
             tags="exoplanet, WASP-39b, transit, JWST"))

    # Step 8: LLM agent analysis
    print(f"  [8/8] Agent Conversational Analysis")
    try:
        from orchestral import Agent
        from orchestral.llm import Ollama
        agent = Agent(
            llm=Ollama(model="devstral-small-2:24b-cloud"),
            system_prompt="You are a scientific research assistant. Be very concise (3-4 sentences max).",
        )
        response = agent.run(
            "WASP-39b: transit depth ~2.03%, T_eq=1166K, JWST detected H2O/CO2/SO2/Na/K. "
            "Give 2 key takeaways and 1 follow-up observation in 3 sentences."
        )
        for line in response.text.strip().split("\n"):
            print(f"       {line}")
        print(f"\n       📊 Cost: ${agent.get_total_cost():.6f} (Ollama = $0 actual)")
    except Exception as e:
        print(f"       Agent unavailable ({e})")

    print()
    print("=" * 60)
    print("  ✅ COMPLETE — All 8 Orchestral AI concepts demonstrated")
    print("  Check workspace/ for plots and notes!")
    print("=" * 60)


if __name__ == "__main__":
    main()
