DROP DATABASE IF EXISTS flagstaff_weather;
CREATE DATABASE IF NOT EXISTS flagstaff_weather;
USE flagstaff_weather;

CREATE TABLE weather_log (
id INT AUTO_INCREMENT PRIMARY KEY,
curr_datetime DATETIME NOT NULL,
curr_condition VARCHAR(100) NOT NULL,
curr_temperature DECIMAL(10, 2),
curr_location VARCHAR(30)
);

SELECT * FROM weather_log