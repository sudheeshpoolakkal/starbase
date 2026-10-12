-- 1. MATERIAL CATEGORY
CREATE TABLE material_category (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- 2. DATA SOURCE
CREATE TABLE data_source (
    source_id INT PRIMARY KEY,
    source_name VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    publication_year INT,
    doi_or_url VARCHAR(500)
);

-- 3. MATERIAL
CREATE TABLE material (
    material_id INT PRIMARY KEY,
    category_id INT NOT NULL REFERENCES material_category(category_id),
    data_source_id INT NOT NULL REFERENCES data_source(source_id),
    material_name VARCHAR(255) NOT NULL UNIQUE,
    material_code VARCHAR(100) NOT NULL UNIQUE,
    density_g_cm3 NUMERIC(8, 4),
    description TEXT
);

-- 4. MATERIAL PROPERTY
CREATE TABLE material_property (
    property_id INT PRIMARY KEY,
    material_id INT NOT NULL REFERENCES material(material_id) ON DELETE CASCADE,
    property_type VARCHAR(50) NOT NULL,
    property_name VARCHAR(100) NOT NULL,
    property_value NUMERIC(12, 4) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    test_condition VARCHAR(255) DEFAULT 'Standard Ambient (25°C, 1 atm)'
);

-- 5. MANUFACTURING PROCESS
CREATE TABLE manufacturing_process (
    process_id INT PRIMARY KEY,
    process_name VARCHAR(100) NOT NULL UNIQUE,
    process_type VARCHAR(50) NOT NULL,
    description TEXT
);

-- 6. MATERIAL PROCESS
CREATE TABLE material_process (
    material_id INT NOT NULL REFERENCES material(material_id) ON DELETE CASCADE,
    process_id INT NOT NULL REFERENCES manufacturing_process(process_id) ON DELETE CASCADE,
    feasibility_score INT,
    notes TEXT,
    PRIMARY KEY (material_id, process_id)
);

-- 7. MATERIAL COST
CREATE TABLE material_cost (
    cost_id INT PRIMARY KEY,
    material_id INT NOT NULL REFERENCES material(material_id) ON DELETE CASCADE,
    cost_per_unit NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    unit_of_measure VARCHAR(20) NOT NULL,
    effective_date DATE NOT NULL,
    supplier_name VARCHAR(255)
);

-- ============================================================
-- EXPANDED SEED DATA (37 REAL-WORLD ENGINEERING MATERIALS)
-- ============================================================

-- 1. CATEGORIES
INSERT INTO material_category (category_id, category_name, description) VALUES
(1, 'Metals & Alloys', 'Ferrous, non-ferrous, structural, and high-temperature alloys'),
(2, 'Engineering Polymers', 'Thermoplastics, thermosets, and high-performance polymers'),
(3, 'Technical Ceramics', 'High-hardness, refractory, and dielectric ceramic materials'),
(4, 'Composites', 'Fiber-reinforced polymers and structural laminates'),
(5, 'Glasses & Semiconductors', 'Optical glasses, silica, and semiconductor substrates');

-- 2. DATA SOURCES
INSERT INTO data_source (source_id, source_name, publisher, publication_year, doi_or_url) VALUES
(101, 'ASM Materials Information Database', 'ASM International', 2022, 'https://www.asminternational.org'),
(102, 'MatWeb Material Property Data', 'MatWeb LLC', 2023, 'https://www.matweb.com'),
(103, 'CES EduPack Materials Handbook', 'Ansys Granta', 2021, 'https://www.ansys.com/products/materials');

-- 3. MATERIALS (37 Total)
INSERT INTO material (material_id, category_id, data_source_id, material_name, material_code, density_g_cm3, description) VALUES
(1, 1, 101, 'Aluminum 6061-T6', 'Al 6061-T6', 2.7000, 'Precipitation-hardened aluminum alloy containing magnesium and silicon'),
(2, 1, 101, 'Stainless Steel 304', 'SS 304', 8.0000, 'Austenitic chromium-nickel stainless steel with high corrosion resistance'),
(3, 1, 102, 'Titanium Ti-6Al-4V (Grade 5)', 'Ti-6Al-4V', 4.4300, 'Alpha-beta titanium alloy with ultra-high strength-to-weight ratio'),
(4, 1, 101, 'Copper C11000 (ETP)', 'Cu-ETP', 8.8900, 'Electrolytic Tough Pitch copper with high thermal and electrical conductivity'),
(5, 1, 101, 'Brass C36000 (Free-Cutting)', 'CuZn39Pb3', 8.5000, 'Standard brass alloy optimized for high-speed automatic machining'),
(6, 1, 101, 'Inconel 718', 'NC19FeNb', 8.1900, 'Nickel-chromium superalloy for extreme high-temperature aerospace environments'),
(7, 1, 101, 'Magnesium AZ31B', 'AZ31B-H24', 1.7700, 'Ultra-lightweight wrought magnesium alloy with good formability'),
(8, 1, 101, 'Tool Steel D2', 'AISI-D2', 7.7000, 'High-carbon, high-chromium cold-work tool steel with high wear resistance'),
(9, 1, 101, 'Structural Steel A36', 'ASTM-A36', 7.8500, 'Standard low-carbon structural steel used in construction and framing'),
(10, 1, 101, 'Aluminum 7075-T6', 'Al 7075-T6', 2.8100, 'Very high strength zinc-bearing aluminum alloy used in aerospace structures'),
(11, 1, 101, 'Stainless Steel 316L', 'SS 316L', 8.0000, 'Low-carbon molybdenum stainless steel with superior marine pitting resistance'),
(12, 1, 101, 'Cast Iron G2500 (Gray)', 'Class 35', 7.2000, 'Gray iron with excellent vibration damping and thermal conductivity'),
(13, 2, 102, 'Polyether Ether Ketone (PEEK)', 'PEEK-1000', 1.3200, 'High-performance thermoplastic with extreme chemical and heat resistance'),
(14, 2, 102, 'Polycarbonate', 'PC-Lexan', 1.2000, 'Transparent engineering thermoplastic with high impact strength'),
(15, 2, 102, 'Nylon 6/6 (PA 66)', 'PA-66', 1.1400, 'Strong engineering plastic with high mechanical strength and rigidity'),
(16, 2, 102, 'Acrylonitrile Butadiene Styrene', 'ABS-Standard', 1.0500, 'Common thermoplastic polymer used for 3D printing and enclosures'),
(17, 2, 102, 'Polytetrafluoroethylene (PTFE)', 'Teflon', 2.2000, 'Fluoropolymer with ultra-low friction coefficient and chemical inertness'),
(18, 2, 102, 'Polypropylene', 'PP-Homopolymer', 0.9000, 'Low-density commodity thermoplastic with high fatigue and chemical resistance'),
(19, 2, 102, 'Polyethylene Terephthalate', 'PETG', 1.2700, 'Clear glycol-modified polyester with high toughness and chemical resistance'),
(20, 2, 102, 'Polyurethane Elastomer', 'PU-Shore90A', 1.2100, 'Flexible thermoset elastomer with high abrasion resistance'),
(21, 2, 102, 'Polylactic Acid', 'PLA-Standard', 1.2400, 'Biodegradable thermoplastic derived from renewable plant starch'),
(22, 2, 102, 'Polyacetal (POM / Delrin)', 'POM-H', 1.4200, 'High-rigidity engineering thermoplastic with low friction and dimensional stability'),
(23, 3, 103, 'Alumina Ceramic (99.5%)', 'Al2O3-995', 3.8900, 'Technical ceramic with high hardness, dielectric strength, and wear resistance'),
(24, 3, 103, 'Silicon Carbide', 'SSiC', 3.1000, 'Extremely hard ceramic with high thermal conductivity and thermal shock resistance'),
(25, 3, 103, 'Zirconia (Y-TZP)', 'ZrO2-Y2O3', 6.0500, 'Yttria-stabilized zirconia with exceptional fracture toughness among ceramics'),
(26, 3, 103, 'Silicon Nitride', 'Si3N4-GasSintered', 3.2500, 'High-strength structural ceramic used in high-speed bearings and gas turbines'),
(27, 3, 103, 'Boron Carbide', 'B4C-Armor', 2.5200, 'Third hardest material known; used in ballistic body armor and shielding'),
(28, 3, 103, 'Aluminum Nitride', 'AlN-Substrate', 3.2600, 'Ceramic with exceptionally high thermal conductivity and electrical insulation'),
(29, 4, 103, 'Carbon Fiber Composite (Epoxy/CF 60%)', 'CFRP-UD', 1.5500, 'Unidirectional carbon fiber reinforced polymer matrix composite'),
(30, 4, 103, 'Fiberglass Composite (FR-4)', 'FR4-Epoxy', 1.8500, 'Glass-reinforced epoxy laminate widely used in printed circuit boards'),
(31, 4, 103, 'Glass-Filled Nylon (PA66-GF30)', 'PA66-GF30', 1.3500, '30% glass fiber reinforced nylon with elevated stiffness and strength'),
(32, 4, 103, 'Kevlar Composite (Arimid/Epoxy)', 'AFRP-Aramid', 1.3800, 'Aramid fiber composite offering high impact absorption and tensile strength'),
(33, 4, 103, 'Carbon Fiber PEEK (CF30-PEEK)', 'PEEK-CF30', 1.4400, '30% carbon fiber reinforced PEEK for extreme mechanical and thermal environments'),
(34, 5, 103, 'Borosilicate Glass (Pyrex)', 'Glass-Pyrex', 2.2300, 'Low thermal expansion glass resistant to thermal shock and chemical attack'),
(35, 5, 103, 'Fused Silica (Quartz)', 'SiO2-Fused', 2.2000, 'High-purity amorphous silica with ultra-high optical transparency'),
(36, 5, 101, 'Monocrystalline Silicon', 'Si-Wafer', 2.3300, 'High-purity semiconductor substrate used in integrated circuits and solar cells'),
(37, 5, 101, 'Gallium Arsenide', 'GaAs-Semi', 5.3200, 'Compound semiconductor with high electron mobility for RF microelectronics');

-- 4. MATERIAL PROPERTIES
INSERT INTO material_property (property_id, material_id, property_type, property_name, property_value, unit, test_condition) VALUES
(1, 1, 'Mechanical', 'Yield Strength', 276.0, 'MPa', '23°C'),
(2, 1, 'Mechanical', 'Tensile Strength', 310.0, 'MPa', '23°C'),
(3, 1, 'Thermal', 'Thermal Conductivity', 167.0, 'W/m-K', '25°C'),
(4, 2, 'Mechanical', 'Yield Strength', 215.0, 'MPa', '23°C'),
(5, 2, 'Mechanical', 'Tensile Strength', 505.0, 'MPa', '23°C'),
(6, 2, 'Thermal', 'Thermal Conductivity', 16.2, 'W/m-K', '100°C'),
(7, 3, 'Mechanical', 'Yield Strength', 880.0, 'MPa', '23°C'),
(8, 3, 'Mechanical', 'Tensile Strength', 950.0, 'MPa', '23°C'),
(9, 4, 'Electrical', 'Electrical Conductivity', 58.0, 'MS/m', '20°C'),
(10, 4, 'Thermal', 'Thermal Conductivity', 391.0, 'W/m-K', '20°C'),
(11, 5, 'Mechanical', 'Tensile Strength', 380.0, 'MPa', '23°C'),
(12, 6, 'Mechanical', 'Tensile Strength', 1375.0, 'MPa', '23°C'),
(13, 6, 'Thermal', 'Max Operating Temp', 650.0, '°C', 'Continuous'),
(14, 7, 'Mechanical', 'Yield Strength', 200.0, 'MPa', '23°C'),
(15, 8, 'Mechanical', 'Hardness (Rockwell C)', 60.0, 'HRC', '23°C'),
(16, 9, 'Mechanical', 'Yield Strength', 250.0, 'MPa', '23°C'),
(17, 10, 'Mechanical', 'Tensile Strength', 572.0, 'MPa', '23°C'),
(18, 11, 'Mechanical', 'Yield Strength', 290.0, 'MPa', '23°C'),
(19, 12, 'Mechanical', 'Compressive Strength', 820.0, 'MPa', '23°C'),
(20, 13, 'Mechanical', 'Tensile Strength', 100.0, 'MPa', '23°C'),
(21, 13, 'Thermal', 'Melting Point', 343.0, '°C', '1 atm'),
(22, 14, 'Mechanical', 'Tensile Strength', 62.0, 'MPa', '23°C'),
(23, 15, 'Mechanical', 'Tensile Strength', 85.0, 'MPa', '23°C'),
(24, 16, 'Mechanical', 'Tensile Strength', 40.0, 'MPa', '23°C'),
(25, 17, 'Thermal', 'Max Operating Temp', 260.0, '°C', 'Continuous'),
(26, 18, 'Mechanical', 'Yield Strength', 33.0, 'MPa', '23°C'),
(27, 19, 'Mechanical', 'Tensile Strength', 50.0, 'MPa', '23°C'),
(28, 20, 'Mechanical', 'Tensile Strength', 45.0, 'MPa', '23°C'),
(29, 21, 'Mechanical', 'Tensile Strength', 60.0, 'MPa', '23°C'),
(30, 22, 'Mechanical', 'Tensile Strength', 70.0, 'MPa', '23°C'),
(31, 23, 'Mechanical', 'Compressive Strength', 2600.0, 'MPa', '23°C'),
(32, 24, 'Thermal', 'Thermal Conductivity', 120.0, 'W/m-K', '25°C'),
(33, 25, 'Mechanical', 'Fracture Toughness', 8.0, 'MPa-m^1/2', '23°C'),
(34, 26, 'Mechanical', 'Tensile Strength', 800.0, 'MPa', '23°C'),
(35, 27, 'Mechanical', 'Hardness (Vickers)', 2800.0, 'HV', '23°C'),
(36, 28, 'Thermal', 'Thermal Conductivity', 180.0, 'W/m-K', '25°C'),
(37, 29, 'Mechanical', 'Tensile Strength', 1500.0, 'MPa', '0° Fiber'),
(38, 30, 'Electrical', 'Dielectric Strength', 20.0, 'kV/mm', '23°C'),
(39, 31, 'Mechanical', 'Tensile Strength', 175.0, 'MPa', '23°C'),
(40, 32, 'Mechanical', 'Tensile Strength', 1400.0, 'MPa', '0° Fiber'),
(41, 33, 'Mechanical', 'Tensile Strength', 225.0, 'MPa', '23°C'),
(42, 34, 'Thermal', 'Max Operating Temp', 500.0, '°C', 'Continuous'),
(43, 35, 'Thermal', 'Thermal Conductivity', 1.4, 'W/m-K', '25°C'),
(44, 36, 'Electrical', 'Electrical Resistivity', 0.01, 'Ohm-cm', '25°C'),
(45, 37, 'Electrical', 'Electron Mobility', 8500.0, 'cm^2/V-s', '300 K');

-- 5. MANUFACTURING PROCESSES
INSERT INTO manufacturing_process (process_id, process_name, process_type, description) VALUES
(1, 'CNC Milling / Machining', 'Subtractive', 'Precision computer-controlled metal cutting'),
(2, 'Selective Laser Sintering (SLS)', 'Additive', '3D printing via laser fusion'),
(3, 'Investment Casting', 'Casting', 'Precision molten metal casting'),
(4, 'Injection Molding', 'Molding', 'High-volume pressure injection molding'),
(5, 'Autoclave Curing', 'Forming', 'High-pressure thermal consolidation'),
(6, 'Fused Deposition Modeling (FDM)', 'Additive', 'Standard filament-based 3D printing'),
(7, 'Powder Metallurgy / Sintering', 'Forming', 'High-pressure compaction and thermal bonding of powders');

-- 6. PROCESS MAPPING
INSERT INTO material_process (material_id, process_id, feasibility_score, notes) VALUES
(1, 1, 5, 'Highly machinable alloy'),
(1, 3, 4, 'Standard alloy for casting'),
(2, 1, 3, 'Requires rigid setups'),
(3, 1, 2, 'High tool wear'),
(4, 1, 4, 'Easy to machine'),
(5, 1, 5, 'Free-cutting brass benchmark'),
(13, 1, 4, 'Machinable high-temp polymer'),
(13, 4, 5, 'Requires elevated mold temps'),
(16, 4, 5, 'Excellent injection molding resin'),
(16, 6, 5, 'Standard FDM filament'),
(21, 6, 5, 'Easiest material for 3D printing'),
(23, 7, 5, 'Standard ceramic press-sinter process'),
(29, 5, 5, 'Aerospace autoclave curing'),
(31, 4, 5, 'High strength glass-filled molding');

-- 7. MATERIAL COSTS
INSERT INTO material_cost (cost_id, material_id, cost_per_unit, currency, unit_of_measure, effective_date, supplier_name) VALUES
(1, 1, 3.85, 'USD', 'kg', '2026-02-01', 'McMaster-Carr Supply Co.'),
(2, 2, 4.90, 'USD', 'kg', '2026-02-01', 'Ryerson Steel Distribution'),
(3, 3, 35.50, 'USD', 'kg', '2026-02-01', 'TIMET Aerospace Metals'),
(4, 4, 9.20, 'USD', 'kg', '2026-02-01', 'Luvata Copper Products'),
(5, 5, 7.50, 'USD', 'kg', '2026-02-01', 'Midwest Metal Supply'),
(6, 6, 48.00, 'USD', 'kg', '2026-02-01', 'Special Metals Corp'),
(7, 7, 5.10, 'USD', 'kg', '2026-02-01', 'Luxfer MAG Metals'),
(8, 8, 8.50, 'USD', 'kg', '2026-02-01', 'Bohler Uddeholm'),
(9, 9, 1.20, 'USD', 'kg', '2026-02-01', 'ArcelorMittal Steel'),
(10, 10, 6.40, 'USD', 'kg', '2026-02-01', 'Kaiser Aluminum'),
(11, 11, 6.10, 'USD', 'kg', '2026-02-01', 'Outokumpu Stainless'),
(12, 12, 1.80, 'USD', 'kg', '2026-02-01', 'Waupaca Foundry'),
(13, 13, 88.00, 'USD', 'kg', '2026-02-01', 'Victrex Polymer Materials'),
(14, 14, 2.75, 'USD', 'kg', '2026-02-01', 'Sabic Innovative Plastics'),
(15, 15, 3.20, 'USD', 'kg', '2026-02-01', 'BASF Performance Materials'),
(16, 16, 2.10, 'USD', 'kg', '2026-02-01', 'LG Chem Ltd.'),
(17, 17, 18.50, 'USD', 'kg', '2026-02-01', 'Chemours Teflon'),
(18, 18, 1.45, 'USD', 'kg', '2026-02-01', 'LyondellBasell Polymers'),
(19, 19, 2.30, 'USD', 'kg', '2026-02-01', 'Eastman Chemical'),
(20, 20, 4.60, 'USD', 'kg', '2026-02-01', 'Covestro Polyurethanes'),
(21, 21, 1.90, 'USD', 'kg', '2026-02-01', 'NatureWorks PLA'),
(22, 22, 3.80, 'USD', 'kg', '2026-02-01', 'DuPont Delrin'),
(23, 23, 18.20, 'USD', 'kg', '2026-02-01', 'CoorsTek Technical Ceramics'),
(24, 24, 42.00, 'USD', 'kg', '2026-02-01', 'Saint-Gobain Ceramics'),
(25, 25, 55.00, 'USD', 'kg', '2026-02-01', 'Toshiba Materials'),
(26, 26, 65.00, 'USD', 'kg', '2026-02-01', 'Kyocera Fine Ceramics'),
(27, 27, 120.00, 'USD', 'kg', '2026-02-01', '3M Advanced Materials'),
(28, 28, 78.00, 'USD', 'kg', '2026-02-01', 'Tokai Carbon'),
(29, 29, 115.00, 'USD', 'kg', '2026-02-01', 'Toray Composite Materials'),
(30, 30, 4.50, 'USD', 'kg', '2026-02-01', 'Isola Group PCB'),
(31, 31, 4.10, 'USD', 'kg', '2026-02-01', 'EMS-GRIVORY Polymers'),
(32, 32, 95.00, 'USD', 'kg', '2026-02-01', 'DuPont Kevlar Systems'),
(33, 33, 140.00, 'USD', 'kg', '2026-02-01', 'Solvay Specialty Polymers'),
(34, 34, 3.50, 'USD', 'kg', '2026-02-01', 'Schott AG Glass'),
(35, 35, 22.00, 'USD', 'kg', '2026-02-01', 'Corning Inc.'),
(36, 36, 180.00, 'USD', 'kg', '2026-02-01', 'GlobalWafers Silicon'),
(37, 37, 450.00, 'USD', 'kg', '2026-02-01', 'AXT Semiconductors');