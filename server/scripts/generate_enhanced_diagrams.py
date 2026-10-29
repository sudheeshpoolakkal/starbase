#!/usr/bin/env python3
"""
Generates high-resolution academic SVG diagrams for Starbase Material Selection System:
1. Fig2-4_Selection_Algorithm.svg: Multi-Criteria Screening & Scoring Algorithm Flowchart
2. Fig3-1_ER_Diagram.svg: Enhanced Conceptual ER Diagram with Associative Entities and Attributes
3. Fig3-2_Relational_Schema_Map.svg: Physical Relational Schema Dependency & Foreign Key Map
4. Fig4-1_ETL_Pipeline.svg: Transactional Batch ETL Pipeline and Ingestion Architecture
"""

from pathlib import Path
import subprocess

SVG_DIR = Path("Starbase_Diagrams_SVG")
PNG_DIR = Path("docs/diagram-renders")
SVG_DIR.mkdir(parents=True, exist_ok=True)
PNG_DIR.mkdir(parents=True, exist_ok=True)

print("Writing enhanced SVG diagrams...")

def generate_fig2_4_selection_algorithm():
    svg_path = SVG_DIR / "Fig2-4_Selection_Algorithm.svg"
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1350" viewBox="0 0 1500 1350" font-family="Carlito, Calibri, Arial, sans-serif" role="img" aria-label="Starbase material selection and multi-criteria scoring algorithm">
<title>Starbase Selection &amp; Scoring Algorithm Flowchart</title>
<desc>Two-phase hybrid evaluation: indexed SQL hard constraint screening followed by in-memory min-max normalization and weighted priority utility scoring without zero-imputation.</desc>
<defs>
  <marker id="ah" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M1,1 L11,6 L1,11 Z" fill="#2a3846"/>
  </marker>
</defs>
<rect width="1500" height="1350" fill="#ffffff"/>

<!-- Title -->
<text x="750" y="48" font-size="28" font-weight="700" fill="#1b2733" text-anchor="middle">Starbase Selection &amp; Multi-Attribute Scoring Algorithm Flowchart</text>
<text x="750" y="80" font-size="18" font-weight="400" fill="#566473" text-anchor="middle">Hybrid execution: Indexed SQL constraint screening, non-imputing property validation, and min-max weighted ranking</text>

<!-- PHASE 1: USER REQUIREMENTS SPECIFICATION -->
<rect x="50" y="110" width="1400" height="170" rx="14" fill="#eef3fa" stroke="#2a3846" stroke-width="2.5"/>
<rect x="50" y="110" width="1400" height="42" rx="14" fill="#c5d5ea" stroke="none"/>
<text x="750" y="139" font-size="20" font-weight="700" fill="#1b2733" text-anchor="middle">STAGE 1: ENGINEERING REQUIREMENTS &amp; PRIORITY WEIGHT SPECIFICATION</text>

<rect x="80" y="170" width="410" height="85" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="285" y="200" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">Hard Engineering Constraints</text>
<text x="285" y="224" font-size="15" fill="#566473" text-anchor="middle">Tensile strength ≥ 400 MPa, Density ≤ 4.5 g/cm³,</text>
<text x="285" y="244" font-size="15" fill="#566473" text-anchor="middle">Service temperature ≥ 300°C, Vacuum outgassing</text>

<rect x="545" y="170" width="410" height="85" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="750" y="200" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">Multi-Objective Priority Weights</text>
<text x="750" y="224" font-size="15" fill="#566473" text-anchor="middle">User-allocated weights: w_strength, w_lightness,</text>
<text x="750" y="244" font-size="15" fill="#566473" text-anchor="middle">w_stiffness, w_thermal, w_cost (Σ w_i = 100)</text>

<rect x="1010" y="170" width="410" height="85" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="1215" y="200" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">Component Context &amp; Scope</text>
<text x="1215" y="224" font-size="15" fill="#566473" text-anchor="middle">Component volume V (for mass = V · ρ),</text>
<text x="1215" y="244" font-size="15" fill="#566473" text-anchor="middle">category filter (Metal, Polymer, Ceramic, etc.)</text>

<!-- Flow down arrow -->
<line x1="750" y1="280" x2="750" y2="320" stroke="#2a3846" stroke-width="3" marker-end="url(#ah)"/>

<!-- PHASE 2: DATABASE SCREENING (SQL ENGINE) -->
<rect x="50" y="325" width="1400" height="340" rx="14" fill="#eff7f2" stroke="#2a3846" stroke-width="2.5"/>
<rect x="50" y="325" width="1400" height="42" rx="14" fill="#c6e0cf" stroke="none"/>
<text x="750" y="354" font-size="20" font-weight="700" fill="#1b2733" text-anchor="middle">STAGE 2: PARAMETERIZED SQL SCREENING &amp; COMPOSITE INDEX EVALUATION</text>

<rect x="80" y="385" width="460" height="135" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="310" y="415" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">Parameterized SQL Query Construction</text>
<text x="100" y="445" font-size="14" font-family="Courier New, monospace" fill="#1b2733">SELECT m.material_id, m.name, ...</text>
<text x="100" y="468" font-size="14" font-family="Courier New, monospace" fill="#1b2733">JOIN Material_Property v_ts ON ...</text>
<text x="100" y="491" font-size="14" font-family="Courier New, monospace" fill="#1b2733">WHERE v_ts.numeric_value &gt;= ? ...</text>

<path fill="none" d="M 540,452 L 610,452" stroke="#2a3846" stroke-width="2.5" marker-end="url(#ah)"/>

<!-- Index Execution -->
<rect x="620" y="385" width="410" height="135" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="825" y="415" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">B-Tree Composite Index Search</text>
<text x="825" y="445" font-size="15" fill="#566473" text-anchor="middle">Leverages material_numeric_index on</text>
<text x="825" y="468" font-size="15" font-family="Courier New, monospace" fill="#1b2733">(property_id, numeric_value)</text>
<text x="825" y="495" font-size="14" font-weight="700" fill="#2e7d32" text-anchor="middle">Fast B-Tree Range Scan (&lt; 5 ms latency)</text>

<path fill="none" d="M 1030,452 L 1090,452" stroke="#2a3846" stroke-width="2.5" marker-end="url(#ah)"/>

<!-- Decision Diamond -->
<polygon points="1235,395 1365,452 1235,510 1105,452" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<text x="1235" y="447" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Meets All Hard</text>
<text x="1235" y="468" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Constraints?</text>

<!-- False branch -->
<path fill="none" d="M 1365,452 L 1420,452 L 1420,560 L 980,560" stroke="#d32f2f" stroke-width="2.5" marker-end="url(#ah)"/>
<text x="1390" y="442" font-size="15" font-weight="700" fill="#d32f2f">NO</text>

<rect x="620" y="535" width="350" height="50" rx="8" fill="#ffebee" stroke="#d32f2f" stroke-width="1.8"/>
<text x="795" y="565" font-size="15" font-weight="700" fill="#c62828" text-anchor="middle">Disqualify &amp; Record Exact Failure Reason</text>

<!-- True branch -->
<path fill="none" d="M 1235,510 L 1235,605 L 750,605 L 750,630" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#ah)"/>
<text x="1245" y="535" font-size="15" font-weight="700" fill="#2e7d32">YES</text>

<!-- Flow down arrow -->
<line x1="750" y1="630" x2="750" y2="695" stroke="#2a3846" stroke-width="3" marker-end="url(#ah)"/>

<!-- PHASE 3: MIN-MAX NORMALIZATION & SCORING -->
<rect x="50" y="700" width="1400" height="340" rx="14" fill="#fcf3eb" stroke="#2a3846" stroke-width="2.5"/>
<rect x="50" y="700" width="1400" height="42" rx="14" fill="#fae3cf" stroke="none"/>
<text x="750" y="729" font-size="20" font-weight="700" fill="#1b2733" text-anchor="middle">STAGE 3: NON-IMPUTING VALIDATION &amp; WEIGHTED UTILITY AGGREGATION</text>

