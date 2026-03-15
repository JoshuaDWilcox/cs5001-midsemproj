"""
Multi-Agent Research Discussion Demo
=======================================

Demonstrates Orchestral AI's multi-agent capabilities in a
scientific research context. Two agents — a "Research Analyst"
and a "Peer Reviewer" — collaborate to evaluate an exoplanet's
habitability potential.

This showcases:
  - Multiple independent Agent instances with different roles
  - Provider-agnostic design (both use Ollama/local models)
  - Programmatic agent-to-agent conversation flow
  - Scientific domain application
  - Automatic cost tracking across agents

Run:
    python multi_agent_demo.py
"""

from orchestral import Agent
from orchestral.llm import Ollama

# ─── Configuration ────────────────────────────────────────────────────────────

MODEL = "devstral-small-2:24b-cloud"
NUM_ROUNDS = 2

# ─── Create Two Specialized Science Agents ───────────────────────────────────

analyst = Agent(
    system_prompt="""You are a Research Analyst specializing in exoplanet characterization.
You present evidence-based findings about exoplanet atmospheres and habitability.
Keep responses concise (2-3 short paragraphs). Cite specific values and data.""",
    llm=Ollama(model=MODEL),
)

reviewer = Agent(
    system_prompt="""You are a Peer Reviewer for astrophysics research.
You critically evaluate claims about exoplanets, checking methodology and assumptions.
Keep responses concise (2-3 short paragraphs). Identify gaps and suggest improvements.""",
    llm=Ollama(model=MODEL),
)

# ─── Run the Multi-Agent Research Discussion ─────────────────────────────────

def run_discussion():
    TOPIC = "the habitability potential of TRAPPIST-1e based on recent JWST observations"

    print("=" * 70)
    print("  MULTI-AGENT SCIENTIFIC DISCUSSION")
    print(f"  Topic: {TOPIC}")
    print(f"  Model: {MODEL} (Ollama — local, $0 cost)")
    print(f"  Rounds: {NUM_ROUNDS}")
    print("=" * 70)

    # Opening analysis
    opening = (
        f"Please present your analysis of {TOPIC}. "
        "TRAPPIST-1e has the following parameters: "
        "Mass = 0.692 Earth masses, Radius = 0.920 Earth radii, "
        "Equilibrium Temperature = 251 K, Orbital Period = 6.1 days. "
        "What can we conclude about its potential for habitability?"
    )
    print(f"\n{'─' * 70}")
    print(f"  MODERATOR: {opening}")
    print(f"{'─' * 70}")

    response = analyst.run(opening)
    print(f"\n🔬 RESEARCH ANALYST:\n{response.text}\n")

    # Multi-round peer review
    for round_num in range(1, NUM_ROUNDS + 1):
        print(f"\n{'━' * 70}")
        print(f"  ROUND {round_num} of {NUM_ROUNDS}")
        print(f"{'━' * 70}")

        # Reviewer critiques
        review = reviewer.run(
            f"The research analyst presents:\n\n\"{response.text}\"\n\n"
            "Evaluate their methodology and conclusions. "
            "What assumptions should be questioned? What additional data is needed?"
        )
        print(f"\n📋 PEER REVIEWER:\n{review.text}\n")

        # Analyst responds
        response = analyst.run(
            f"The peer reviewer raises these points:\n\n\"{review.text}\"\n\n"
            "Address their concerns and refine your analysis."
        )
        print(f"\n🔬 RESEARCH ANALYST:\n{response.text}\n")

    # Final summary
    print(f"\n{'═' * 70}")
    print(f"  DISCUSSION COMPLETE")
    print(f"{'═' * 70}")

    # Cost tracking demonstration
    analyst_cost = analyst.get_total_cost()
    reviewer_cost = reviewer.get_total_cost()
    total = analyst_cost + reviewer_cost

    print(f"\n📊 Cost Tracking (Key Orchestral Feature):")
    print(f"   Analyst agent:  ${analyst_cost:.6f}")
    print(f"   Reviewer agent: ${reviewer_cost:.6f}")
    print(f"   Total cost:     ${total:.6f}")
    print(f"   (Ollama = local inference, actual monetary cost is $0.00)")
    print(f"\n   Note: With a cloud provider (Claude, GPT-4), these costs")
    print(f"   would reflect real API usage — Orchestral tracks this")
    print(f"   automatically for reproducibility and budgeting.\n")


if __name__ == "__main__":
    run_discussion()
