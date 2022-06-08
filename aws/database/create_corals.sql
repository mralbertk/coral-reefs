-- Bad table with improper key

CREATE TABLE IF NOT EXISTS coral_segmentation(
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    island VARCHAR(30) NOT NULL,
    location INT NOT NULL,
    year_taken YEAR NOT NULL,
    coral_coverage DECIMAL(5,2)
);

-- Good (?) table with proper key

CREATE TABLE IF NOT EXISTS coral_coverage(
    island VARCHAR(30) NOT NULL,
    location INT NOT NULL,
    year_taken YEAR NOT NULL,
    coral_coverage DECIMAL(5,2) NOT NULL,
    last_update DATE NOT NULL,
    PRIMARY KEY (island, location, year_taken)
);

-- Proper table

CREATE TABLE IF NOT EXISTS coral_coverage(
    island VARCHAR(30) NOT NULL,
    location INT NOT NULL,
    year INT NOT NULL,
    coverage DECIMAL(5,2) NOT NULL,
    last_update DATE NOT NULL,
    PRIMARY KEY (island, location, year)
);