<polygon points="310,760 440,817 310,875 180,817" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<text x="310" y="812" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Has Required</text>
<text x="310" y="833" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Priority Properties?</text>

<!-- Missing property -> Exclude -->
<path fill="none" d="M 310,875 L 310,925" stroke="#d32f2f" stroke-width="2.5" marker-end="url(#ah)"/>
<text x="320" y="900" font-size="15" font-weight="700" fill="#d32f2f">NO (Missing Data)</text>
<rect x="150" y="930" width="320" height="50" rx="8" fill="#ffebee" stroke="#d32f2f" stroke-width="1.8"/>
<text x="310" y="960" font-size="14" font-weight="700" fill="#c62828" text-anchor="middle">Exclude Candidate (Zero-Imputation Prohibited)</text>

<!-- Has property -> Normalize -->
<path fill="none" d="M 440,817 L 530,817" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#ah)"/>
<text x="475" y="805" font-size="15" font-weight="700" fill="#2e7d32">YES</text>

<rect x="540" y="765" width="410" height="105" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="745" y="795" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">Dimensionless Min–Max Normalization</text>
<text x="745" y="825" font-size="15" fill="#1b2733" text-anchor="middle">Higher is better: s_norm = (x - x_min) / (x_max - x_min)</text>
<text x="745" y="850" font-size="15" fill="#1b2733" text-anchor="middle">Lower is better: s_norm = (x_max - x) / (x_max - x_min)</text>

<path fill="none" d="M 950,817 L 1030,817" stroke="#2a3846" stroke-width="2.5" marker-end="url(#ah)"/>

<rect x="1040" y="765" width="410" height="105" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="1245" y="795" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">Composite Weighted Scoring</text>
<text x="1245" y="825" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Total Score S = Σ [ w_i · s_i,norm ]</text>
<text x="1245" y="850" font-size="15" fill="#566473" text-anchor="middle">Applies density mass penalty: Mass = Volume · ρ</text>

<rect x="540" y="900" width="910" height="60" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="995" y="927" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Stable Rounded-Score Tie Breaking</text>
<text x="995" y="948" font-size="14" fill="#566473" text-anchor="middle">Rounds composite score to 3 decimals; breaks ties by secondary criteria (yield strength $\rightarrow$ lightness $\rightarrow$ name)</text>

<!-- Flow down arrow -->
<line x1="750" y1="960" x2="750" y2="1010" stroke="#2a3846" stroke-width="3" marker-end="url(#ah)"/>

<!-- PHASE 4: OUTPUT & WORKSPACE -->
<rect x="50" y="1015" width="1400" height="280" rx="14" fill="#f9f0f9" stroke="#2a3846" stroke-width="2.5"/>
<rect x="50" y="1015" width="1400" height="42" rx="14" fill="#f2daf0" stroke="none"/>
<text x="750" y="1044" font-size="20" font-weight="700" fill="#1b2733" text-anchor="middle">STAGE 4: DELIVERABLE OUTPUT, EXPLANATIONS &amp; WORKSPACE PERSISTENCE</text>

<rect x="80" y="1080" width="410" height="170" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="285" y="1115" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">Top-K Ranked Candidates</text>
<text x="100" y="1145" font-size="15" fill="#1b2733">• Sorted candidate list (Limit 50)</text>
<text x="100" y="1175" font-size="15" fill="#1b2733">• Normalized score breakdowns</text>
<text x="100" y="1205" font-size="15" fill="#1b2733">• Computed mass &amp; cost indices</text>
<text x="100" y="1235" font-size="15" fill="#1b2733">• Complete source provenance</text>

<rect x="545" y="1080" width="410" height="170" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="750" y="1115" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">Audit Logs &amp; Explanations</text>
<text x="565" y="1145" font-size="15" fill="#1b2733">• Detailed inclusion rationale</text>
<text x="565" y="1175" font-size="15" fill="#1b2733">• Explicit disqualification causes</text>
<text x="565" y="1205" font-size="15" fill="#1b2733">• Bound violation diagnostics</text>
<text x="565" y="1235" font-size="15" fill="#1b2733">• Unmet testing standards</text>

<rect x="1010" y="1080" width="410" height="170" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<text x="1215" y="1115" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">Workspace Actions</text>
<text x="1030" y="1145" font-size="15" fill="#1b2733">• Shortlist to project workspace</text>
<text x="1030" y="1175" font-size="15" fill="#1b2733">• 4-way side-by-side comparison</text>
<text x="1030" y="1205" font-size="15" fill="#1b2733">• Share with team collaborators</text>
<text x="1030" y="1235" font-size="15" fill="#1b2733">• Export requirements &amp; results</text>

