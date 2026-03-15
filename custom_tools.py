"""
Scientific Research Tools Module
==================================

Custom tools for a scientific data analysis agent, inspired by the
ASTER (Agentic Science Toolkit for Exoplanet Research) use case
from the Orchestral AI paper (Section 7.2).

This module demonstrates:
  - Domain-specific tool creation via @define_tool()
  - Integration with scientific Python (numpy, scipy, matplotlib)
  - Data retrieval, statistical analysis, and visualization tools
  - Reproducible research workflows
"""

import os
import json
import math
import datetime
import numpy as np
from orchestral import define_tool

WORKSPACE = "workspace"
os.makedirs(WORKSPACE, exist_ok=True)


# ─── Data Retrieval Tools ─────────────────────────────────────────────────────

@define_tool()
def fetch_planetary_data(planet_name: str) -> str:
    """Retrieve planetary parameters from a built-in catalog of known exoplanets.
    Simulates querying the NASA Exoplanet Archive, as in the ASTER use case.

    Args:
        planet_name: Name of the planet (e.g., "WASP-39b", "HD 209458b", "TRAPPIST-1e")

    Returns:
        JSON-formatted planetary parameters including mass, radius, temperature, etc.
    """
    # Built-in catalog of notable exoplanets (real data from NASA Exoplanet Archive)
    catalog = {
        "WASP-39b": {
            "name": "WASP-39b",
            "host_star": "WASP-39",
            "discovery_year": 2011,
            "mass_jupiter": 0.28,
            "radius_jupiter": 1.27,
            "orbital_period_days": 4.055,
            "equilibrium_temp_k": 1166,
            "distance_pc": 213.9,
            "detection_method": "Transit",
            "atmosphere": "H2O, CO2, SO2, Na, K detected (JWST)",
        },
        "HD 209458b": {
            "name": "HD 209458b (Osiris)",
            "host_star": "HD 209458",
            "discovery_year": 1999,
            "mass_jupiter": 0.73,
            "radius_jupiter": 1.39,
            "orbital_period_days": 3.525,
            "equilibrium_temp_k": 1449,
            "distance_pc": 48.3,
            "detection_method": "Transit / Radial Velocity",
            "atmosphere": "Na, H, C, O detected",
        },
        "TRAPPIST-1e": {
            "name": "TRAPPIST-1e",
            "host_star": "TRAPPIST-1",
            "discovery_year": 2017,
            "mass_jupiter": 0.00218,
            "radius_jupiter": 0.0823,
            "orbital_period_days": 6.101,
            "equilibrium_temp_k": 251,
            "distance_pc": 12.43,
            "detection_method": "Transit",
            "atmosphere": "Under investigation (JWST)",
        },
        "55 Cancri e": {
            "name": "55 Cancri e",
            "host_star": "55 Cancri A",
            "discovery_year": 2004,
            "mass_jupiter": 0.0254,
            "radius_jupiter": 0.169,
            "orbital_period_days": 0.737,
            "equilibrium_temp_k": 2573,
            "distance_pc": 12.59,
            "detection_method": "Radial Velocity",
            "atmosphere": "Possible volcanic atmosphere (JWST)",
        },
        "GJ 1214b": {
            "name": "GJ 1214b",
            "host_star": "GJ 1214",
            "discovery_year": 2009,
            "mass_jupiter": 0.0204,
            "radius_jupiter": 0.244,
            "orbital_period_days": 1.580,
            "equilibrium_temp_k": 596,
            "distance_pc": 14.65,
            "detection_method": "Transit",
            "atmosphere": "High mean molecular weight atmosphere (JWST)",
        },
    }

    # Normalize lookup
    key = planet_name.strip().upper().replace(" ", "")
    for k, v in catalog.items():
        if k.upper().replace(" ", "") == key:
            return (
                f"📡 Planetary Data Retrieved: {v['name']}\n"
                f"```json\n{json.dumps(v, indent=2)}\n```"
            )

    available = ", ".join(catalog.keys())
    return (
        f"❌ Planet '{planet_name}' not found in catalog.\n"
        f"Available planets: {available}"
    )


