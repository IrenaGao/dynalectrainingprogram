BEGIN TRANSACTION;

CREATE TABLE courses (
    idcourses INT(11),
    name VARCHAR(45),
    courseno INT(11),
    deptid VARCHAR(45),
    timecomp INT(11),
    freqperyear INT(11),
    allemp TINYINT(4)
);

INSERT INTO courses
(idcourses, name, courseno, deptid, timecomp, freqperyear, allemp)
VALUES
(1, 'Cleaning of Electric Components', 1, 'QA', 0.66, 0, 0);

COMMIT;