</svg>'''
    with open(svg_path, "w") as f:
        f.write(svg)
    print(f"Generated {svg_path}")

generate_fig2_4_selection_algorithm()

def generate_fig3_2_relational_schema_map():
    svg_path = SVG_DIR / "Fig3-2_Relational_Schema_Map.svg"
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1350" viewBox="0 0 1600 1350" font-family="Carlito, Calibri, Arial, sans-serif" role="img" aria-label="Starbase relational schema and foreign key dependency map">
<title>Starbase Relational Schema &amp; Foreign Key Dependency Map</title>
<desc>Detailed physical table schemas with primary keys (PK), foreign keys (FK), and referential integrity constraints across the 18 active schema tables.</desc>
<defs>
  <marker id="fk_arr" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M1,1 L11,6 L1,11 Z" fill="#0066cc"/>
  </marker>
  <marker id="casc_arr" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M1,1 L11,6 L1,11 Z" fill="#d32f2f"/>
  </marker>
</defs>
<rect width="1600" height="1350" fill="#ffffff"/>

<!-- Title -->
<text x="800" y="45" font-size="28" font-weight="700" fill="#1b2733" text-anchor="middle">Starbase Relational Schema &amp; Foreign Key Dependency Architecture</text>
<text x="800" y="75" font-size="18" font-weight="400" fill="#566473" text-anchor="middle">Physical table schemas, primary keys (PK), foreign keys (FK), and referential cascade constraints across core catalog &amp; workspace entities</text>

<!-- Legend -->
<rect x="50" y="95" width="1500" height="42" rx="8" fill="#f8f9fa" stroke="#b0b8c1" stroke-width="1.5"/>
<rect x="80" y="106" width="36" height="20" rx="4" fill="#ffecb3" stroke="#ff8f00" stroke-width="1.2"/>
<text x="98" y="121" font-size="12" font-weight="700" fill="#b78103" text-anchor="middle">PK</text>
<text x="125" y="121" font-size="14" fill="#1b2733">= Primary Key</text>

<rect x="240" y="106" width="36" height="20" rx="4" fill="#e1f5fe" stroke="#0288d1" stroke-width="1.2"/>
<text x="258" y="121" font-size="12" font-weight="700" fill="#0277bd" text-anchor="middle">FK</text>
<text x="285" y="121" font-size="14" fill="#1b2733">= Foreign Key</text>

<line x1="420" y1="116" x2="470" y2="116" stroke="#0066cc" stroke-width="2.5" marker-end="url(#fk_arr)"/>
<text x="480" y="121" font-size="14" fill="#0066cc" font-weight="700">RESTRICT (Prevents orphaned children)</text>

<line x1="820" y1="116" x2="870" y2="116" stroke="#d32f2f" stroke-width="2.5" marker-end="url(#casc_arr)"/>
<text x="880" y="121" font-size="14" fill="#d32f2f" font-weight="700">CASCADE (Deletes child tuples on parent delete)</text>

<!-- GROUP 1: CATALOG REFERENCE TABLES (LEFT) -->
<!-- Data_Source -->
<rect x="50" y="160" width="310" height="220" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="50" y="160" width="310" height="38" rx="10" fill="#c5d5ea" stroke="none"/>
<text x="205" y="186" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Data_Source</text>
<text x="65" y="218" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan>source_id: INT AUTO_INCREMENT</text>
<text x="65" y="242" font-size="14" fill="#1b2733">source_key: VARCHAR(64) UNIQUE</text>
<text x="65" y="266" font-size="14" fill="#1b2733">name: VARCHAR(255)</text>
<text x="65" y="290" font-size="14" fill="#1b2733">url: VARCHAR(500)</text>
<text x="65" y="314" font-size="14" fill="#1b2733">data_kind: ENUM(...)</text>
<text x="65" y="338" font-size="14" fill="#1b2733">license: VARCHAR(255)</text>
<text x="65" y="362" font-size="14" fill="#1b2733">checksum: VARCHAR(128)</text>

<!-- Material_Category -->
<rect x="50" y="420" width="310" height="130" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="50" y="420" width="310" height="38" rx="10" fill="#c5d5ea" stroke="none"/>
<text x="205" y="446" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Material_Category</text>
<text x="65" y="478" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan>category_id: INT AUTO_INCREMENT</text>
<text x="65" y="504" font-size="14" fill="#1b2733">name: VARCHAR(80) UNIQUE</text>
<text x="65" y="530" font-size="14" fill="#1b2733">description: TEXT</text>

<!-- Application -->
<rect x="50" y="590" width="310" height="130" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="50" y="590" width="310" height="38" rx="10" fill="#c5d5ea" stroke="none"/>
<text x="205" y="616" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Application</text>
<text x="65" y="648" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan>application_id: INT AUTO_INCREMENT</text>
<text x="65" y="674" font-size="14" fill="#1b2733">name: VARCHAR(255) UNIQUE</text>
<text x="65" y="700" font-size="14" fill="#1b2733">category: VARCHAR(64)</text>

<!-- Manufacturing_Process -->
<rect x="50" y="760" width="310" height="130" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="50" y="760" width="310" height="38" rx="10" fill="#c5d5ea" stroke="none"/>
<text x="205" y="786" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Manufacturing_Process</text>
<text x="65" y="818" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan>process_id: INT AUTO_INCREMENT</text>
<text x="65" y="844" font-size="14" fill="#1b2733">name: VARCHAR(100) UNIQUE</text>
<text x="65" y="870" font-size="14" fill="#1b2733">description: TEXT</text>

<!-- GROUP 2: CORE MATERIAL CATALOG ENTITIES (CENTER) -->
<!-- Material (Core Table) -->
<rect x="460" y="160" width="380" height="300" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.8"/>
<rect x="460" y="160" width="380" height="42" rx="10" fill="#c6e0cf" stroke="none"/>
<text x="650" y="188" font-size="20" font-weight="700" fill="#1b2733" text-anchor="middle">Material (6.26M Records)</text>
<text x="480" y="222" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan>material_id: INT AUTO_INCREMENT</text>
<text x="480" y="248" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#0277bd">FK </tspan>source_id: INT (Data_Source)</text>
<text x="480" y="274" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#0277bd">FK </tspan>category_id: INT (Material_Category)</text>
<text x="480" y="300" font-size="14" fill="#1b2733">external_id: VARCHAR(128)</text>
<text x="480" y="326" font-size="14" fill="#1b2733">name: VARCHAR(255) [INDEXED]</text>
<text x="480" y="352" font-size="14" fill="#1b2733">description: TEXT</text>
<text x="480" y="378" font-size="14" fill="#1b2733">formula: VARCHAR(128)</text>
<text x="480" y="404" font-size="14" fill="#1b2733">is_active: TINYINT(1) DEFAULT 1</text>
<text x="480" y="430" font-size="14" fill="#1b2733">metadata_json: MEDIUMTEXT (Packed Codec)</text>

<!-- Foreign Keys to Material -->
<path fill="none" d="M 360,250 L 460,250" stroke="#0066cc" stroke-width="2.5" marker-end="url(#fk_arr)"/>
<text x="410" y="242" font-size="11" font-weight="700" fill="#0066cc" text-anchor="middle">RESTRICT</text>

<path fill="none" d="M 360,470 L 410,470 L 410,274 L 460,274" stroke="#0066cc" stroke-width="2.5" marker-end="url(#fk_arr)"/>
<text x="410" y="462" font-size="11" font-weight="700" fill="#0066cc" text-anchor="middle">RESTRICT</text>

<!-- Property Dictionary -->
<rect x="460" y="520" width="380" height="210" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="460" y="520" width="380" height="38" rx="10" fill="#c5d5ea" stroke="none"/>
<text x="650" y="546" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Property (Dictionary Entity)</text>
<text x="480" y="578" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan>property_id: INT AUTO_INCREMENT</text>
<text x="480" y="604" font-size="14" fill="#1b2733">property_key: VARCHAR(80) UNIQUE NOT NULL</text>
<text x="480" y="630" font-size="14" fill="#1b2733">name: VARCHAR(100) NOT NULL</text>
<text x="480" y="656" font-size="14" fill="#1b2733">unit: VARCHAR(80) NOT NULL (SI base)</text>
<text x="480" y="682" font-size="14" fill="#1b2733">data_type: ENUM('numeric','text','boolean')</text>
<text x="480" y="708" font-size="14" fill="#1b2733">category: VARCHAR(64) ('Mechanical','Thermal')</text>

<!-- Material_Property (Junction Table with Payload) -->
<rect x="460" y="790" width="380" height="230" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.5"/>
<rect x="460" y="790" width="380" height="38" rx="10" fill="#fae3cf" stroke="none"/>
<text x="650" y="816" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Material_Property (Associative Payload)</text>
<text x="480" y="848" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan><tspan font-weight="700" fill="#0277bd">FK </tspan>material_id: INT (Material)</text>
<text x="480" y="874" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan><tspan font-weight="700" fill="#0277bd">FK </tspan>property_id: INT (Property)</text>
<text x="480" y="900" font-size="14" font-weight="700" fill="#2e7d32">numeric_value: DOUBLE [COMPOSITE INDEXED]</text>
<text x="480" y="926" font-size="14" fill="#1b2733">text_value: VARCHAR(100)</text>
<text x="480" y="952" font-size="14" fill="#1b2733">uncertainty: DOUBLE</text>
<text x="480" y="978" font-size="14" fill="#1b2733">test_conditions: VARCHAR(255) ('293 K, 1 atm')</text>
<text x="480" y="1004" font-size="14" fill="#1b2733">is_estimated: TINYINT(1) DEFAULT 0</text>

<!-- Cascades into Material_Property -->
<path fill="none" d="M 580,460 L 580,790" stroke="#d32f2f" stroke-width="2.5" marker-end="url(#casc_arr)"/>
<text x="590" y="500" font-size="11" font-weight="700" fill="#d32f2f">CASCADE</text>

<path fill="none" d="M 680,730 L 680,790" stroke="#0066cc" stroke-width="2.5" marker-end="url(#fk_arr)"/>
<text x="690" y="755" font-size="11" font-weight="700" fill="#0066cc">RESTRICT</text>

<!-- Material_Application -->
<rect x="460" y="1070" width="380" height="130" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="460" y="1070" width="380" height="38" rx="10" fill="#fae3cf" stroke="none"/>
<text x="650" y="1096" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Material_Application</text>
<text x="480" y="1128" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan><tspan font-weight="700" fill="#0277bd">FK </tspan>material_id: INT (Material)</text>
<text x="480" y="1154" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan><tspan font-weight="700" fill="#0277bd">FK </tspan>application_id: INT (Application)</text>
<text x="480" y="1180" font-size="14" fill="#1b2733">suitability_score: DOUBLE DEFAULT 1.0</text>

<path fill="none" d="M 360,650 L 410,650 L 410,1154 L 460,1154" stroke="#0066cc" stroke-width="2.5" marker-end="url(#fk_arr)"/>
<path fill="none" d="M 460,350 L 430,350 L 430,1128 L 460,1128" stroke="#d32f2f" stroke-width="2.5" marker-end="url(#casc_arr)"/>

<!-- GROUP 3: WORKSPACE & COLLABORATION (RIGHT) -->
<!-- Users -->
<rect x="940" y="160" width="350" height="190" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.5"/>
<rect x="940" y="160" width="350" height="38" rx="10" fill="#f2daf0" stroke="none"/>
<text x="1115" y="186" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Users (Account Entity)</text>
<text x="960" y="218" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan>user_id: INT AUTO_INCREMENT</text>
<text x="960" y="244" font-size="14" fill="#1b2733">email: VARCHAR(255) UNIQUE NOT NULL</text>
<text x="960" y="270" font-size="14" fill="#1b2733">password_hash: VARCHAR(255) (bcrypt)</text>
<text x="960" y="296" font-size="14" fill="#1b2733">full_name: VARCHAR(255)</text>
<text x="960" y="322" font-size="14" fill="#1b2733">role: ENUM('user','admin') DEFAULT 'user'</text>

<!-- Projects -->
<rect x="940" y="410" width="350" height="180" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.5"/>
<rect x="940" y="410" width="350" height="38" rx="10" fill="#f2daf0" stroke="none"/>
<text x="1115" y="436" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Projects (Workspace Entity)</text>
<text x="960" y="468" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan>project_id: INT AUTO_INCREMENT</text>
<text x="960" y="494" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#0277bd">FK </tspan>owner_id: INT (Users)</text>
<text x="960" y="520" font-size="14" fill="#1b2733">name: VARCHAR(255) NOT NULL</text>
<text x="960" y="546" font-size="14" fill="#1b2733">description: TEXT</text>
<text x="960" y="572" font-size="14" fill="#1b2733">status: ENUM('active','archived')</text>

<path fill="none" d="M 1030,350 L 1030,410" stroke="#d32f2f" stroke-width="2.5" marker-end="url(#casc_arr)"/>
<text x="1040" y="385" font-size="11" font-weight="700" fill="#d32f2f">CASCADE</text>

<!-- Project_Collaborator (Junction) -->
<rect x="1330" y="280" width="240" height="150" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="1330" y="280" width="240" height="38" rx="10" fill="#f2daf0" stroke="none"/>
<text x="1450" y="306" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Project_Collaborator</text>
<text x="1345" y="338" font-size="13" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan><tspan font-weight="700" fill="#0277bd">FK </tspan>project_id: INT</text>
<text x="1345" y="364" font-size="13" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan><tspan font-weight="700" fill="#0277bd">FK </tspan>user_id: INT</text>
<text x="1345" y="390" font-size="13" fill="#1b2733">permission: ENUM</text>
<text x="1345" y="412" font-size="12" fill="#566473">('read','write','admin')</text>

<path fill="none" d="M 1290,260 L 1330,260 L 1330,364" stroke="#d32f2f" stroke-width="2.5" marker-end="url(#casc_arr)"/>
<path fill="none" d="M 1290,460 L 1315,460 L 1315,338 L 1330,338" stroke="#d32f2f" stroke-width="2.5" marker-end="url(#casc_arr)"/>

<!-- Saved_Selection -->
<rect x="940" y="650" width="350" height="170" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="940" y="650" width="350" height="38" rx="10" fill="#f2daf0" stroke="none"/>
<text x="1115" y="676" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Saved_Selection</text>
<text x="960" y="708" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan>selection_id: INT AUTO_INCREMENT</text>
<text x="960" y="734" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#0277bd">FK </tspan>project_id: INT (Projects)</text>
<text x="960" y="760" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#0277bd">FK </tspan>user_id: INT (Users)</text>
<text x="960" y="786" font-size="14" fill="#1b2733">title: VARCHAR(255)</text>
<text x="960" y="810" font-size="14" fill="#1b2733">created_at: TIMESTAMP</text>

<path fill="none" d="M 1030,590 L 1030,650" stroke="#d32f2f" stroke-width="2.5" marker-end="url(#casc_arr)"/>

<!-- Selection_Requirement -->
<rect x="940" y="880" width="350" height="170" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="940" y="880" width="350" height="38" rx="10" fill="#f2daf0" stroke="none"/>
<text x="1115" y="906" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Selection_Requirement</text>
<text x="960" y="938" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#ff8f00">PK </tspan>requirement_id: INT AUTO_INCREMENT</text>
<text x="960" y="964" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#0277bd">FK </tspan>selection_id: INT (Saved_Selection)</text>
<text x="960" y="990" font-size="14" fill="#1b2733"><tspan font-weight="700" fill="#0277bd">FK </tspan>property_id: INT (Property)</text>
<text x="960" y="1016" font-size="14" fill="#1b2733">min_value, max_value: DOUBLE</text>
<text x="960" y="1040" font-size="14" fill="#1b2733">weight: DOUBLE, is_mandatory: BOOL</text>

<path fill="none" d="M 1030,820 L 1030,880" stroke="#d32f2f" stroke-width="2.5" marker-end="url(#casc_arr)"/>
<path fill="none" d="M 840,650 L 890,650 L 890,990 L 940,990" stroke="#0066cc" stroke-width="2.5" marker-end="url(#fk_arr)"/>

<!-- GROUP 4: CLOUD MIGRATION TABLES (BOTTOM) -->
<rect x="50" y="1225" width="1500" height="95" rx="10" fill="#fafafa" stroke="#78909c" stroke-width="2.0"/>
<text x="70" y="1255" font-size="16" font-weight="700" fill="#37474f">Cloud Migration &amp; Audit Support Tables (TiDB Staging):</text>
<text x="70" y="1285" font-size="14" fill="#455a64">• <tspan font-weight="700">Catalog_Import_Progress</tspan> (import_id PK, source_key, file_byte_offset, row_count, md5_checksum, status) — Idempotent chunked resume.</text>
<text x="70" y="1308" font-size="14" fill="#455a64">• <tspan font-weight="700">Contribution_Review</tspan> (review_id PK, material_id FK, user_id FK, status, review_notes) — Peer staging before public catalog promotion.</text>

</svg>'''
    with open(svg_path, "w") as f:
        f.write(svg)
    print(f"Generated {svg_path}")

