UPDATE mysql.user SET Password = PASSWORD('****PASS_HERE****') WHERE User = 'root';
FLUSH PRIVILEGES;
DROP USER ''@'localhost';
DROP USER ''@'host_name';