@define_tool()
def list_available_planets() -> str:
    """List all planets available in the built-in exoplanet catalog.

    Returns:
        A formatted list of available planets with key properties
    """
    planets = [
        ("WASP-39b",     1166, 0.28,   "Hot Saturn, JWST target"),
        ("HD 209458b",   1449, 0.73,   "First transiting exoplanet"),
        ("TRAPPIST-1e",   251, 0.00218, "Habitable zone rocky planet"),
        ("55 Cancri e",  2573, 0.0254,  "Super-Earth, lava world"),
        ("GJ 1214b",      596, 0.0204,  "Sub-Neptune, water world"),
    ]
    lines = ["🌍 Available Exoplanets in Catalog:\n"]
    lines.append(f"  {'Name':<15} {'Temp (K)':<10} {'Mass (Mj)':<12} {'Description'}")
    lines.append(f"  {'-'*15} {'-'*10} {'-'*12} {'-'*30}")
    for name, temp, mass, desc in planets:
        lines.append(f"  {name:<15} {temp:<10} {mass:<12.4f} {desc}")
    return "\n".join(lines)


# ─── Analysis Tools ──────────────────────────────────────────────────────────

@define_tool()
def compute_transit_depth(planet_radius_rj: float, star_radius_rsun: float) -> str:
    """Compute the expected transit depth for an exoplanet transiting its host star.
    Transit depth = (R_planet / R_star)^2, expressed as a percentage.

    Args:
        planet_radius_rj: Planet radius in Jupiter radii
        star_radius_rsun: Star radius in Solar radii

    Returns:
        Transit depth as a percentage with interpretation
    """
    # Convert to common units (Solar radii)
    # 1 Jupiter radius = 0.10049 Solar radii
    rp_rsun = planet_radius_rj * 0.10049
    depth = (rp_rsun / star_radius_rsun) ** 2 * 100  # percent

    interpretation = (
        "easily detectable from ground" if depth > 1.0
        else "detectable with space telescopes" if depth > 0.01
        else "extremely challenging to detect"
    )

    return (
        f"🌑 Transit Depth Calculation:\n"
        f"  Planet radius:  {planet_radius_rj:.3f} R_Jupiter ({rp_rsun:.4f} R_Sun)\n"
        f"  Star radius:    {star_radius_rsun:.3f} R_Sun\n"
        f"  Transit depth:  {depth:.4f}%\n"
        f"  Assessment:     {interpretation}"
    )


@define_tool()
def compute_habitable_zone(star_temp_k: float, star_luminosity_lsun: float) -> str:
    """Estimate the habitable zone boundaries for a star based on its properties.
    Uses the conservative habitable zone model.

    Args:
        star_temp_k: Effective temperature of the star in Kelvin
        star_luminosity_lsun: Luminosity of the star in Solar luminosities

    Returns:
        Inner and outer habitable zone boundaries in AU
    """
    # Conservative HZ boundaries (Kopparapu et al. 2013 approximation)
    inner_au = math.sqrt(star_luminosity_lsun / 1.1)
    outer_au = math.sqrt(star_luminosity_lsun / 0.36)

    return (
        f"🟢 Habitable Zone Estimate:\n"
        f"  Star temperature:  {star_temp_k:.0f} K\n"
        f"  Star luminosity:   {star_luminosity_lsun:.4f} L_Sun\n"
        f"  Inner HZ boundary: {inner_au:.3f} AU\n"
        f"  Outer HZ boundary: {outer_au:.3f} AU\n"
        f"  HZ width:          {outer_au - inner_au:.3f} AU"
    )