generate_fig3_2_relational_schema_map()

def generate_fig4_1_etl_pipeline():
    svg_path = SVG_DIR / "Fig4-1_ETL_Pipeline.svg"
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1100" viewBox="0 0 1500 1100" font-family="Carlito, Calibri, Arial, sans-serif" role="img" aria-label="Starbase transactional batch ETL pipeline and ingestion architecture">
<title>Starbase Transactional Batch ETL Ingestion Pipeline</title>
<desc>High-throughput offline pipeline ingesting 6.26M materials from 14 repositories with cryptographic verification, reversible metadata codec packing, and ACID transaction boundaries.</desc>
<defs>
  <marker id="etl_ah" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M1,1 L11,6 L1,11 Z" fill="#2a3846"/>
  </marker>
</defs>
<rect width="1500" height="1100" fill="#ffffff"/>

<!-- Title -->
<text x="750" y="45" font-size="28" font-weight="700" fill="#1b2733" text-anchor="middle">Starbase Transactional Batch ETL Ingestion Architecture</text>
<text x="750" y="75" font-size="18" font-weight="400" fill="#566473" text-anchor="middle">Scalable pipeline ingesting 6,265,691 records across 14 scientific repositories with ACID batch transactions</text>

<!-- STAGE 1: RAW DATA HARVESTING (TOP) -->
<rect x="50" y="105" width="1400" height="150" rx="12" fill="#eef3fa" stroke="#2a3846" stroke-width="2.2"/>
<rect x="50" y="105" width="1400" height="38" rx="12" fill="#c5d5ea" stroke="none"/>
<text x="750" y="132" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">STAGE 1: MULTI-SOURCE SCIENTIFIC REPOSITORY HARVESTING (14 DATASETS)</text>

