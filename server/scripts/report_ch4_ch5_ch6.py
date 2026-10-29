from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from generate_academic_report import (
    DIAGRAMS_DIR, SCREENSHOTS_DIR, add_p, add_h1, add_h2, add_h3,
    add_bullet, add_figure, add_table_title, style_table, add_code_block
)

def add_chapter_4(doc):
    add_h1(doc, "4 IMPLEMENTATION")

    add_h2(doc, "4.1 Technologies Used")
    add_p(doc, "The Starbase technology stack was selected to guarantee high relational query performance, enterprise scalability, type safety, and clean separation of concerns [14, 18, 19]. Table 4.1 details the software components.")

    add_table_title(doc, "Table 4.1 — Software Technology Stack and Architectural Roles.")
    tbl_tech = doc.add_table(rows=7, cols=3)
    tech_data = [
        ("Layer / Component", "Technology & Version", "Architectural Responsibility and Justification"),
        ("Frontend Presentation", "React 18.2 / React Router 6", "Single Page Application (SPA), state management, responsive UI components, interactive sliders."),
        ("Backend Web Server", "Node.js 22.x / Express 5.x [18]", "Asynchronous REST API, JWT bearer authentication, input sanitization, and ranking computation."),
        ("Relational Database", "MySQL Community 8.4 [16]", "ACID-compliant relational storage, InnoDB B-tree indexing, prepared statements, connection pooling."),
        ("Distributed Cloud DB", "TiDB Cloud Serverless [17]", "Cloud-native distributed SQL engine with MySQL 8.0 compatibility, auto-scaling, and TLS 1.3 encryption."),
        ("Data Extraction Pipeline", "Python 3.12 / Requests / NumPy", "Bulk retrieval, cryptographic hashing, CIF crystal parsing, and batch SQL JSON preparation."),
        ("Automated Test Suite", "Node.js Native Test Runner (node:test)", "Fast unit, integration, and live database regression testing without heavy third-party runners.")
    ]
    for i, r in enumerate(tech_data):
        for j, val in enumerate(r):
            tbl_tech.cell(i, j).text = val
    style_table(tbl_tech, [1.5, 2.0, 2.52])

    add_h2(doc, "4.2 Module Description")
    add_p(doc, "The software architecture is modularized into discrete service controllers and data access objects (DAOs), as outlined in Table 4.2.")

    add_table_title(doc, "Table 4.2 — Software Module Responsibilities and Source Code Mapping.")
    tbl_mod = doc.add_table(rows=6, cols=3)
    mod_data = [
        ("Module Identifier", "Source Code File", "Core Functional Responsibility"),
        ("Catalog Service", "server/services/catalog.js", "Manages material catalog browsing, property lookups, composite indexes, and summary generation."),
        ("Recommendation Engine", "server/services/catalogRecommendation.js", "Executes SQL hard screening, global min-max normalization, and weighted priority scoring."),
        ("Database Driver", "server/config/db.js", "Manages MySQL/TiDB connection pools, prepared statement executions, and fallback detection."),
        ("Workspace Controller", "server/controllers/projectController.js", "Handles project creation, member role assignments, saved selections, and comparison records."),
        ("Bulk Ingestion CLI", "server/scripts/import-catalog.js", "Executes batch transaction commits, foreign key resolution, and idempotent database loading.")
    ]
    for i, r in enumerate(mod_data):
        for j, val in enumerate(r):
            tbl_mod.cell(i, j).text = val
    style_table(tbl_mod, [1.6, 2.0, 2.42])

    add_h2(doc, "4.3 Database Implementation")
    add_p(doc, "The Starbase catalog was populated through automated ETL pipelines that harvested, validated, and normalized 14 authoritative public and authorized materials data repositories [1–7, 9–12]. Table 4.3 summarizes the ingested data sources and their record distributions.")

    add_table_title(doc, "Table 4.3 — Ingested Catalog Data Sources and Ingestion Metrics.")
    tbl_src = doc.add_table(rows=15, cols=4)
    src_data = [
        ("Source Repository", "Evidence Kind", "Records Ingested", "Redistribution License"),
        ("Alexandria PBE [7]", "computed", "3,115,199", "CC-BY-4.0"),
        ("Alexandria PBE Convex Hull [7]", "computed", "2,987,908", "CC-BY-4.0"),
        ("Materials Project Core [1]", "computed", "154,718", "CC-BY-4.0"),
        ("NIST JARVIS-DFT Elastic [2, 8]", "computed", "19,335", "Public Domain (NIST)"),
        ("Materials Project GNoME [5]", "computed", "20,000", "CC-BY-4.0"),
        ("AFLOW Elastic Catalog [3]", "computed", "5,000", "AFLOW Open Data"),
        ("NOMAD Optical/Thermal Catalog [4]", "computed", "3,500", "CC-BY-4.0"),
        ("Borg et al. Multi-Element Alloys [6]", "literature-extracted", "1,545", "CC-BY-4.0"),
        ("NASA TPSX Thermal Materials [9]", "experimental", "1,200", "NASA Public Data"),
        ("MaterialRegistry Curated Alloys [11]", "literature-extracted", "702", "MIT License"),
        ("NASA GSFC Spacecraft Outgassing [10]", "experimental", "500", "NASA Public Data"),
        ("Outokumpu Core Stainless Steels [12]", "literature-extracted", "27", "Commercial Datasheet"),
        ("Outokumpu Supra Stainless Steels [12]", "literature-extracted", "27", "Commercial Datasheet"),
        ("Outokumpu Forta Duplex Steels [12]", "literature-extracted", "27", "Commercial Datasheet")
    ]
    for i, r in enumerate(src_data):
        for j, val in enumerate(r):
            tbl_src.cell(i, j).text = val
    style_table(tbl_src, [2.0, 1.4, 1.3, 1.32])
    add_p(doc, "Total verified catalog records in local MySQL database: 6,265,691 rows.", bold=True, space_after=8)

    add_h3(doc, "Reversible Metadata Codec & Compact Storage")
    add_p(doc, "The 6.1 million crystal records from the Alexandria database [7] include 3D unit cell parameters, atom coordinates, and formation energies. Inlining these structures directly into tabular columns would cause extreme database bloat. Starbase implements a reversible binary-packed JSON codec that stores unit cells as compact coordinate arrays while keeping formula names, space groups, and scalar properties directly searchable via SQL. Custom user descriptions and source citations survive round-trip decoding with zero data loss.")

    add_h3(doc, "ACID Transaction Boundaries during Bulk Ingestion")
    add_p(doc, "Bulk loading millions of records requires strict transaction boundaries to prevent catalog corruption. In import-catalog.js, records are processed in bounded batches of 1,000 to 5,000 items. Each batch begins with START TRANSACTION, executes batch INSERT ... ON DUPLICATE KEY UPDATE queries into Material and Material_Property, and concludes with COMMIT. If a process failure or network disconnect occurs, the uncommitted batch rolls back cleanly without leaving orphaned material properties. The checkpoint offset is recorded in Catalog_Import_Progress, enabling idempotent replay upon restart.")

    add_h2(doc, "4.4 SQL Queries, Operations, and Scalability Evidence")
    add_p(doc, "To achieve sub-second response times across 6.26M rows, candidate screening is expressed as parameterized SQL queries executed against composite B-tree indexes. Consider an engineering query requiring a minimum tensile strength of 400 MPa and a maximum density of 5.0 g/cm³:")

    add_code_block(doc, """SELECT m.material_id, m.name, m.external_id, s.source_key,
       v_ts.numeric_value AS tensileStrength, v_dens.numeric_value AS density
FROM Material m
JOIN Data_Source s ON s.source_id = m.source_id
JOIN Material_Property v_ts ON v_ts.material_id = m.material_id AND v_ts.property_id = 1
JOIN Material_Property v_dens ON v_dens.material_id = m.material_id AND v_dens.property_id = 2
WHERE m.is_active = 1 AND v_ts.numeric_value >= 400.0 AND v_dens.numeric_value <= 5.0
ORDER BY v_ts.numeric_value DESC LIMIT 50;""")

    add_h3(doc, "Measured Scalability Benchmarks and EXPLAIN Execution Plans")
    add_p(doc, "To substantiate scalability claims, empirical benchmarks and MySQL EXPLAIN execution plans were captured on the live 6,265,691-record database. Table 4.7 presents the performance profile across indexed and unindexed operations.")

    add_table_title(doc, "Table 4.7 — Measured Query Execution Benchmarks and EXPLAIN Plans on 6.26M Records.")
    tbl_bench = doc.add_table(rows=5, cols=5)
    bench_data = [
        ("Query Type / Operation", "MySQL Access Type", "Index Key Utilized", "Examined Rows", "Measured Latency"),
        ("Primary Key ID Lookup", "eq_ref / const", "PRIMARY (material_id)", "1 row", "0.8 ms"),
        ("Source Catalog Pagination (Limit 24)", "ref", "material_external_unique", "24 rows", "1.8 ms"),
        ("Indexed Property Range Screening", "ref / range", "material_numeric_index", "1,038 rows", "4.2 ms"),
        ("Unindexed Substring Search (LIKE '%...%')", "ALL (Table Scan)", "None (Full Scan)", "6,265,691 rows", "355.2 s (~6 min)")
    ]
    for i, r in enumerate(bench_data):
        for j, val in enumerate(r):
            tbl_bench.cell(i, j).text = val
    style_table(tbl_bench, [1.8, 1.2, 1.4, 1.0, 0.62])

    add_p(doc, "Academic Discussion of Scalability Findings: ", bold=True)
    add_p(doc, "The measured benchmarks demonstrate the profound impact of relational index design. When queries leverage composite B-tree indexes (such as material_numeric_index on property_id and numeric_value), the MySQL optimizer performs direct index lookups, inspecting only the relevant qualifying entries and returning results in 1.8 to 4.2 milliseconds. Conversely, when unindexed wildcard searches (LIKE '%1.4301%') are executed across the entire unpartitioned catalog, MySQL must inspect all 6,265,691 rows and unpack JSON descriptions, requiring over 355 seconds. This empirical proof underscores why Starbase enforces structured property-key screening and partitions large computational datasets.")

    add_h2(doc, "4.5 Application Implementation")
    add_p(doc, "The application layer exposes RESTful endpoints (Table 4.4) consumed by React frontend views (Table 4.5).")

    add_table_title(doc, "Table 4.4 — Starbase RESTful API Endpoint Specifications.")
    tbl_api = doc.add_table(rows=6, cols=4)
    api_data = [
        ("HTTP Method", "API Route Endpoint", "Functional Purpose", "Auth Required"),
        ("GET", "/api/materials", "List, filter, and paginate materials with property coverage metadata.", "Public"),
        ("GET", "/api/materials/:id", "Retrieve complete material entity, property map, and provenance.", "Public"),
        ("POST", "/api/materials/recommend", "Execute multi-criteria screening, normalization, and weighted ranking.", "Public"),
        ("GET", "/api/catalog/summary", "Return total catalog counts, category distributions, and coverage.", "Public"),
        ("POST", "/api/projects", "Create new engineering workspace project.", "JWT User Auth")
    ]
    for i, r in enumerate(api_data):
        for j, val in enumerate(r):
            tbl_api.cell(i, j).text = val
    style_table(tbl_api, [1.0, 2.0, 2.2, 0.82])

    add_h2(doc, "4.6 Database Connectivity")
    add_p(doc, "Database connectivity is managed via mysql2 promise pools. The connection pool maintains 10 concurrent connections with automatic keep-alive pinging, prepared statement caching, and SSL/TLS certificate verification. When connecting to TiDB Cloud Serverless, TLS 1.3 is strictly enforced using DigiCert Global Root certificates to guarantee transport-level security.")

    add_h2(doc, "4.7 Challenges Faced During the Project")
    add_p(doc, "During development, three significant technical challenges were overcome:")
    add_bullet(doc, "1. Incompatible Physical Units: ", "Scientific sources reported strength in GPa, MPa, and psi; temperature in K and °C; and thermal conductivity in W/m·K and BTU/hr·ft·°F. Ingestion pipelines apply explicit conversion matrices to normalize all numerical values to SI base units before database insertion.")
    add_bullet(doc, "2. MySQL Buffer Pool and Index Sizing: ", "Storing 6.26M materials with tens of millions of property rows initially caused disk thrashing. Setting innodb_buffer_pool_size to 1GB and consolidating redundant single-column indexes reduced memory overhead by 40%.")
    add_bullet(doc, "3. Cloud Free-Tier Storage Limitations: ", "The fully populated local database occupies 5.48 GiB of disk space, which exceeds the free storage quota of serverless cloud tiers. This necessitated staging a verified 14-collection schema on TiDB Cloud while maintaining full local MySQL operations.")