@define_tool()
def statistical_analysis(data_csv: str, label: str = "Dataset") -> str:
    """Perform statistical analysis on a comma-separated list of numerical values.
    Uses numpy for computation — demonstrating scientific Python integration.

    Args:
        data_csv: Comma-separated numerical values (e.g., "1.2, 3.4, 5.6, 7.8")
        label: Optional label for the dataset

    Returns:
        Statistical summary including mean, median, std dev, and percentiles
    """
    try:
        data = np.array([float(x.strip()) for x in data_csv.split(",")])
    except ValueError:
        return "❌ Error: Please provide valid comma-separated numbers."

    n = len(data)
    result = (
        f"📊 Statistical Analysis: {label} (n={n})\n"
        f"  ──────────────────────────────\n"
        f"  Mean:          {np.mean(data):.4f}\n"
        f"  Median:        {np.median(data):.4f}\n"
        f"  Std Deviation: {np.std(data):.4f}\n"
        f"  Min:           {np.min(data):.4f}\n"
        f"  Max:           {np.max(data):.4f}\n"
        f"  25th %-ile:    {np.percentile(data, 25):.4f}\n"
        f"  75th %-ile:    {np.percentile(data, 75):.4f}\n"
        f"  IQR:           {np.percentile(data, 75) - np.percentile(data, 25):.4f}"
    )
    return result


@define_tool()
def generate_plot(
    x_values: str,
    y_values: str,
    title: str = "Plot",
    x_label: str = "X",
    y_label: str = "Y",
    plot_type: str = "scatter",
) -> str:
    """Generate a matplotlib plot and save it as a PNG image in the workspace.
    Demonstrates scientific Python integration for visualization.

    Args:
        x_values: Comma-separated X values (e.g., "1, 2, 3, 4, 5")
        y_values: Comma-separated Y values (e.g., "2.1, 4.0, 5.9, 8.1, 9.8")
        title: Plot title
        x_label: X-axis label
        y_label: Y-axis label
        plot_type: Type of plot - "scatter", "line", or "bar"

    Returns:
        Confirmation message with saved file path
    """
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend
    import matplotlib.pyplot as plt

    try:
        x = [float(v.strip()) for v in x_values.split(",")]
        y = [float(v.strip()) for v in y_values.split(",")]
    except ValueError:
        return "❌ Error: Please provide valid comma-separated numbers for X and Y."

    if len(x) != len(y):
        return f"❌ Error: X ({len(x)} values) and Y ({len(y)} values) must have the same length."

    fig, ax = plt.subplots(figsize=(8, 5))
    if plot_type == "scatter":
        ax.scatter(x, y, c="#2196F3", alpha=0.7, edgecolors="#1565C0", s=60)
    elif plot_type == "line":
        ax.plot(x, y, "-o", color="#4CAF50", markersize=6)
    elif plot_type == "bar":
        ax.bar(x, y, color="#FF9800", edgecolor="#E65100", alpha=0.8)
    else:
        ax.scatter(x, y)

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plot_{timestamp}.png"
    filepath = os.path.join(WORKSPACE, filename)
    fig.savefig(filepath, dpi=150)
    plt.close(fig)

    return f"📈 Plot saved to: {filepath}\n  Title: {title}\n  Type: {plot_type}\n  Data points: {len(x)}"


@define_tool()
def create_research_note(title: str, content: str, tags: str = "") -> str:
    """Create a structured research note and save it to the workspace.
    Supports reproducible research workflows by persisting notes as files.

    Args:
        title: Title of the research note
        content: The note content/body
        tags: Optional comma-separated tags (e.g., "exoplanet, atmosphere, JWST")

    Returns:
        Confirmation with file path
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    tag_str = ", ".join(tag_list) if tag_list else "untagged"

    note = (
        f"# {title}\n\n"
        f"**Date:** {timestamp}\n"
        f"**Tags:** {tag_str}\n\n"
        f"---\n\n"
        f"{content}\n"
    )

    safe_title = "".join(c if c.isalnum() or c in "-_ " else "" for c in title)
    safe_title = safe_title.replace(" ", "_").lower()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"note_{safe_title}_{ts}.md"
    filepath = os.path.join(WORKSPACE, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(note)

    return (
        f"📝 Research Note Saved!\n"
        f"  File: {filepath}\n"
        f"  Title: {title}\n"
        f"  Tags: {tag_str}"
    )


# ─── Export all tools ─────────────────────────────────────────────────────────

ALL_TOOLS = [
    fetch_planetary_data,
    list_available_planets,
    compute_transit_depth,
    compute_habitable_zone,
    statistical_analysis,
    generate_plot,
    create_research_note,
]