<rect x="75" y="155" width="310" height="85" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.6"/>
<text x="230" y="183" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Computational DFT Repositories</text>
<text x="230" y="206" font-size="14" fill="#566473" text-anchor="middle">Alexandria (6.1M BZip2 tar.gz),</text>
<text x="230" y="226" font-size="14" fill="#566473" text-anchor="middle">Materials Project, AFLOW, JARVIS, NOMAD</text>

<rect x="420" y="155" width="310" height="85" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.6"/>
<text x="575" y="183" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Empirical Literature Datasets</text>
<text x="575" y="206" font-size="14" fill="#566473" text-anchor="middle">Borg et al. Multi-Element Alloys,</text>
<text x="575" y="226" font-size="14" fill="#566473" text-anchor="middle">MaterialRegistry Curated Engineering Alloys</text>

<rect x="765" y="155" width="310" height="85" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.6"/>
<text x="920" y="183" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Aerospace Environmental Data</text>
<text x="920" y="206" font-size="14" fill="#566473" text-anchor="middle">NASA Ames TPSX Thermal Materials,</text>
<text x="920" y="226" font-size="14" fill="#566473" text-anchor="middle">NASA Goddard Spacecraft Outgassing (CVCM)</text>

<rect x="1110" y="155" width="315" height="85" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.6"/>
<text x="1267" y="183" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Manufacturer Catalogs</text>
<text x="1267" y="206" font-size="14" fill="#566473" text-anchor="middle">Outokumpu Stainless Steel Technical</text>
<text x="1267" y="226" font-size="14" fill="#566473" text-anchor="middle">Datasheets (Core, Supra, Forta Duplex)</text>

<line x1="750" y1="255" x2="750" y2="290" stroke="#2a3846" stroke-width="2.8" marker-end="url(#etl_ah)"/>

<!-- STAGE 2: VALIDATION, CONVERSION & PACKING -->
<rect x="50" y="295" width="1400" height="150" rx="12" fill="#eff7f2" stroke="#2a3846" stroke-width="2.2"/>
<rect x="50" y="295" width="1400" height="38" rx="12" fill="#c6e0cf" stroke="none"/>
<text x="750" y="322" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">STAGE 2: EXTRACTION, UNIT HARMONIZATION &amp; REVERSIBLE CODEC PACKING</text>

<rect x="75" y="345" width="410" height="85" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.6"/>
<text x="280" y="373" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Cryptographic Audit &amp; Provenance</text>
<text x="280" y="396" font-size="14" fill="#566473" text-anchor="middle">Computes SHA-256 digest of source files.</text>
<text x="280" y="416" font-size="14" fill="#566473" text-anchor="middle">Validates CC-BY-4.0 / Public Domain licenses.</text>

<rect x="545" y="345" width="410" height="85" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.6"/>
<text x="750" y="373" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Physical Unit Normalization to SI</text>
<text x="750" y="396" font-size="14" fill="#566473" text-anchor="middle">Strength: GPa/psi $\rightarrow$ MPa. Temp: K $\rightarrow$ °C.</text>
<text x="750" y="416" font-size="14" fill="#566473" text-anchor="middle">Thermal Cond: BTU/hr·ft·°F $\rightarrow$ W/m·K.</text>

<rect x="1015" y="345" width="410" height="85" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.6"/>
<text x="1220" y="373" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Reversible Binary Metadata Codec</text>
<text x="1220" y="396" font-size="14" fill="#566473" text-anchor="middle">Packs 3D crystal unit cells into compact strings.</text>
<text x="1220" y="416" font-size="14" fill="#566473" text-anchor="middle">Preserves custom descriptions &amp; raw citations.</text>

<line x1="750" y1="445" x2="750" y2="480" stroke="#2a3846" stroke-width="2.8" marker-end="url(#etl_ah)"/>

<!-- STAGE 3: CHUNKED BATCH STREAMING -->
<rect x="50" y="485" width="1400" height="230" rx="12" fill="#fcf3eb" stroke="#2a3846" stroke-width="2.2"/>
<rect x="50" y="485" width="1400" height="38" rx="12" fill="#fae3cf" stroke="none"/>
<text x="750" y="512" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">STAGE 3: BOUNDED CHUNK BUFFER &amp; ACID TRANSACTION BOUNDARY</text>

<rect x="75" y="535" width="310" height="160" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.6"/>
<text x="230" y="565" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Chunk Streaming Buffer</text>
<text x="95" y="595" font-size="14" fill="#1b2733">• Batches of 1,000–5,000 rows</text>
<text x="95" y="620" font-size="14" fill="#1b2733">• Memory footprint &lt; 250 MB</text>
<text x="95" y="645" font-size="14" fill="#1b2733">• Stream parser handles 100M+ lines</text>
<text x="95" y="670" font-size="14" fill="#1b2733">• Zero-skip guaranteed on restart</text>

<path fill="none" d="M 385,615 L 450,615" stroke="#2a3846" stroke-width="2.8" marker-end="url(#etl_ah)"/>

<!-- Atomic Transaction Block -->
<rect x="460" y="535" width="580" height="160" rx="8" fill="#ffffff" stroke="#ff8f00" stroke-width="2.0"/>
<text x="750" y="565" font-size="17" font-weight="700" fill="#b78103" text-anchor="middle">ACID Transaction Execution Block</text>
<text x="480" y="595" font-size="14" font-family="Courier New, monospace" fill="#1b2733">1. START TRANSACTION;</text>
<text x="480" y="620" font-size="14" font-family="Courier New, monospace" fill="#1b2733">2. INSERT INTO Material ... ON DUPLICATE KEY UPDATE;</text>
<text x="480" y="645" font-size="14" font-family="Courier New, monospace" fill="#1b2733">3. INSERT INTO Material_Property ... (Bulk payload);</text>
<text x="480" y="670" font-size="14" font-family="Courier New, monospace" fill="#1b2733">4. COMMIT;  /* Rollback on network/data error */</text>

<path fill="none" d="M 1040,615 L 1105,615" stroke="#2a3846" stroke-width="2.8" marker-end="url(#etl_ah)"/>

<rect x="1115" y="535" width="310" height="160" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.6"/>
<text x="1270" y="565" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Checkpoint Logging</text>
<text x="1135" y="595" font-size="14" fill="#1b2733">• Writes to Catalog_Import_Progress</text>
<text x="1135" y="620" font-size="14" fill="#1b2733">• Persists file byte offset &amp; row count</text>
<text x="1135" y="645" font-size="14" fill="#1b2733">• Verifies MD5 digest of snapshot</text>
<text x="1135" y="670" font-size="14" fill="#1b2733">• Guarantees idempotent replay</text>

<line x1="750" y1="715" x2="750" y2="750" stroke="#2a3846" stroke-width="2.8" marker-end="url(#etl_ah)"/>

<!-- STAGE 4: DATABASE PERSISTENCE -->
<rect x="50" y="755" width="1400" height="280" rx="12" fill="#f9f0f9" stroke="#2a3846" stroke-width="2.2"/>
<rect x="50" y="755" width="1400" height="38" rx="12" fill="#f2daf0" stroke="none"/>
<text x="750" y="782" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">STAGE 4: DUAL DATABASE STORAGE TARGETS &amp; INDEX CONSOLIDATION</text>

