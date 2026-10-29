from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from generate_academic_report import (
    DIAGRAMS_DIR, add_p, add_h1, add_h2, add_h3, add_bullet,
    add_figure, add_table_title, style_table
)

def add_chapter_1(doc):
    add_h1(doc, "1 INTRODUCTION")

    add_h2(doc, "1.1 Introduction")
    add_p(doc, "Every engineered physical artifact—from microelectronic lead frames and battery casings to aerospace thermal protection tiles and high-pressure cryogenic valves—is fundamentally constrained by the physical properties of its constituent materials. An engineer designing a component must systematically reconcile competing requirements, balancing structural yield strength, elastic stiffness, thermal conductivity, service temperature limits, environmental corrosion resistance, raw material costs, and manufacturing feasibility. In modern design methodology, selecting the optimal material is not an afterthought but the primary determinant of mass efficiency, structural integrity, and lifecycle economy [13].")

    add_p(doc, "Despite decades of scientific research yielding vast quantities of material data, utilizing this information in everyday engineering practice remains remarkably challenging. Computational crystal simulations, standardized tensile testing data, cryogenic outgassing metrics, and manufacturer alloy certifications are distributed across disparate silos [1–7, 9–12]. These sources employ conflicting nomenclature, proprietary schemas, incompatible physical units, and varying levels of experimental fidelity. Consequently, engineers are frequently forced to navigate between printed reference handbooks, individual PDF supplier datasheets, and specialized computational research portals [13].")

    add_p(doc, "From a database management systems perspective, material selection is an archetype of multi-criteria decision analysis over heterogeneous, sparse-matrix scientific data [14, 15]. Resolving this challenge requires a robust relational architecture capable of standardizing disparate entities, preserving complete cryptographic and legal provenance, and executing bounded multi-parameter screening queries at interactive speeds. This project, titled Starbase, was developed as part of the Database Management System (PBEOT504) Project-Based Learning curriculum for the B.Tech Electrical and Computer Engineering programme at College of Engineering Trivandrum.")

    add_h2(doc, "1.2 Problem Statement")
    add_p(doc, "Engineering organizations face four structural bottlenecks when attempting to screen and select materials across modern public and proprietary datasets:")
    add_bullet(doc, "Syntactic and Schema Heterogeneity: ", "Open materials repositories publish data in non-interoperable formats. Computational repositories such as Materials Project [1] and AFLOW [3] utilize JSON REST APIs and crystallographic CIF files; Alexandria [7] provides dense BZip2-compressed tar archives; NASA TPSX [9] uses XML and PDF technical reports; and alloy manufacturers [12] distribute unstructured tabular PDF datasheets.")
    add_bullet(doc, "Semantic Divergence and Sparse Attributes: ", "Mechanical properties (yield strength, elongation, fracture toughness) are reported predominantly for commercial alloys, whereas electronic and quantum-mechanical properties (band gaps, bulk modulus, formation energy) are reported for computational density functional theory (DFT) structures. Attempting to fit these diverse records into a single rigid relational table results in extreme column sparsity (over 95% NULL values) or data distortion.")
    add_bullet(doc, "Lack of Verifiable Provenance: ", "Many aggregated commercial tools strip raw citations and licensing conditions. Engineers cannot verify whether a quoted yield strength represents a minimum design guarantee, an average laboratory test at 20°C, or an unvalidated computational approximation.")
    add_bullet(doc, "Multi-Attribute Decision Complexity: ", "Designers require a mechanism that enforces non-negotiable hard constraints (e.g., minimum yield strength > 400 MPa and service temperature > 300°C) while simultaneously performing multi-objective optimization across normalized secondary priorities (e.g., maximizing strength-to-weight ratio while minimizing cost).")

    add_h2(doc, "1.3 Objectives")
    add_p(doc, "The primary objectives of the Starbase system are:")
    add_bullet(doc, "Relational Schema Normalization: ", "Design and implement a Third Normal Form (3NF) relational database schema capable of accommodating millions of material records with arbitrary, extensible physical properties without schema mutations or column bloat.")
    add_bullet(doc, "Scalable Ingestion of Authoritative Repositories: ", "Develop robust, transaction-safe ETL pipelines to ingest, normalize, and reconcile over 6 million records from 14 open and authorized materials repositories [1–7, 9–12].")
    add_bullet(doc, "Interactive Multi-Criteria Screening Engine: ", "Implement a hybrid evaluation engine that executes SQL-level hard constraint pruning followed by min-max normalized weighted priority scoring.")
    add_bullet(doc, "Comprehensive Provenance Tracking: ", "Record upstream repository keys, dataset licenses, source URLs, raw metadata JSON, and digital checksums for 100% of ingested materials.")
    add_bullet(doc, "Collaborative Engineering Workspaces: ", "Provide multi-tenant project management capabilities with role-based access control (RBAC), requirement versioning, candidate shortlisting, and side-by-side comparison.")
    add_bullet(doc, "Enterprise Cloud & Local Compatibility: ", "Ensure seamless execution across local developer environments running MySQL 8.4 [16] and distributed cloud infrastructure running TiDB Serverless [17].")

    add_h2(doc, "1.4 Scope of the Project")
    add_p(doc, "The scope of Starbase encompasses relational schema modeling, automated bulk ingestion pipelines, backend RESTful web services, and an interactive React-based user interface. The system accommodates computational DFT crystals, empirical alloy test results, polymer specifications, ceramic properties, and spacecraft-certified outgassing measurements.")
    add_p(doc, "Clarification on Property Availability versus Catalog Coverage: ", bold=True)
    add_p(doc, "A critical engineering distinction maintained throughout Starbase is that while 100% of the 6,265,691 ingested materials possess verified source provenance, licenses, and categorization, physical property availability varies significantly across scientific domains. For example, 599 materials report empirical tensile strength in literature datasets, 81 commercial stainless-steel grades report temperature-dependent thermal conductivity, and millions of computational structures report calculated bulk modulus and formation energy. Starbase strictly avoids artificial zero-imputation: if a candidate material lacks a property demanded by an engineer's hard constraint, it is disqualified with explicit diagnostic feedback rather than evaluated with fabricated numerical approximations.")