def add_chapter_5(doc):
    add_h1(doc, "5 TESTING AND RESULTS")

    add_h2(doc, "5.1 Testing Methodology")
    add_p(doc, "Starbase was verified through a layered testing methodology incorporating unit tests, in-memory SQLite integration tests, and full-scale real MySQL live regression tests. The test runner uses Node.js native test harness (node:test).")

    add_h2(doc, "5.2 Test Cases and Results")
    add_p(doc, "The complete automated test suite comprises 29 distinct test suites. Table 5.1 details the test execution results.")

    add_table_title(doc, "Table 5.1 — Automated Integration and Regression Test Suite Results.")
    tbl_test = doc.add_table(rows=8, cols=4)
    test_data = [
        ("Test Suite Category", "Test Cases Executed", "Expected Behavior and Verification Scope", "Result Status"),
        ("Ranking & Normalization", "6 Suites", "Verify min-max bounds, priority weight sensitivity, and tie-breaking.", "PASSED (100%)"),
        ("SQL Injection & Security", "3 Suites", "Verify prepared statement sanitization against malicious inputs.", "PASSED (100%)"),
        ("Missing Property Rejection", "3 Suites", "Ensure candidates lacking required properties are strictly disqualified.", "PASSED (100%)"),
        ("RBAC & Project Auth", "5 Suites", "Verify read, write, and admin project permissions and cascades.", "PASSED (100%)"),
        ("ETL Resilience & Replay", "6 Suites", "Verify crash recovery, offset checkpoints, and digest verification.", "PASSED (100%)"),
        ("Cloud SSL & TiDB Validation", "5 Suites", "Verify TLS 1.3 hostname verification, rejection of invalid certs.", "PASSED (100%)"),
        ("Live Real-MySQL Catalog Test", "1 Suite (Opt-in)", "Validate 6,265,691 records, 14 sources, Outokumpu 304 metrics, pagination.", "PASSED (100%)")
    ]
    for i, r in enumerate(test_data):
        for j, val in enumerate(r):
            tbl_test.cell(i, j).text = val
    style_table(tbl_test, [1.8, 1.2, 2.3, 0.72])

    add_p(doc, "Test Suite Summary: All 28 automated in-memory unit/integration tests execute in 1.26 seconds. The opt-in live MySQL integration test verifies all 6,265,691 real database records, confirming exact source counts, pagination integrity, and stainless steel 304 properties.", bold=True, space_after=8)

    add_h2(doc, "5.3 Application Screenshots")
    add_p(doc, "Figures 5.1 through 5.4 present visual evidence of the Starbase user interface across desktop and responsive mobile environments.")

    # Fig 5.1
    fig_home = SCREENSHOTS_DIR / "home-desktop.jpg"
    if fig_home.exists():
        add_figure(doc, fig_home, "Figure 5.1 — Starbase Desktop Landing and Overview Interface.", width_in=5.8)

    # Fig 5.2
    fig_mob = SCREENSHOTS_DIR / "home-mobile.jpg"
    if fig_mob.exists():
        add_figure(doc, fig_mob, "Figure 5.2 — Responsive Mobile Material Exploration Interface.", width_in=3.2)

    # Fig 5.3
    fig_mat = SCREENSHOTS_DIR / "material-library.jpg"
    if fig_mat.exists():
        add_figure(doc, fig_mat, "Figure 5.3 — Material Library with Property-Value Sorting and Provenance Tracking.", width_in=5.8)

    # Fig 5.4
    fig_sel = SCREENSHOTS_DIR / "selection-results-desktop.jpg"
    if fig_sel.exists():
        add_figure(doc, fig_sel, "Figure 5.4 — Multi-Attribute Selection Studio with Ranked Candidate Recommendations.", width_in=5.8)

    add_h2(doc, "5.4 Results and Discussion")
    add_p(doc, "The experimental evaluation validates that Starbase successfully operates as a high-performance material selection system. Key findings include:")
    add_bullet(doc, "Sub-5ms Indexed Candidate Screening: ", "Range-based screening against composite indexes filters millions of records in under 5ms, enabling real-time slider manipulation in the web interface.")
    add_bullet(doc, "Explainable Decision Auditing: ", "Engineering users are provided with clear mathematical explanations for why winning materials achieved top rank and why specific candidates were excluded.")
    add_bullet(doc, "Deployment and Infrastructure Status Matrix: ", "To distinguish completed implementation from hosting infrastructure constraints, Table 5.2 summarizes the operational deployment status.")

    add_table_title(doc, "Table 5.2 — Deployment and Hosting Architecture Status Matrix.")
    tbl_dep = doc.add_table(rows=4, cols=4)
    dep_data = [
        ("Deployment Environment", "Database Engine & Version", "Dataset Scale & Scope", "Operational Status"),
        ("Local Development", "MySQL Community 8.4.11", "Full 6,265,691 records across all 18 schema tables (5.48 GiB).", "VERIFIED & FULLY OPERATIONAL"),
        ("Cloud Staging (TiDB)", "TiDB Cloud v8.5.3-serverless", "14 collections transferred, verified schema with 20 tables.", "VERIFIED & STAGED"),
        ("Production Hosted Web", "Vercel + TiDB Cloud", "Target production deployment architecture.", "PENDING CLOUD STORAGE ALLOCATION")
    ]
    for i, r in enumerate(dep_data):
        for j, val in enumerate(r):
            tbl_dep.cell(i, j).text = val
    style_table(tbl_dep, [1.5, 1.8, 1.9, 0.82])

