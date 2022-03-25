create table `data_logs`(
	temperature varchar(10) NOT NULL,
    humidity varchar(10) NOT NULL,
    date_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
);