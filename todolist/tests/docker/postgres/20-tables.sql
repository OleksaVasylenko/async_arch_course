CREATE TYPE employee_type AS ENUM (
    'worker',
    'admin',
    'accountant',
    'manager'
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    type employee_type NOT NULL
);

CREATE TYPE task_status AS ENUM (
    'open',
    'done'
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    status task_status NOT NULL ,
    employee_id INTEGER REFERENCES employees(id) ON DELETE SET NULL
);

ALTER TABLE tasks OWNER TO testuser;
ALTER TABLE employees OWNER TO testuser;