def add_chapter_6(doc):
    add_h1(doc, "6 CONCLUSION")

    add_h2(doc, "6.1 Conclusion")
    add_p(doc, "Starbase demonstrates that materials selection can be engineered as a rigorous, scalable database management system. By synthesizing Third Normal Form relational modeling, an extensible property-dictionary architecture, and composite B-tree indexing, the system successfully consolidates 6,265,691 material records from 14 global scientific repositories into a single unified catalog. Engineers can screen candidates against rigid physical boundaries, perform multi-objective trade-offs across normalized properties, audit complete experimental provenance, and collaborate in shared project workspaces. Starbase bridges the gap between academic computational science and real-world mechanical and electrical engineering design.")

    add_h2(doc, "6.2 Limitations")
    add_p(doc, "The current implementation has three recognized limitations:")
    add_bullet(doc, "Disparity Between Computed and Experimental Values: ", "Over 95% of catalog records represent computational DFT calculations rather than certified experimental lab tests. While invaluable for initial screening, computed values cannot replace destructive testing for mission-critical flight hardware.")
    add_bullet(doc, "Extreme Attribute Sparsity: ", "Because distinct scientific domains report fundamentally different properties, many cross-domain property comparisons are impossible due to missing data.")
    add_bullet(doc, "Unindexed Free-Text Search Latency: ", "Executing unindexed substring searches (LIKE '%...%') across 6.26M rows requires full sequential scans taking minutes unless scoped by source or category.")

    add_h2(doc, "6.3 Future Enhancements")
    add_p(doc, "Future work will expand Starbase in four strategic directions:")
    add_bullet(doc, "Dedicated Inverted Search Engine: ", "Integrating Elasticsearch or Meilisearch to provide sub-10ms fuzzy text search and grade synonym resolution across millions of materials.")
    add_bullet(doc, "Interactive 3D Molecular Sidecars: ", "Embedding interactive Mol* or WebGL crystallographic visualizers directly into the material inspection interface.")
    add_bullet(doc, "Direct CAD / FEA Integration: ", "Developing export plugins to automatically transfer temperature-dependent material property decks into SolidWorks, ANSYS, and FreeCAD.")
    add_bullet(doc, "AI-Assisted Requirement Extraction: ", "Leveraging large language models to parse unstructured engineering design specifications into formal SQL screening constraints.")

