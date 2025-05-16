DROP TABLE IF EXISTS request_interaction;
DROP TABLE IF EXISTS rating_interaction;

DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS rating;

DROP TABLE IF EXISTS exhibition;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS floor;

CREATE TABLE request (
    request_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    request_value SMALLINT NOT NULL,
    request_description VARCHAR(100),
    PRIMARY KEY (request_id)
);

CREATE TABLE rating (
    rating_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    rating_value SMALLINT NOT NULL,
    rating_description VARCHAR(100),
    PRIMARY KEY (rating_id)
);

CREATE TABLE department (
    department_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    department_name VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (department_id)
);

CREATE TABLE floor (
    floor_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    floor_name VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (floor_id)
);

CREATE TABLE exhibition (
    exhibition_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    exhibition_name VARCHAR(100) UNIQUE NOT NULL,
    exhibition_description TEXT,
    department_id SMALLINT,
    floor_id SMALLINT,
    exhibition_start_date DATE,
    public_id TEXT,
    PRIMARY KEY (exhibition_id),
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (floor_id) REFERENCES floor(floor_id)
);

CREATE TABLE request_interaction (
    request_interaction_id BIGINT GENERATED ALWAYS AS IDENTITY,
    exhibition_id SMALLINT,
    request_id SMALLINT,
    event_at TIMESTAMPTZ,
    PRIMARY KEY (request_interaction_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY (request_id) REFERENCES request(request_id)
);

CREATE TABLE rating_interaction (
    rating_interaction_id BIGINT GENERATED ALWAYS AS IDENTITY,
    exhibition_id SMALLINT,
    rating_id SMALLINT,
    event_at TIMESTAMPTZ,
    PRIMARY KEY (rating_interaction_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY (rating_id) REFERENCES rating(rating_id)
);

INSERT INTO floor(floor_name)
VALUES 
    ('Vault'),
    ('1'),
    ('2'),
    ('3')
;

INSERT INTO department(department_name)
VALUES 
    ('Entomology'),
    ('Geology'),
    ('Paleontology'),
    ('Zoology'),
    ('Ecology')
;

INSERT INTO exhibition(exhibition_name, exhibition_description, floor_id, department_id, exhibition_start_date, public_id)
VALUES 
    ('Adaptation', 'How insect evolution has kept pace with an industrialised world', 1, 1, TO_DATE('01/07/19', 'DD/MM/YYY'), 'EXH_01'),
    ('Measureless to Man', 'An immersive 3D experience: delve deep into a previously-inaccessible cave system.', 2, 2, TO_DATE('23/08/21', 'DD/MM/YYY'), 'EXH_00'),
    ('Thunder Lizards', 'How new research is making scientists rethink what dinosaurs really looked like.', 2, 3, TO_DATE('01/02/23', 'DD/MM/YYY'), 'EXH_05'),
    ('The Crenshaw Collection', 'An exhibition of 18th Century watercolours, mostly focused on South American wildlife.', 3, 4, TO_DATE('03/03/21', 'DD/MM/YYY'), 'EXH_02'),
    ('Our Polluted World', 'A hard-hitting exploration of humanity"s impact on the environment.', 4, 5, TO_DATE('12/05/21', 'DD/MM/YYY'), 'EXH_04'),
    ('Cetacean Sensations', 'Whales: from ancient myth to critically endangered.', 2, 4, TO_DATE('01/07/19', 'DD/MM/YYY'), 'EXH_03')
;

INSERT INTO request (request_value, request_description)
VALUES 
    (0, 'assistance'),
    (1, 'emergency')
;

INSERT INTO rating (rating_value, rating_description)
VALUES
    (0, 'Terrible'),
    (1, 'Bad'),
    (2, 'Neutral'),
    (3, 'Good'),
    (4, 'Amazing')
;