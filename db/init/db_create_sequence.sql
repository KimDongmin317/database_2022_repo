CREATE DATABASE IF NOT EXISTS `database_2022`;
USE `database_2022`;
CREATE USER 'kimdm'@'%' IDENTIFIED BY '1q2w3e4r';
GRANT ALL PRIVILEGES ON database_2022.* TO 'kimdm'@'%';
FLUSH PRIVILEGES;

DROP TABLE IF EXISTS univ_excel;
DROP TABLE IF EXISTS everytime_info;
DROP TABLE IF EXISTS review;

CREATE TABLE univ_excel (
    class_code_num VARCHAR(20) NOT NULL PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    professor_name VARCHAR(100) NOT NULL
);

CREATE TABLE everytime_info (
    everytime_lecture_number VARCHAR(20) NOT NULL PRIMARY KEY,
    class_code_num VARCHAR(20) NOT NULL
);

ALTER TABLE everytime_info
    ADD CONSTRAINT FK_CN
    FOREIGN KEY (class_code_num)
    REFERENCES univ_excel(class_code_num);

CREATE TABLE review (
    id INT NOT NULL PRIMARY KEY,
    review TEXT NOT NULL,
    star TINYINT NOT NULL,
    everytime_lecture_number VARCHAR(20) NOT NULL
);

ALTER TABLE review
    ADD CONSTRAINT FK_EN
    FOREIGN KEY (everytime_lecture_number)
    REFERENCES everytime_info(everytime_lecture_number);