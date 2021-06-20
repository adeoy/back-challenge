USE BACK_CHALLENGE;

INSERT INTO patient (first_name, last_name, birth_date, email, is_active) VALUES
('Jose', 'Villalobos', '1955-04-10', 'pepe@ejemplo.com', 1);
SET @_patient_id_1 = LAST_INSERT_ID();

INSERT INTO patient (first_name, last_name, birth_date, email, is_active) VALUES
('Jessica', 'Ramirez', '1971-07-01', 'jessica@ejemplo.com', 1);
SET @_patient_id_2 = LAST_INSERT_ID();

INSERT INTO patient (first_name, last_name, birth_date, email, is_active) VALUES
('Diana Laura', 'Del Toro', '1988-08-29', 'diana@ejemplo.com', 1);
SET @_patient_id_3 = LAST_INSERT_ID();

INSERT INTO patient (first_name, last_name, birth_date, email, is_active) VALUES
('Jorge Alberto', 'Trevino', '1990-05-05', 'jorge@ejemplo.com', 1);
SET @_patient_id_4 = LAST_INSERT_ID();

INSERT INTO study (urgency_level, body_part, description, type, is_active, patient_id) VALUES
('HIGH', 'STOMACH', 'NO FINDINGS', 'XRAY', 1, @_patient_id_1),
('HIGH', 'NECK', 'NORMAL THYROID', 'XRAY', 1, @_patient_id_2),
('LOW', 'CHEST', 'UNUSUAL RATIO', 'XRAY', 1, @_patient_id_4),
('MID', 'BREASTS', 'HIGH DENSITY ON LEFT SIDE', 'MAMMOGRAM', 1, @_patient_id_3);