<rect x="120" y="810" width="560" height="200" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.0"/>
<text x="400" y="845" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Local Primary Storage: MySQL 8.4</text>
<text x="145" y="880" font-size="15" fill="#1b2733">• <tspan font-weight="700">6,265,691</tspan> materials &amp; 18 normalized schema tables</text>
<text x="145" y="910" font-size="15" fill="#1b2733">• Total disk footprint: <tspan font-weight="700">5.48 GiB</tspan> in InnoDB tablespace</text>
<text x="145" y="940" font-size="15" fill="#1b2733">• Consolidated composite indexes (removed single-key bloat)</text>
<text x="145" y="970" font-size="15" fill="#1b2733">• Buffer pool allocation: 1.0 GB RAM for fast cache hits</text>

<rect x="820" y="810" width="560" height="200" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.0"/>
<text x="1100" y="845" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Cloud Distributed Staging: TiDB Serverless</text>
<text x="845" y="880" font-size="15" fill="#1b2733">• <tspan font-weight="700">14 collections</tspan> transferred with certified TLS 1.3 encryption</text>
<text x="845" y="910" font-size="15" fill="#1b2733">• Fully verified schema footprint: <tspan font-weight="700">20 tables</tspan> (including audit tables)</text>
<text x="845" y="940" font-size="15" fill="#1b2733">• Distributed Raft-replicated storage regions across TiKV</text>
<text x="845" y="970" font-size="15" fill="#1b2733">• Idempotent stream reconciliation verified via transfer-tidb.js</text>