def add_chapter_2(doc):
    add_h1(doc, "2 SYSTEM ANALYSIS AND DESIGN")

    add_h2(doc, "2.1 Existing System and Its Limitations")
    add_p(doc, "Engineering materials selection currently relies on three principal categories of tools, each exhibiting distinct operational limitations:")
    add_bullet(doc, "Printed Handbooks and Personal Spreadsheets: ", "Handbooks such as ASM International reference manuals provide trustworthy experimental data but are static, cannot be queried programmatically, and do not scale to comparative multi-objective trade-offs. Ad-hoc engineering spreadsheets lack schema integrity, validation constraints, and multi-user collaboration controls.")
    add_bullet(doc, "Proprietary Commercial Databases: ", "Enterprise solutions such as Ansys Granta Selector, Total Materia, and MatWeb provide extensive certified engineering properties. However, they are closed-source, require prohibitively expensive site licenses, and frequently treat their underlying scoring algorithms as black boxes.")
    add_bullet(doc, "Specialized Research Web Repositories: ", "Open scientific portals (Materials Project [1], NIST JARVIS [2], AFLOW [3], NOMAD [4]) offer excellent deep APIs for solid-state physics and computational materials science. However, they are isolated from commercial manufacturing catalogs and lack integrated multi-attribute engineering selection studios.")

    add_h2(doc, "2.2 Proposed System")
    add_p(doc, "Starbase resolves these deficiencies by introducing an open, scalable, relational materials database and selection platform. The proposed system features:")
    add_bullet(doc, "A Property Dictionary Architecture: ", "Decoupling property definitions from material entities via a normalized entity-attribute-value model, enabling thousands of physical attributes to be indexed without altering table DDL.")
    add_bullet(doc, "Dual-Engine Evaluation: ", "Offloading hard boundary screening (minimum yield strength, maximum density, service temperature thresholds) to indexed SQL queries, followed by in-memory normalized ranking across user-weighted priorities.")
    add_bullet(doc, "Explainable Recommendation Logic: ", "Every candidate evaluation produces detailed inclusion justifications, normalized sub-scores, and explicit disqualification audit logs.")
    add_bullet(doc, "Collaborative Workspaces: ", "Project teams can persist selection requirements, save shortlisted candidates, and collaborate under Owner, Editor, or Viewer access permissions.")

    add_h2(doc, "2.3 System Requirements")
    add_p(doc, "The functional and non-functional requirements governing the Starbase architecture are summarized in Table 2.1.")

    add_table_title(doc, "Table 2.1 — System Requirements Specifications.")
    tbl_req = doc.add_table(rows=9, cols=3)
    req_data = [
        ("ID", "Requirement Category", "Description and Acceptance Criteria"),
        ("FR-1", "Catalog Browsing", "Search, filter, and paginate 6.26M+ materials by keyword, collection, category, and source repository with sub-50ms latency."),
        ("FR-2", "Multi-Criteria Screening", "Execute SQL-filtered property screening based on numerical thresholds, category masks, and environment limits."),
        ("FR-3", "Weighted Priority Scoring", "Compute normalized composite scores based on user-allocated weights across strength, lightness, stiffness, thermal, and cost."),
        ("FR-4", "Provenance Auditing", "Display upstream repository URL, license classification, checksum, and experimental versus computational evidence kind."),
        ("FR-5", "Material Comparison", "Render tabular side-by-side property comparisons with delta highlighting for up to 4 shortlisted materials."),
        ("FR-6", "Project Workspace", "Create named engineering projects, save requirement parameters, shortlist candidates, and share access via RBAC."),
        ("NFR-1", "Scalability & Performance", "Execute indexed candidate queries across 6.26M+ records in under 20ms on dedicated MySQL 8.4 and TiDB Cloud."),
        ("NFR-2", "Data Integrity", "Enforce relational foreign keys, unique constraint indexes, atomic batch ETL transactions, and non-imputation of missing properties.")
    ]
    for i, r in enumerate(req_data):
        for j, val in enumerate(r):
            tbl_req.cell(i, j).text = val
    style_table(tbl_req, [1.0, 1.8, 3.22])

    add_h2(doc, "2.4 System Architecture")
    add_p(doc, "Starbase is architected as a decoupled, multi-tier system comprising a presentation tier, an application tier, a relational data tier, and an offline bulk ingestion pipeline. Figure 2.1 illustrates the structural relationship between these architectural layers.")

    fig_arch = DIAGRAMS_DIR / "Fig2-1_System_Architecture.png"
    if fig_arch.exists():
        add_figure(doc, fig_arch, "Figure 2.1 — Starbase three-tier system architecture and offline ingestion pipeline.", width_in=6.0)

    add_p(doc, "The architectural tiers fulfill the following responsibilities:")
    add_bullet(doc, "Presentation Tier: ", "Implemented in React 18 with modern component-driven styling. Communicates with backend services over asynchronous RESTful HTTP calls, managing local client-side state for real-time slider adjustments and comparative views.")
    add_bullet(doc, "Application Tier: ", "Built with Node.js and Express 5, providing RESTful API controllers, JWT authentication, query parameter sanitization, and the multi-criteria ranking engine.")
    add_bullet(doc, "Data Tier: ", "A high-performance relational database engine (MySQL 8.4 locally and TiDB Serverless in the cloud) managing core entity tables, property dictionaries, composite indexes, and project collaboration schemas.")
    add_bullet(doc, "Offline Ingestion Pipeline: ", "Python and Node.js extraction scripts that pull open datasets, unpack crystal lattices, compute cryptographic SHA-256 hashes, normalize units, and execute atomic batch SQL insertions.")

    add_h2(doc, "2.5 System Workflow")
    add_p(doc, "The end-to-end engineering selection workflow follows five discrete operational stages:")
    add_bullet(doc, "1. Requirement Specification: ", "The engineer establishes non-negotiable physical constraints (e.g., Yield Strength ≥ 450 MPa, Max Density ≤ 4.5 g/cm³) and specifies relative priority weights for optimization goals.")
    add_bullet(doc, "2. Indexed SQL Candidate Screening: ", "The backend maps specified criteria to database property keys, executing parameterized queries against composite indexes to filter eligible candidates.")
    add_bullet(doc, "3. Min-Max Normalization: ", "For surviving candidates, each property value is normalized against global catalog extremes to generate dimensionless metrics between 0.0 and 1.0.")
    add_bullet(doc, "4. Composite Scoring & Ranking: ", "Normalized metrics are multiplied by user priority weights to produce an overall suitability score. Disqualified materials are categorized with explicit exclusion reasons.")
    add_bullet(doc, "5. Workspace Collaboration: ", "The resulting shortlist is persisted to the engineer's project workspace, enabling team-wide reviews, note additions, and side-by-side comparative trade-off studies.")

    add_h2(doc, "2.6 Dataflow Diagrams")
    add_p(doc, "The data interactions within Starbase are formalized through Level 0 and Level 1 Data Flow Diagrams (DFDs). Table 2.2 defines the functional processes and data store interactions.")

    add_table_title(doc, "Table 2.2 — DFD Process Specifications and Data Store Interactions.")
    tbl_dfd = doc.add_table(rows=7, cols=4)
    dfd_data = [
        ("Process ID", "Process Name", "Input Data Streams", "Data Stores & Outputs"),
        ("P1", "User Authentication", "Credentials, registration data", "D1 (Users) -> JWT Auth Token"),
        ("P2", "Catalog Exploration", "Search query, filters, pagination", "D2 (Catalog) -> Material Summaries"),
        ("P3", "Multi-Criteria Screening", "Hard physical limits, property keys", "D2 (Catalog), D3 (Properties) -> Candidate Set"),
        ("P4", "Scoring & Ranking", "Priority weights, component volume", "Candidate Set -> Ranked Shortlist & Audit"),
        ("P5", "Project Management", "Requirements, shortlists, collaborators", "D4 (Projects) -> Persisted Workspace"),
        ("P6", "Catalog Data Ingestion", "Raw source files (JSON, CSV, CIF)", "D2 (Catalog), D3 (Properties) -> Database Rows")
    ]
    for i, r in enumerate(dfd_data):
        for j, val in enumerate(r):
            tbl_dfd.cell(i, j).text = val
    style_table(tbl_dfd, [0.9, 1.8, 1.8, 1.52])

    fig_dfd0 = DIAGRAMS_DIR / "Fig2-2_DFD_Level0.png"
    if fig_dfd0.exists():
        add_figure(doc, fig_dfd0, "Figure 2.2 — Level 0 Data Flow Diagram (Context Analysis).", width_in=5.8)

    fig_dfd1 = DIAGRAMS_DIR / "Fig2-3_DFD_Level1.png"
    if fig_dfd1.exists():
        add_figure(doc, fig_dfd1, "Figure 2.3 — Level 1 Data Flow Diagram (Decomposed Functional Modules).", width_in=5.5)
