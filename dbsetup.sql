# Secure db
UPDATE mysql.user SET Password = PASSWORD('plym0utH') WHERE User = 'root';
FLUSH PRIVILEGES;
DROP USER ''@'localhost';
DROP USER ''@'host_name';

# Set up user
CREATE USER 'twitstream'@'localhost' IDENTIFIED BY 'tw1tstream!';
CREATE DATABASE twitstream;
GRANT ALL PRIVILEGES ON twitstream.* TO 'twitstream'@'localhost';

# Build tables
CREATE TABLE tweet (id INT NOT NULL AUTO_INCREMENT, time INT(13), username VARCHAR(20), tweet VARCHAR(200), PRIMARY KEY(id)); 
CREATE TABLE url (id INT NOT NULL AUTO_INCREMENT, url VARCHAR(2000), url_hash VARCHAR(32), domain VARCHAR(100), count INT, PRIMARY KEY (id));
CREATE TABLE tweet_urls (tweet_id INT NOT NULL, url_id INT NOT NULL);

# Fix character encoding to support emojis (#eggplantfist)
ALTER DATABASE twitstream CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE tweets CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tweets CHANGE tweet tweet VARCHAR(160) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;