</svg>'''
    with open(svg_path, "w") as f:
        f.write(svg)
    print(f"Generated {svg_path}")

generate_fig4_1_etl_pipeline()

def generate_fig3_1_er_diagram():
    svg_path = SVG_DIR / "Fig3-1_ER_Diagram.svg"
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1850" viewBox="0 0 1600 1850" font-family="Carlito, Calibri, Arial, sans-serif" role="img" aria-label="Starbase complete entity-relationship diagram">
<title>Starbase Enhanced Entity-Relationship Diagram</title>
<desc>Conceptual and logical ER diagram showing core entities, associative tables with attributes (Material_Property, Project_Collaborator), and cardinality ratios.</desc>
<defs>
  <marker id="er_ah" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M1,1 L11,6 L1,11 Z" fill="#2a3846"/>
  </marker>
</defs>
<rect width="1600" height="1850" fill="#ffffff"/>

<!-- Title -->
<text x="800" y="45" font-size="28" font-weight="700" fill="#1b2733" text-anchor="middle">Starbase Entity–Relationship (ER) Diagram</text>
<text x="800" y="75" font-size="18" font-weight="400" fill="#566473" text-anchor="middle">Enhanced logical entity model with associative tables, payload attributes, and cardinality constraints</text>

<!-- Legend -->
<rect x="50" y="95" width="1500" height="42" rx="8" fill="#f8f9fa" stroke="#b0b8c1" stroke-width="1.5"/>
<text x="80" y="122" font-size="15" font-weight="700" fill="#1b2733">Notation Legend:</text>
<rect x="210" y="106" width="30" height="20" rx="4" fill="#c5d5ea" stroke="#2a3846" stroke-width="1.2"/>
<text x="250" y="122" font-size="14" fill="#1b2733">= Regular Entity</text>

<rect x="400" y="106" width="30" height="20" rx="4" fill="#fae3cf" stroke="#2a3846" stroke-width="1.2"/>
<text x="440" y="122" font-size="14" fill="#1b2733">= Associative Entity (M:N with Attributes)</text>

<rect x="740" y="106" width="30" height="20" rx="4" fill="#f2daf0" stroke="#2a3846" stroke-width="1.2"/>
<text x="780" y="122" font-size="14" fill="#1b2733">= Workspace / User Entity</text>

<text x="1100" y="122" font-size="14" font-weight="700" fill="#1b2733">Cardinalities: 1:N (One-to-Many), M:N (Many-to-Many)</text>

<!-- ROW 1: USERS & PROJECTS (TOP) -->
<!-- Users -->
<rect x="60" y="160" width="300" height="230" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="60" y="160" width="300" height="38" rx="10" fill="#f2daf0" stroke="none"/>
<text x="210" y="186" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Users</text>
<text x="78" y="218" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">user_id</tspan> (PK)</text>
<text x="78" y="244" font-size="14" fill="#1b2733">email (Unique)</text>
<text x="78" y="270" font-size="14" fill="#1b2733">password_hash</text>
<text x="78" y="296" font-size="14" fill="#1b2733">full_name</text>
<text x="78" y="322" font-size="14" fill="#1b2733">role ('user', 'admin')</text>
<text x="78" y="348" font-size="14" fill="#1b2733">created_at</text>
<text x="78" y="374" font-size="14" fill="#1b2733">last_login</text>

<!-- Project_Collaborator (Associative Entity) -->
<rect x="460" y="180" width="280" height="170" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="460" y="180" width="280" height="38" rx="10" fill="#fae3cf" stroke="none"/>
<text x="600" y="206" font-size="17" font-weight="700" fill="#1b2733" text-anchor="middle">Project_Collaborator</text>
<text x="478" y="238" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">project_id</tspan> (FK, PK)</text>
<text x="478" y="264" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">user_id</tspan> (FK, PK)</text>
<text x="478" y="290" font-size="14" font-weight="700" fill="#b78103">permission ('read','write','admin')</text>
<text x="478" y="316" font-size="14" fill="#1b2733">invited_at</text>

<!-- Projects -->
<rect x="840" y="160" width="300" height="220" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="840" y="160" width="300" height="38" rx="10" fill="#f2daf0" stroke="none"/>
<text x="990" y="186" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Projects</text>
<text x="858" y="218" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">project_id</tspan> (PK)</text>
<text x="858" y="244" font-size="14" fill="#1b2733">owner_id (FK -> Users)</text>
<text x="858" y="270" font-size="14" fill="#1b2733">name</text>
<text x="858" y="296" font-size="14" fill="#1b2733">description</text>
<text x="858" y="322" font-size="14" fill="#1b2733">status ('active','archived')</text>
<text x="858" y="348" font-size="14" fill="#1b2733">created_at, updated_at</text>

<!-- Saved_Selection -->
<rect x="1240" y="160" width="300" height="190" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="1240" y="160" width="300" height="38" rx="10" fill="#f2daf0" stroke="none"/>
<text x="1390" y="186" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Saved_Selection</text>
<text x="1258" y="218" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">selection_id</tspan> (PK)</text>
<text x="1258" y="244" font-size="14" fill="#1b2733">project_id (FK -> Projects)</text>
<text x="1258" y="270" font-size="14" fill="#1b2733">user_id (FK -> Users)</text>
<text x="1258" y="296" font-size="14" fill="#1b2733">title, notes</text>
<text x="1258" y="322" font-size="14" fill="#1b2733">created_at</text>

<!-- Relationship lines Row 1 -->
<line x1="360" y1="265" x2="460" y2="265" stroke="#2a3846" stroke-width="2.2"/>
<text x="380" y="255" font-size="14" font-weight="700">1</text>
<text x="435" y="255" font-size="14" font-weight="700">N</text>

<line x1="740" y1="265" x2="840" y2="265" stroke="#2a3846" stroke-width="2.2"/>
<text x="760" y="255" font-size="14" font-weight="700">N</text>
<text x="815" y="255" font-size="14" font-weight="700">1</text>

<line x1="1140" y1="255" x2="1240" y2="255" stroke="#2a3846" stroke-width="2.2"/>
<text x="1160" y="245" font-size="14" font-weight="700">1</text>
<text x="1215" y="245" font-size="14" font-weight="700">N</text>

<!-- Direct Owner line -->
<path fill="none" d="M 210,390 L 210,430 L 990,430 L 990,380" stroke="#2a3846" stroke-width="2.2" stroke-dasharray="6,4"/>
<text x="600" y="420" font-size="13" font-weight="700" fill="#566473" text-anchor="middle">Owns (1 : N)</text>

<!-- ROW 2: SEARCH HISTORY, SELECTION REQUIREMENTS & RECOMMENDATIONS -->
<!-- Search_History -->
<rect x="60" y="470" width="300" height="150" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.0"/>
<rect x="60" y="470" width="300" height="34" rx="10" fill="#f2daf0" stroke="none"/>
<text x="210" y="493" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Search_History</text>
<text x="78" y="522" font-size="13" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">search_id</tspan> (PK)</text>
<text x="78" y="546" font-size="13" fill="#1b2733">user_id (FK -> Users)</text>
<text x="78" y="570" font-size="13" fill="#1b2733">requirements (JSON)</text>
<text x="78" y="594" font-size="13" fill="#1b2733">result_count, created_at</text>

<line x1="210" y1="390" x2="210" y2="470" stroke="#2a3846" stroke-width="2.0"/>
<text x="220" y="445" font-size="13" font-weight="700">1:N</text>

<!-- Selection_Requirement -->
<rect x="1240" y="410" width="300" height="190" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.0"/>
<rect x="1240" y="410" width="300" height="34" rx="10" fill="#f2daf0" stroke="none"/>
<text x="1390" y="433" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Selection_Requirement</text>
<text x="1258" y="462" font-size="13" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">requirement_id</tspan> (PK)</text>
<text x="1258" y="486" font-size="13" fill="#1b2733">selection_id (FK -> Saved_Selection)</text>
<text x="1258" y="510" font-size="13" fill="#1b2733">property_id (FK -> Property)</text>
<text x="1258" y="534" font-size="13" fill="#1b2733">min_value, max_value</text>
<text x="1258" y="558" font-size="13" fill="#1b2733">target_value, weight</text>
<text x="1258" y="582" font-size="13" fill="#1b2733">is_mandatory (BOOL)</text>

<line x1="1390" y1="350" x2="1390" y2="410" stroke="#2a3846" stroke-width="2.0"/>
<text x="1400" y="385" font-size="13" font-weight="700">1:N</text>

<!-- Recommendation -->
<rect x="840" y="470" width="300" height="150" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.0"/>
<rect x="840" y="470" width="300" height="34" rx="10" fill="#f2daf0" stroke="none"/>
<text x="990" y="493" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Recommendation</text>
<text x="858" y="522" font-size="13" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">recommendation_id</tspan> (PK)</text>
<text x="858" y="546" font-size="13" fill="#1b2733">project_id (FK -> Projects)</text>
<text x="858" y="570" font-size="13" fill="#1b2733">material_id (FK -> Material)</text>
<text x="858" y="594" font-size="13" fill="#1b2733">score, explanation, created_at</text>

<line x1="990" y1="380" x2="990" y2="470" stroke="#2a3846" stroke-width="2.0"/>
<text x="1000" y="445" font-size="13" font-weight="700">1:N</text>

<!-- ROW 3: CATALOG CORE (CENTER) -->
<!-- Data_Source -->
<rect x="60" y="700" width="300" height="240" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="60" y="700" width="300" height="38" rx="10" fill="#c5d5ea" stroke="none"/>
<text x="210" y="726" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Data_Source (14 Sources)</text>
<text x="78" y="758" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">source_id</tspan> (PK)</text>
<text x="78" y="784" font-size="14" fill="#1b2733">source_key (Unique)</text>
<text x="78" y="810" font-size="14" fill="#1b2733">name, url, note</text>
<text x="78" y="836" font-size="14" fill="#1b2733">data_kind ('computed',...)</text>
<text x="78" y="862" font-size="14" fill="#1b2733">license (CC-BY, Public)</text>
<text x="78" y="888" font-size="14" fill="#1b2733">version, checksum</text>
<text x="78" y="914" font-size="14" fill="#1b2733">imported_at, summary_json</text>

<!-- Material_Category -->
<rect x="60" y="990" width="300" height="130" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="60" y="990" width="300" height="38" rx="10" fill="#c5d5ea" stroke="none"/>
<text x="210" y="1016" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Material_Category</text>
<text x="78" y="1048" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">category_id</tspan> (PK)</text>
<text x="78" y="1074" font-size="14" fill="#1b2733">name (Unique)</text>
<text x="78" y="1100" font-size="14" fill="#1b2733">description</text>

<!-- Material (Core Entity) -->
<rect x="520" y="700" width="380" height="310" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.8"/>
<rect x="520" y="700" width="380" height="42" rx="10" fill="#c6e0cf" stroke="none"/>
<text x="710" y="728" font-size="20" font-weight="700" fill="#1b2733" text-anchor="middle">Material (6,265,691 Records)</text>
<text x="540" y="762" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">material_id</tspan> (PK)</text>
<text x="540" y="788" font-size="14" fill="#1b2733">source_id (FK -> Data_Source)</text>
<text x="540" y="814" font-size="14" fill="#1b2733">category_id (FK -> Material_Category)</text>
<text x="540" y="840" font-size="14" fill="#1b2733">external_id (Unique per source)</text>
<text x="540" y="866" font-size="14" fill="#1b2733">name (Chemical formula / Trade name)</text>
<text x="540" y="892" font-size="14" fill="#1b2733">description</text>
<text x="540" y="918" font-size="14" fill="#1b2733">formula, crystal_system, space_group</text>
<text x="540" y="944" font-size="14" fill="#1b2733">is_active (TINYINT default 1)</text>
<text x="540" y="970" font-size="14" fill="#1b2733">metadata_json (Packed Binary Codec)</text>
<text x="540" y="996" font-size="14" fill="#1b2733">created_at, updated_at</text>

<!-- Connections to Material -->
<line x1="360" y1="820" x2="520" y2="820" stroke="#2a3846" stroke-width="2.2"/>
<text x="380" y="810" font-size="14" font-weight="700">1</text>
<text x="495" y="810" font-size="14" font-weight="700">N</text>

<path fill="none" d="M 360,1050 L 440,1050 L 440,880 L 520,880" stroke="#2a3846" stroke-width="2.2"/>
<text x="380" y="1040" font-size="14" font-weight="700">1</text>
<text x="495" y="870" font-size="14" font-weight="700">N</text>

<line x1="710" y1="700" x2="880" y2="620" stroke="#2a3846" stroke-width="2.0"/>
<text x="735" y="660" font-size="13" font-weight="700">1 : N</text>

<!-- Manufacturing_Process -->
<rect x="1240" y="690" width="300" height="130" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.0"/>
<rect x="1240" y="690" width="300" height="34" rx="10" fill="#c5d5ea" stroke="none"/>
<text x="1390" y="713" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Manufacturing_Process</text>
<text x="1258" y="742" font-size="13" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">process_id</tspan> (PK)</text>
<text x="1258" y="766" font-size="13" fill="#1b2733">name (Unique)</text>
<text x="1258" y="790" font-size="13" fill="#1b2733">description</text>

<!-- Application -->
<rect x="1240" y="880" width="300" height="140" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.0"/>
<rect x="1240" y="880" width="300" height="34" rx="10" fill="#c5d5ea" stroke="none"/>
<text x="1390" y="903" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Application</text>
<text x="1258" y="932" font-size="13" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">application_id</tspan> (PK)</text>
<text x="1258" y="956" font-size="13" fill="#1b2733">name (Unique)</text>
<text x="1258" y="980" font-size="13" fill="#1b2733">category, description</text>

<!-- Material_Process (Associative) -->
<rect x="960" y="690" width="220" height="120" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<rect x="960" y="690" width="220" height="30" rx="8" fill="#fae3cf" stroke="none"/>
<text x="1070" y="711" font-size="14" font-weight="700" fill="#1b2733" text-anchor="middle">Material_Process</text>
<text x="975" y="738" font-size="12" fill="#1b2733"><tspan text-decoration="underline">material_id</tspan> (FK, PK)</text>
<text x="975" y="760" font-size="12" fill="#1b2733"><tspan text-decoration="underline">process_id</tspan> (FK, PK)</text>
<text x="975" y="782" font-size="12" fill="#1b2733">notes</text>

<line x1="900" y1="750" x2="960" y2="750" stroke="#2a3846" stroke-width="2.0"/>
<line x1="1180" y1="750" x2="1240" y2="750" stroke="#2a3846" stroke-width="2.0"/>

<!-- Material_Application (Associative) -->
<rect x="960" y="880" width="220" height="130" rx="8" fill="#ffffff" stroke="#2a3846" stroke-width="1.8"/>
<rect x="960" y="880" width="220" height="30" rx="8" fill="#fae3cf" stroke="none"/>
<text x="1070" y="901" font-size="14" font-weight="700" fill="#1b2733" text-anchor="middle">Material_Application</text>
<text x="975" y="928" font-size="12" fill="#1b2733"><tspan text-decoration="underline">material_id</tspan> (FK, PK)</text>
<text x="975" y="950" font-size="12" fill="#1b2733"><tspan text-decoration="underline">application_id</tspan> (FK, PK)</text>
<text x="975" y="972" font-size="12" fill="#1b2733">suitability_score</text>
<text x="975" y="994" font-size="12" fill="#1b2733">notes</text>

<line x1="900" y1="940" x2="960" y2="940" stroke="#2a3846" stroke-width="2.0"/>
<line x1="1180" y1="940" x2="1240" y2="940" stroke="#2a3846" stroke-width="2.0"/>

<!-- ROW 4: PROPERTY & MATERIAL_PROPERTY (CORE DICTIONARY PAYLOAD) -->
<!-- Material_Property (The central associative entity with measurement attributes!) -->
<rect x="520" y="1120" width="380" height="260" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.8"/>
<rect x="520" y="1120" width="380" height="42" rx="10" fill="#fae3cf" stroke="none"/>
<text x="710" y="1148" font-size="19" font-weight="700" fill="#1b2733" text-anchor="middle">Material_Property (Associative Payload)</text>
<text x="540" y="1182" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">material_id</tspan> (FK, PK -> Material)</text>
<text x="540" y="1208" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">property_id</tspan> (FK, PK -> Property)</text>
<text x="540" y="1234" font-size="15" font-weight="700" fill="#2e7d32">numeric_value: DOUBLE (Composite Indexed)</text>
<text x="540" y="1260" font-size="14" fill="#1b2733">text_value: VARCHAR(100)</text>
<text x="540" y="1286" font-size="14" fill="#1b2733">uncertainty: DOUBLE</text>
<text x="540" y="1312" font-size="14" fill="#1b2733">test_conditions: VARCHAR(255) ('293 K, 1 atm')</text>
<text x="540" y="1338" font-size="14" fill="#1b2733">is_estimated: TINYINT(1) DEFAULT 0</text>
<text x="540" y="1364" font-size="14" fill="#566473">Enforces non-imputation: Missing != 0</text>

<line x1="710" y1="1010" x2="710" y2="1120" stroke="#2a3846" stroke-width="2.5"/>
<text x="720" y="1035" font-size="14" font-weight="700">1</text>
<text x="720" y="1105" font-size="14" font-weight="700">N</text>

<!-- Property Entity -->
<rect x="520" y="1480" width="380" height="230" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.2"/>
<rect x="520" y="1480" width="380" height="38" rx="10" fill="#c5d5ea" stroke="none"/>
<text x="710" y="1506" font-size="18" font-weight="700" fill="#1b2733" text-anchor="middle">Property (Dictionary Entity)</text>
<text x="540" y="1538" font-size="14" fill="#1b2733"><tspan text-decoration="underline" font-weight="700">property_id</tspan> (PK)</text>
<text x="540" y="1564" font-size="14" fill="#1b2733">property_key: VARCHAR(80) UNIQUE</text>
<text x="540" y="1590" font-size="14" fill="#1b2733">name: VARCHAR(100)</text>
<text x="540" y="1616" font-size="14" fill="#1b2733">unit: VARCHAR(80) (Standardized SI)</text>
<text x="540" y="1642" font-size="14" fill="#1b2733">data_type: ENUM('numeric','text','boolean')</text>
<text x="540" y="1668" font-size="14" fill="#1b2733">category: ('Mechanical','Thermal','Space')</text>
<text x="540" y="1694" font-size="14" fill="#1b2733">is_active: TINYINT(1) DEFAULT 1</text>

<line x1="710" y1="1380" x2="710" y2="1480" stroke="#2a3846" stroke-width="2.5"/>
<text x="720" y="1405" font-size="14" font-weight="700">N</text>
<text x="720" y="1465" font-size="14" font-weight="700">1</text>

<!-- Application_Property (Associative) -->
<rect x="1060" y="1480" width="320" height="150" rx="10" fill="#ffffff" stroke="#2a3846" stroke-width="2.0"/>
<rect x="1060" y="1480" width="320" height="34" rx="10" fill="#fae3cf" stroke="none"/>
<text x="1220" y="1503" font-size="16" font-weight="700" fill="#1b2733" text-anchor="middle">Application_Property</text>
<text x="1078" y="1532" font-size="13" fill="#1b2733"><tspan text-decoration="underline">application_id</tspan> (FK, PK)</text>
<text x="1078" y="1556" font-size="13" fill="#1b2733"><tspan text-decoration="underline">property_id</tspan> (FK, PK)</text>
<text x="1078" y="1580" font-size="13" fill="#1b2733">weight: DOUBLE DEFAULT 1.0</text>
<text x="1078" y="1604" font-size="13" fill="#1b2733">notes</text>

<line x1="900" y1="1550" x2="1060" y2="1550" stroke="#2a3846" stroke-width="2.0"/>
<text x="920" y="1540" font-size="13" font-weight="700">1</text>
<text x="1035" y="1540" font-size="13" font-weight="700">N</text>

<path fill="none" d="M 1390,1020 L 1390,1440 L 1220,1440 L 1220,1480" stroke="#2a3846" stroke-width="2.0"/>
<text x="1400" y="1050" font-size="13" font-weight="700">1</text>
<text x="1230" y="1465" font-size="13" font-weight="700">N</text>

<!-- ROW 5: NOTES & INTEGRITY CHECKS (BOTTOM) -->
<rect x="50" y="1740" width="1500" height="85" rx="8" fill="#f8f9fa" stroke="#b0b8c1" stroke-width="1.5"/>
<text x="70" y="1770" font-size="15" font-weight="700" fill="#37474f">Relational Integrity &amp; Normalization Rules:</text>
<text x="70" y="1795" font-size="14" fill="#455a64">• All many-to-many relationships (Material-Property, Material-Application, User-Project) are formally resolved via associative entities with payload attributes.</text>
<text x="70" y="1815" font-size="14" fill="#455a64">• Enforces 3NF: No repeating groups (1NF), no partial key dependencies (2NF), and zero transitive non-prime dependencies (3NF).</text>

</svg>'''
    with open(svg_path, "w") as f:
        f.write(svg)
    print(f"Generated enhanced {svg_path}")

generate_fig3_1_er_diagram()
