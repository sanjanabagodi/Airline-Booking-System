drop database [if exists] abs;
create database abs;

create table airport 
(	
	airport_code varchar(4) not null,
	airport_name varchar(50),
	city char(20) not null,
	country char(20) not null,
	zipp int not null,
	primary key(airport_code)
);

create table airline_company
(
	company_id varchar(3) not null,
	company_name varchar(50) not null,
	primary key(company_id)
);

create table airplane
(
	airplane_no varchar(4) not null,
	aircraft_type varchar(50) default 'Multi-engine land class',
	seating_capacity int not null,
	company_id varchar(20),

	primary key(airplane_no),
	foreign key(company_id) references airline_company(company_id)
);
 
create table travelling_agent
(
	name char(20) not null,
	t_id varchar(20) not null,
	ph_no bigint not null,
	company_name varchar(20) not null,
	primary key(t_id)
);

create table usser
(
	fname char(20) not null,
	mname char(20),
	lname char(20) not null,
	dob date not null,
	ph_no bigint not null,
	gender char(1) not null,
	passport_id varchar(20) not null,
	t_id varchar(20),

	primary key(passport_id),
	foreign key(t_id) references travelling_agent(t_id)
);

create table seat
(
	seat_no int not null,
	type varchar(20) not null,
	class varchar(15) not null,
	location varchar(20),
	airplane_no varchar(10),
	t_id varchar(20),

	primary key(seat_no, airplane_no),
	foreign key(airplane_no) references airplane(airplane_no),
	foreign key(t_id) references travelling_agent(t_id)
);

create table flight_trip
(
	source char(20) not null,
	destination char(20) not null,
	via char(20),
	dept_time time not null,
	arrival_time time not null,
	no_of_passengers int,
	trip_id varchar(20) not null,
	primary key(trip_id)
);

create table fare
(
	discount decimal,
	tax decimal,
	final_amount decimal not null,
	price decimal not null,
	fare_type char(20) not null,
	trip_id varchar(20),

	primary key(price),
	foreign key(trip_id) references flight_trip(trip_id)
);

create table goes_to
(
	airport_code varchar(15) not null,
	airplane_no varchar(10) not null,

	foreign key(airport_code) references airport(airport_code),
	foreign key(airplane_no) references airplane(airplane_no)
);

create table booking 
(
	t_id varchar(20) not null,
	trip_id varchar(20) not null,
	PNR char(6) not null,

	foreign key(t_id) references travelling_agent(t_id),
	foreign key(trip_id) references flight_trip(trip_id)
);

create table hop
(
	hop_id varchar(20) not null,
	distance decimal(7,2) not null,
	dept_time time,
	arrival_time time,
	dept_airport varchar(15) not null,
	arrival_airport varchar(15) not null,
	airplane_no varchar(10) not null,

	check(distance > 500.0),

	primary key(hop_id),
	foreign key(arrival_airport) references airport(airport_code),
	foreign key(dept_airport) references airport(airport_code),
	foreign key(airplane_no) references airplane(airplane_no)
);

create table has
(
	hop_id varchar(20) not null,
	trip_id varchar(20) not null,

	foreign key(hop_id) references hop(hop_id),
	foreign key(trip_id) references flight_trip(trip_id)
);

create table login_user
(
	username varchar(50) not null,
	passw varchar(20) not null
);


create table login_agent
(
	username varchar(50) not null,
	passw varchar(20) not null
);
