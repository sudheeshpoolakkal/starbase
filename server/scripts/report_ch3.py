from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from generate_academic_report import (
    DIAGRAMS_DIR, add_p, add_h1, add_h2, add_h3, add_bullet,
    add_figure, add_table_title, style_table
)

def add_chapter_3(doc):
    add_h1(doc, "3 DATABASE DESIGN")

    add_h2(doc, "3.1 Database Overview")
    add_p(doc, "The Starbase relational database is structured to balance rigorous Third Normal Form (3NF) relational integrity with high-throughput query performance across millions of scientific records. The local application DDL specifies exactly 18 relational tables, comprising 17 active application tables and one legacy user review table retained for backward compatibility. In the cloud deployment on TiDB Serverless, this footprint expands to 20 tables through the addition of two dedicated migration and audit support tables: Contribution_Review (which tracks collaborative dataset staging) and Catalog_Import_Progress (which records idempotent file byte offsets and batch transaction states during bulk cloud transfers).")

    add_p(doc, "The schema is partitioned into four logical functional groups, as detailed in Table 3.1.")

    add_table_title(doc, "Table 3.1 — Database Schema Architecture and Entity Groupings.")
    tbl_group = doc.add_table(rows=5, cols=4)
    group_data = [
        ("Group Name", "Table Count", "Entity Tables Included", "Functional Scope and Role"),
        ("Material Catalog Core", "7 Tables", "Material, Property, Material_Property, Data_Source, Material_Category, Application, Material_Application", "Stores materials, property dictionaries, physical measurements, units, categories, and applications."),
        ("Projects & Selections", "7 Tables", "Project, Project_Collaborator, Saved_Selection, Selection_Requirement, Shortlisted_Material, Material_Comparison, Project_Activity", "Manages collaborative engineering workspaces, selection parameter histories, shortlists, and activity feeds."),
        ("User Management & Auth", "4 Tables", "User, User_Session, System_Log, Material_Reviews (legacy)", "Handles authentication, bcrypt password hashing, session tokens, audit logging, and legacy user ratings."),
        ("Cloud Migration & Audit", "2 Tables", "Contribution_Review, Catalog_Import_Progress", "Dedicated to TiDB Cloud migration tracking, idempotent batch replays, and schema verification.")
    ]
    for i, r in enumerate(group_data):
        for j, val in enumerate(r):
            tbl_group.cell(i, j).text = val
    style_table(tbl_group, [1.5, 0.9, 1.9, 1.72])

    add_h2(doc, "3.2 Three-Schema Architecture")
    add_p(doc, "Starbase adheres to the ANSI/SPARC Three-Schema Architecture [14, 15], cleanly decoupling physical disk storage, logical relational structures, and client presentation views. Table 3.2 outlines this mapping.")

    add_table_title(doc, "Table 3.2 — Three-Schema Architecture Implementation in Starbase.")
    tbl_schema = doc.add_table(rows=4, cols=3)
    schema_data = [
        ("Architecture Level", "Implementation in Starbase", "Representative Technologies & Artifacts"),
        ("Internal Schema (Physical)", "InnoDB storage engine files, B-tree primary and secondary composite indexes, page allocation, UTF-8 MB4 character encodings, and TiDB Raft storage regions.", "MySQL 8.4 InnoDB table spaces, buffer pool memory allocation, composite index definitions, and TiKV peer regions."),
        ("Conceptual Schema (Logical)", "Normalized 3NF relational tables, entity keys, referential foreign key constraints, NOT NULL declarations, and UNIQUE composite integrity rules.", "schema.sql DDL, Data_Source, Material, Property, and Material_Property entity tables."),
        ("External Schema (View)", "Tailored JSON REST payloads, client-scoped material summary cards, comparative property projection tables, and anonymized user workspace states.", "Express API route projections (/api/materials, /api/materials/recommend), React state views.")
    ]
    for i, r in enumerate(schema_data):
        for j, val in enumerate(r):
            tbl_schema.cell(i, j).text = val
    style_table(tbl_schema, [1.5, 2.5, 2.02])

    add_h2(doc, "3.3 Entity–Relationship (ER) Diagram")
    add_p(doc, "The conceptual data model of Starbase represents the entities governing materials science data and collaborative engineering workflows. Figure 3.1 presents the complete Entity–Relationship (ER) diagram.")

    fig_er = DIAGRAMS_DIR / "Fig3-1_ER_Diagram.png"
    if fig_er.exists():
        add_figure(doc, fig_er, "Figure 3.1 — Entity–Relationship (ER) diagram for Starbase material catalog and workspace.", width_in=5.8)

    add_p(doc, "Table 3.3 documents the cardinality and referential rules governing the primary relationships in the ER model.")

    add_table_title(doc, "Table 3.3 — Entity Cardinality and Relationship Constraints.")
    tbl_card = doc.add_table(rows=9, cols=3)
    card_data = [
        ("Relationship", "Cardinality", "Integrity Rules & Structural Notes"),
        ("Data_Source to Material", "1 : N (One-to-Many)", "Every material must reference exactly one data source. Deleting a source is restricted if materials exist."),
        ("Material_Category to Material", "1 : N (One-to-Many)", "Every material belongs to exactly one category (e.g., Metal, Polymer, Ceramic, Composite)."),
        ("Material to Property", "M : N (Many-to-Many)", "Resolved via the Material_Property association table. Composite primary key on (material_id, property_id)."),
        ("Material to Application", "M : N (Many-to-Many)", "Resolved via the Material_Application association table. Cascades deletion upon material removal."),
        ("User to Project", "1 : N (One-to-Many)", "A user acts as Owner of zero or more engineering projects. Projects cascade upon owner deletion."),
        ("Project to Collaborator", "1 : N (One-to-Many)", "Users are invited to projects under 'read', 'write', or 'admin' access roles via Project_Collaborator."),
        ("Project to Saved_Selection", "1 : N (One-to-Many)", "A project records multiple selection iterations, capturing evolving engineering specifications."),
        ("Saved_Selection to Requirement", "1 : N (One-to-Many)", "Captures the exact numerical constraints and priority weights used during that selection run.")
    ]
    for i, r in enumerate(card_data):
        for j, val in enumerate(r):
            tbl_card.cell(i, j).text = val
    style_table(tbl_card, [1.8, 1.4, 2.82])

    add_h2(doc, "3.4 Relational Schema & Normalization Analysis")
    add_p(doc, "The conceptual ER model is mapped to a formal relational schema. In relational notation, primary keys are underlined, and foreign keys are designated in italics:")
    add_bullet(doc, "Data_Source", "(source_id, source_key, name, url, note, data_kind, license, version, checksum, imported_at, summary_json, import_state)")
    add_bullet(doc, "Material_Category", "(category_id, name, description)")
    add_bullet(doc, "Material", "(material_id, source_id, category_id, external_id, name, description, formula, crystal_system, space_group_number, is_active, metadata_json, created_at, updated_at)")
    add_bullet(doc, "Property", "(property_id, property_key, name, unit, data_type, category, description, is_active)")
    add_bullet(doc, "Material_Property", "(material_id, property_id, numeric_value, text_value, uncertainty, test_conditions, is_estimated)")
    add_bullet(doc, "Application", "(application_id, name, category, description)")
    add_bullet(doc, "Material_Application", "(material_id, application_id, suitability_score, notes)")
    add_bullet(doc, "User", "(user_id, email, password_hash, full_name, role, created_at, last_login)")
    add_bullet(doc, "Project", "(project_id, owner_id, name, description, status, created_at, updated_at)")
    add_bullet(doc, "Project_Collaborator", "(project_id, user_id, permission, invited_at)")
    add_bullet(doc, "Saved_Selection", "(selection_id, project_id, user_id, title, notes, created_at)")
    add_bullet(doc, "Selection_Requirement", "(requirement_id, selection_id, property_id, min_value, max_value, target_value, weight, is_mandatory)")

    add_h3(doc, "Formal Third Normal Form (3NF) Normalization Proof")
    add_p(doc, "To ensure optimal data consistency and prevent update, insertion, and deletion anomalies, the Starbase relational design was systematically normalized to Third Normal Form (3NF) [14, 15]. The proof proceeds through functional dependency (FD) analysis across the core entities:")

    add_p(doc, "1. Functional Dependencies Governing the Domain:", bold=True)
    add_p(doc, "Let the primary functional dependencies identified in the materials selection domain be:\n"
               "• FD1 (Data_Source): source_id -> {source_key, name, url, data_kind, license, version, checksum}\n"
               "• FD2 (Material_Category): category_id -> {name, description}\n"
               "• FD3 (Property): property_id -> {property_key, name, unit, data_type, category, description}\n"
               "• FD4 (Material): material_id -> {source_id, category_id, external_id, name, description, formula, crystal_system, space_group_number}\n"
               "• FD5 (Material_Property): {material_id, property_id} -> {numeric_value, text_value, uncertainty, test_conditions, is_estimated}\n"
               "• FD6 (Project): project_id -> {owner_id, name, description, status, created_at}\n"
               "• FD7 (User): user_id -> {email, password_hash, full_name, role}")

    add_p(doc, "2. First Normal Form (1NF) Compliance:", bold=True)
    add_p(doc, "A relation is in 1NF if and only if all underlying domains contain only atomic (indivisible) values, and there are no repeating groups. In unnormalized materials tables, multiple physical properties (e.g., tensile strength, density, thermal conductivity) are frequently packed into delimited strings or varying multi-valued arrays. In Starbase, every property measurement is decoupled into an atomic row in Material_Property, where numeric_value is a scalar DOUBLE and text_value is an atomic VARCHAR. No multi-valued attributes exist; hence, all relations satisfy 1NF.")

    add_p(doc, "3. Second Normal Form (2NF) Compliance:", bold=True)
    add_p(doc, "A relation is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on the entire primary key (no partial key dependencies). In all single-attribute primary key relations (Material, Property, Data_Source, User, Project), partial key dependencies are impossible by definition. In the composite-key relation Material_Property, the primary key is {material_id, property_id}. The non-prime attributes {numeric_value, text_value, uncertainty} depend simultaneously on BOTH the specific material and the specific property being measured. A material_id alone cannot determine a tensile strength value, nor can a property_id alone determine the strength of an unstated material. Therefore, no partial key dependencies exist, and Material_Property satisfies 2NF.")

    add_p(doc, "4. Third Normal Form (3NF) Compliance:", bold=True)
    add_p(doc, "A relation is in 3NF if it is in 2NF and no non-prime attribute is transitively dependent on the primary key (X -> Y and Y -> Z where Z is non-prime). In an unnormalized design where Material inlines category descriptions and data source licensing, transitive dependencies arise: material_id -> category_id -> category_description. If the category description changes, multiple material rows must be updated. Starbase eliminates all such transitive dependencies by decomposing category attributes into Material_Category and repository metadata into Data_Source. In every relation, for every non-trivial functional dependency X -> Y, X is a superkey. Thus, the database satisfies 3NF.")

    add_p(doc, "5. Prevention of Operational Anomalies:", bold=True)
    add_bullet(doc, "Insertion Anomalies: ", "A new material property definition (e.g., Critical Magnetic Field) can be registered in Property without requiring a dummy material record to exist.")
    add_bullet(doc, "Deletion Anomalies: ", "Deleting a discontinued material candidate does not purge the shared physical property definition or the catalog data source licensing terms.")
    add_bullet(doc, "Update Anomalies: ", "If an authoritative repository updates its download URL or version string, the update is executed on exactly one row in Data_Source, instantly propagating across all associated material records.")

    add_h3(doc, "Trade-off Analysis: Property-Dictionary (EAV) Model versus Wide Flat Tables")
    add_p(doc, "A foundational architectural decision in Starbase was adopting a normalized property dictionary (Entity-Attribute-Value) model for physical attributes rather than a traditional wide columnar table. In materials science, cataloging millions of items involves extreme heterogeneity: while metals report hardness, yield strength, and shear modulus, optical crystals report refractive indices and dielectric constants, and polymers report glass transition temperatures. A wide table encompassing all 40+ recognized properties across 6.26M rows would require over 250 million table cells, of which over 92% would be NULL. This causes severe index page fragmentation, wasteful disk footprint, and rigid schema change requirements. Conversely, the EAV model stores only measured properties, provides infinite extensibility for new physical metrics, and leverages compact composite B-tree indexes for lightning-fast range queries.")

    add_h2(doc, "3.5 Database Tables and Attributes")
    add_p(doc, "Tables 3.4 through 3.10 specify the structural data dictionary for the core schema tables.")

    add_table_title(doc, "Table 3.4 — Data Dictionary for Data_Source Entity.")
    tbl_ds = doc.add_table(rows=8, cols=3)
    ds_cols = [
        ("Attribute Name", "SQL Data Type", "Constraints & Description"),
        ("source_id", "INT AUTO_INCREMENT", "PRIMARY KEY. Unique integer surrogate identifier."),
        ("source_key", "VARCHAR(64)", "UNIQUE NOT NULL. Semantic identifier (e.g., 'nist-jarvis-elastic')."),
        ("name", "VARCHAR(255)", "NOT NULL. Full descriptive title of the repository."),
        ("url", "VARCHAR(500)", "Official repository endpoint or persistent DOI web URL."),
        ("data_kind", "ENUM('computed','experimental','literature-extracted')", "NOT NULL. Scientific methodology classification."),
        ("license", "VARCHAR(255)", "Upstream redistribution license (e.g., CC-BY-4.0, Public Domain)."),
        ("checksum", "VARCHAR(128)", "Cryptographic SHA-256 hash of the ingested raw payload archive.")
    ]
    for i, r in enumerate(ds_cols):
        for j, val in enumerate(r):
            tbl_ds.cell(i, j).text = val
    style_table(tbl_ds, [1.5, 2.0, 2.52])

    add_table_title(doc, "Table 3.5 — Data Dictionary for Material Entity.")
    tbl_mat = doc.add_table(rows=9, cols=3)
    mat_cols = [
        ("Attribute Name", "SQL Data Type", "Constraints & Description"),
        ("material_id", "INT AUTO_INCREMENT", "PRIMARY KEY. System-wide unique material surrogate key."),
        ("source_id", "INT", "FOREIGN KEY -> Data_Source(source_id) ON DELETE RESTRICT."),
        ("category_id", "INT", "FOREIGN KEY -> Material_Category(category_id) ON DELETE RESTRICT."),
        ("external_id", "VARCHAR(128)", "NOT NULL. Upstream accession identifier (e.g., 'mp-149')."),
        ("name", "VARCHAR(255)", "NOT NULL. Standard chemical formula, alloy designation, or trade name."),
        ("description", "TEXT", "Scientific description, processing history, or crystal structure summary."),
        ("is_active", "TINYINT(1)", "DEFAULT 1. Soft-delete flag preserving referential integrity."),
        ("metadata_json", "JSON / MEDIUMTEXT", "Reversible packed metadata (crystal lattice, raw citations, aliases).")
    ]
    for i, r in enumerate(mat_cols):
        for j, val in enumerate(r):
            tbl_mat.cell(i, j).text = val
    style_table(tbl_mat, [1.5, 2.0, 2.52])

    add_table_title(doc, "Table 3.6 — Data Dictionary for Property Entity.")
    tbl_prop = doc.add_table(rows=7, cols=3)
    prop_cols = [
        ("Attribute Name", "SQL Data Type", "Constraints & Description"),
        ("property_id", "INT AUTO_INCREMENT", "PRIMARY KEY. Unique property identifier."),
        ("property_key", "VARCHAR(64)", "UNIQUE NOT NULL. Programmatic key (e.g., 'tensileStrength', 'density')."),
        ("name", "VARCHAR(128)", "NOT NULL. Human-readable label (e.g., 'Tensile Strength, Ultimate')."),
        ("unit", "VARCHAR(32)", "Standard SI or engineering unit (e.g., 'MPa', 'g/cm³', 'W/m·K')."),
        ("data_type", "ENUM('numeric','text','boolean')", "NOT NULL. Target type discriminator for property values."),
        ("category", "VARCHAR(64)", "Domain grouping (e.g., 'Mechanical', 'Thermal', 'Electrical').")
    ]
    for i, r in enumerate(prop_cols):
        for j, val in enumerate(r):
            tbl_prop.cell(i, j).text = val
    style_table(tbl_prop, [1.5, 2.0, 2.52])

    add_table_title(doc, "Table 3.7 — Data Dictionary for Material_Property Association Table.")
    tbl_mp = doc.add_table(rows=6, cols=3)
    mp_cols = [
        ("Attribute Name", "SQL Data Type", "Constraints & Description"),
        ("material_id", "INT", "PRIMARY KEY & FOREIGN KEY -> Material(material_id) ON DELETE CASCADE."),
        ("property_id", "INT", "PRIMARY KEY & FOREIGN KEY -> Property(property_id) ON DELETE RESTRICT."),
        ("numeric_value", "DOUBLE", "Indexed floating-point numerical measurement in standardized units."),
        ("text_value", "VARCHAR(255)", "Descriptive rating or qualitative value (e.g., 'Excellent', 'High')."),
        ("test_conditions", "VARCHAR(255)", "Experimental ambient conditions (e.g., '293 K, 1 atm', 'Annealed').")
    ]
    for i, r in enumerate(mp_cols):
        for j, val in enumerate(r):
            tbl_mp.cell(i, j).text = val
    style_table(tbl_mp, [1.5, 2.0, 2.52])

    add_h2(doc, "3.6 Primary Keys, Foreign Keys and Constraints")
    add_p(doc, "Table 3.16 summarizes the primary and foreign key constraints, cascade rules, and domain integrity checks across the database.")

    add_table_title(doc, "Table 3.16 — Relational Constraints and Cascade Actions.")
    tbl_const = doc.add_table(rows=7, cols=4)
    const_data = [
        ("Table Name", "Primary Key", "Foreign Keys & Referenced Parent", "Cascade & Integrity Action"),
        ("Material", "material_id", "source_id -> Data_Source, category_id -> Material_Category", "ON DELETE RESTRICT (Prevents orphaned materials)."),
        ("Material_Property", "(material_id, property_id)", "material_id -> Material, property_id -> Property", "ON DELETE CASCADE on material; RESTRICT on property."),
        ("Material_Application", "(material_id, application_id)", "material_id -> Material, application_id -> Application", "ON DELETE CASCADE on material; RESTRICT on application."),
        ("Project", "project_id", "owner_id -> User(user_id)", "ON DELETE CASCADE (Deleting user removes owned projects)."),
        ("Project_Collaborator", "(project_id, user_id)", "project_id -> Project, user_id -> User", "ON DELETE CASCADE on both parent entities."),
        ("Saved_Selection", "selection_id", "project_id -> Project, user_id -> User", "ON DELETE CASCADE on project; SET NULL on user.")
    ]
    for i, r in enumerate(const_data):
        for j, val in enumerate(r):
            tbl_const.cell(i, j).text = val
    style_table(tbl_const, [1.4, 1.4, 1.9, 1.32])

    add_p(doc, "To achieve high performance across 6.26 million materials and dozens of millions of property measurements, dedicated B-tree indexes were engineered as listed in Table 3.17.")

    add_table_title(doc, "Table 3.17 — Database Indexing Strategy and Query Optimization Roles.")
    tbl_idx = doc.add_table(rows=6, cols=3)
    idx_data = [
        ("Index Identifier", "Target Table & Column Tuple", "Query Optimization Purpose and Execution Role"),
        ("material_numeric_index", "Material_Property(property_id, numeric_value)", "Powers range-based screening (e.g., tensileStrength >= 400). Eliminates table scans."),
        ("material_external_unique", "Material(source_id, external_id)", "Enforces unique source accession numbers and accelerates idempotent ETL batch reimports."),
        ("material_name_index", "Material(name)", "Optimizes alphabetical catalog browsing, prefix lookups, and exact grade matching."),
        ("material_category_index", "Material(category_id, is_active)", "Enables instant category filtering and active status verification."),
        ("proj_collab_user_idx", "Project_Collaborator(user_id, permission)", "Accelerates user workspace dashboard loading and authorization verification.")
    ]
    for i, r in enumerate(idx_data):
        for j, val in enumerate(r):
            tbl_idx.cell(i, j).text = val
    style_table(tbl_idx, [1.6, 2.0, 2.42])