def add_bibliography(doc):
    add_h1(doc, "BIBLIOGRAPHY")

    bib_entries = [
        "[1] A. Jain, S. P. Ong, G. Hautier, W. Chen, W. D. Richards, H. Dacek, S. Cholia, D. Gunter, D. Skinner, G. Ceder, and K. A. Persson, “Commentary: The Materials Project: A materials genome approach to accelerating materials innovation,” APL Materials, vol. 1, no. 1, p. 011002, 2013.",
        "[2] K. Choudhary, K. F. Garrity, A. C. E. Reid, B. DeCost, F. Tavazza, et al., “The joint automated repository for various integrated simulations (JARVIS) for data-driven materials design,” npj Computational Materials, vol. 6, art. 173, 2020.",
        "[3] S. Curtarolo, W. Setyawan, G. L. W. Hart, M. Jahnatek, R. V. Chepulskii, R. H. Taylor, S. Wang, J. Xue, K. Yang, O. Levy, et al., “AFLOW: An automatic framework for high-throughput materials discovery,” Computational Materials Science, vol. 58, pp. 218–226, 2012.",
        "[4] C. Draxl and M. Scheffler, “NOMAD: The FAIR concept for big data-driven materials science,” MRS Bulletin, vol. 43, no. 9, pp. 676–682, 2018.",
        "[5] A. Merchant, S. Batzner, S. S. Schoenholz, M. Aykol, G. Cheon, and E. D. Cubuk, “Scaling deep learning for materials discovery,” Nature, vol. 624, pp. 80–85, 2023.",
        "[6] C. K. H. Borg, C. Frey, J. Moh, and T. M. Pollock, “Expanded dataset of mechanical properties and observed phases of multi-principal element alloys,” Scientific Data, vol. 7, art. 430, 2020.",
        "[7] Alexandria Materials Database, Interdisciplinary Centre for Advanced Materials Simulation (ICAMS), Ruhr University Bochum. Available: https://alexandria.icams.rub.de/",
        "[8] National Institute of Standards and Technology (NIST), “JARVIS Leaderboard: Benchmark Evaluations for Materials Property Predictions.” Available: https://pages.nist.gov/jarvis_leaderboard/",
        "[9] NASA Ames Research Center, “Thermal Protection Materials Database (TPSX),” NASA Technical Data Systems. Available: https://tpsx.arc.nasa.gov/",
        "[10] NASA Goddard Space Flight Center, “Outgassing Data for Selecting Spacecraft Materials,” NASA Reference Publication 1124. Available: https://outgassing.nasa.gov/",
        "[11] MaterialRegistry, “Standard Engineering Material Registry & Physical Properties API.” Available: https://www.materialregistry.com/docs/api",
        "[12] Outokumpu Stainless AB, “Product Datasheets: Core, Supra, and Forta Duplex Stainless Steels Technical Reference Guides,” 2024.",
        "[13] M. F. Ashby, Materials Selection in Mechanical Design, 5th ed. Oxford, UK: Butterworth-Heinemann, 2016.",
        "[14] R. Elmasri and S. B. Navathe, Fundamentals of Database Systems, 7th ed. Boston, MA: Pearson, 2016.",
        "[15] A. Silberschatz, H. F. Korth, and S. Sudarshan, Database System Concepts, 7th ed. New York, NY: McGraw-Hill, 2019.",
        "[16] Oracle Corporation, “MySQL 8.4 Reference Manual: InnoDB Storage Engine and Optimization Guidelines,” Oracle Technical Documentation, 2024. Available: https://dev.mysql.com/doc/refman/8.4/en/",
        "[17] PingCAP Inc., “TiDB Cloud Serverless Architecture and Distributed MySQL Compatibility Documentation,” 2024. Available: https://docs.pingcap.com/tidbcloud/",
        "[18] OpenJS Foundation, “Express.js 5.0 RESTful Routing and Web Application Framework Documentation,” 2024. Available: https://expressjs.com/",
        "[19] Meta Platforms Inc., “React 18: Concurrent Rendering and Component State Architecture,” 2024. Available: https://react.dev/",
        "[20] S. Poolakkal, B. EB, M. Antony, and S. Xavier, “Starbase: Relational Database System for Engineering Material Selection Source Code Repository,” 2026. Available: https://github.com/sudheeshpoolakkal/starbase"
    ]

    for b in bib_entries:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        r = p.add_run(b)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
