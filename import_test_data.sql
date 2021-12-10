


/*INSERT into AIRPORT values(airport_code, airport_name, city, country, zip)*/
INSERT into AIRPORT values('VIJU','Jammu Airport', 'Jammu', 'India', 190007);
INSERT into AIRPORT values('VAAH','Sardar Vallabhbhai Patel International Airport', 'Ahmedabad', 'India', 382475);
INSERT into AIRPORT values('VOBG','HAL Airport', 'Bengaluru', 'India', 560017);
INSERT into AIRPORT values('VIDD','Safdarjung Airport', 'New Delhi', 'India', 110003);
INSERT into AIRPORT values('VCCB', 'Batticaloa Airport', 'Batticaloa', 'Srilanka', 30000);
INSERT into AIRPORT values('VCCK', 'Koggala Airport', 'Galle', 'Srilanka', 80000);
INSERT into AIRPORT values('VGRJ', 'Shah Makhdum Airport', 'Rajshahi', 'Bangladesh', 6202);
INSERT into AIRPORT values('VHSS', 'Shun Tak Heliport', 'Sheung Wan', 'Hong Kong', 999077);
INSERT into AIRPORT values('VNKT', 'Tribhuvan International Airport', 'Kathmandu', 'Nepal', 44600);
INSERT into AIRPORT values('VQPR', 'Paro Airport', 'Paro', 'Bhutan', 12002);
INSERT into AIRPORT values('VLPS', 'Pakse Airport', 'Pakse', 'Laos', 1600);



/*INSERT into AIRLINE_COMPANY values(company_id, company_name);*/
INSERT into AIRLINE_COMPANY values('BML', 'Bismillah Airlines');
INSERT into AIRLINE_COMPANY values('BAV', 'Bay Aviation Ltd');
INSERT into AIRLINE_COMPANY values('DRK', 'Druk Air');
INSERT into AIRLINE_COMPANY values('CPA', 'Cathay Pacific');
INSERT into AIRLINE_COMPANY values('HKG', 'Government Flying Service');
INSERT into AIRLINE_COMPANY values('LEP', 'Air Costa');
INSERT into AIRLINE_COMPANY values('IGO', 'IndiGo');
INSERT into AIRLINE_COMPANY values('PMW', 'Paramount Airways');
INSERT into AIRLINE_COMPANY values('AMU', 'Air Macau');
INSERT into AIRLINE_COMPANY values('LAO', 'Lao Airlines');
INSERT into AIRLINE_COMPANY values('CIN', 'Cinnamon Air');



/*INSERT into AIRPLANE values(airplane_no, aircraft_type, seating capaity, company_id);*/
INSERT into AIRPLANE values('A158', NULL, 4000, 'BML');
INSERT into AIRPLANE values('B37M', NULL, 3500, 'BAV');
INSERT into AIRPLANE values('B748', NULL, 5900, 'DRK');
INSERT into AIRPLANE values('D328', NULL, 1100, 'CPA');
INSERT into AIRPLANE values('CONI', NULL, 900, 'HKG');
INSERT into AIRPLANE values('T210', NULL, 2400, 'LEP');
INSERT into AIRPLANE values('BL8', NULL, 1600, 'IGO');
INSERT into AIRPLANE values('E190', NULL, 4600, 'PMW');
INSERT into AIRPLANE values('F2TH', NULL, 2000, 'AMU');
INSERT into AIRPLANE values('GA8', NULL, 3100, 'LAO');
INSERT into AIRPLANE values('DOVE', NULL, 1500, 'CIN');



/*INSERT into TRAVELLING_AGENT values(name, travel_id, ph_no, company_name)*/
INSERT into TRAVELLING_AGENT values('Raj', 'TA128101', 9182638213, 'Yatra');
INSERT into TRAVELLING_AGENT values('Hank', 'TA273518', 7162643927, 'Cheapflights');
INSERT into TRAVELLING_AGENT values('Jones', 'TA836374', 8263411032, 'Skyscanner');
INSERT into TRAVELLING_AGENT values('Karthik', 'TA813576', 9173428819, 'Kiwi.com');
INSERT into TRAVELLING_AGENT values('Bala', 'TA528169', 6172539271, 'LowFares.com');
INSERT into TRAVELLING_AGENT values('Peter', 'TA252611', 9327436222, 'Goibibo');
INSERT into TRAVELLING_AGENT values('Mike', 'TA826329', 8299917238, 'Makemytrip');
INSERT into TRAVELLING_AGENT values('Shaurya', 'TA361892', 9122910199, 'Kesari Tours');
INSERT into TRAVELLING_AGENT values('Chen', 'TA173023', 8279918201, 'Expedia');
INSERT into TRAVELLING_AGENT values('Debarghya', 'TA162416', 7771912435, 'Priceline');
INSERT into TRAVELLING_AGENT values('Abe', 'TA817253', 6618181717, 'Cheapflights');



/*INSERT into USER values(fname, mname, lname, dob, ph_no, gender, passport_no, travel_id)*/
INSERT into USSER values('Roseline', NULL, 'Matthew', '1999-02-05', 9928183641, 'F', 'A2938101', 'TA128101');
INSERT into UsSER values('Sriranga', 'S', 'K', '1971-05-09', 8837856281, 'M', '19273518', 'TA273518');
INSERT into USSER values('Bhumika', 'M', 'S', '1985-11-16', 8777272622, 'F', 'M1836374', 'TA836374');
INSERT into USSER values('Simon', 'H', 'Peter', '2001-09-11', 6628367188, 'M', 'B2813576', 'TA813576');
INSERT into USSER values('Mohammad', NULL, 'Talha', '2000-07-23', 9992837599, 'M', '62528169', 'TA528169');
INSERT into USSER values('Anika', NULL, 'Sharma', '1994-04-29', 7199976567, 'F', 'H7252611', 'TA252611');
INSERT into USSER values('Debarghya', 'S', 'Bose', '1999-11-25', 6978179763, 'M', 'X1826329', 'TA826329');
INSERT into USSER values('Sonakshi', NULL, 'Dixit', '1964-08-13', 9739389992, 'F', '28361892', 'TA361892');
INSERT into USSER values('Agasthya', NULL, 'Kasthuri', '2005-06-01', 8199181772, 'M', 'A9173023', 'TA173023');
INSERT into USSER values('Akshay', 'A', 'Law', '1997-01-18', 8771871898, 'M', 'N8162416', 'TA162416');
INSERT into USSER values('Rashmi', NULL, 'Kousalya', '2001-12-14', 9188277163, 'F', 'C8817253', 'TA817253');



/*INSERT into SEAT values(seat_no, type, class, location, airplane_no, travel_id)*/
INSERT into SEAT values(45, 'seater', 'Economy', 'Aisle', 'A158', 'TA128101');
INSERT into SEAT values(69, 'sleeper', 'Business', 'Window', 'B37M', 'TA162416');
INSERT into SEAT values(236, 'couch', 'Business', 'Aisle', 'B748', 'TA173023');
INSERT into SEAT values(123, 'sleeper', 'First', 'Window', 'D328', 'TA252611');
INSERT into SEAT values(164, 'seater', 'Business', 'Window', 'CONI', 'TA273518');
INSERT into SEAT values(97, 'seater', 'Business', 'Aisle', 'T210', 'TA361892');
INSERT into SEAT values(61, 'seater', 'Economy', 'Middle', 'BL8', 'TA528169');
INSERT into SEAT values(401, 'couch', 'First', 'Aisle', 'E190', 'TA813576');
INSERT into SEAT values(10, 'seater', 'Economy','Middle', 'F2TH', 'TA817253');
INSERT into SEAT values(538, 'sleeper', 'Business', 'Middle', 'GA8', 'TA836374');
INSERT into SEAT values(379, 'couch', 'First', 'Window', 'DOVE', 'TA826329');



/*INSERT into FLIGHT_TRIP values(source, dest, via, dept_time, arrival_time, no_of_passengers, trip_id)*/
INSERT into FLIGHT_TRIP values('VIJU', 'VLPS', NULL, '13:00:00', '21:20:00', 2655, 'T123');
INSERT into FLIGHT_TRIP values('VOBG', 'VHSS', NULL, '19:30:00', '02:00:00', 1829, 'T261');
INSERT into FLIGHT_TRIP values('VAAH', 'VNKT', NULL, '23:40:00', '18:30:00', 923, 'T433');
INSERT into FLIGHT_TRIP values('VNKT', 'VIDD', NULL, '06:00:00', '12:15:00', 5432, 'T728');
INSERT into FLIGHT_TRIP values('VLPS', 'VQPR', NULL, '11:45:00', '14:30:00', 4276, 'T153');
INSERT into FLIGHT_TRIP values('VGRJ', 'VOBG', NULL, '08:10:00', '13:00:00', 3701, 'T192');
INSERT into FLIGHT_TRIP values('VIDD', 'VCCK', NULL, '15:25:00', '19:55:00', 2200, 'T839');
INSERT into FLIGHT_TRIP values('VHSS', 'VLPS', NULL, '21:20:00', '04:10:00', 799, 'T523');
INSERT into FLIGHT_TRIP values('VCCB', 'VGRJ', NULL, '05:00:00', '10:35:00', 3302, 'T222');
INSERT into FLIGHT_TRIP values('VQPR', 'VOBG', NULL, '17:50:00', '22:40:00', 1220, 'T437');
INSERT into FLIGHT_TRIP values('VCCK', 'VAAH', NULL, '09:35:00', '12:25:00', 2937, 'T325');



/*INSERT into FARE values(discount, tax, final_amt, price, fare_type, trip_id)*/
INSERT into FARE values(100.00, 45.53, 1645.53, 1700.00, 'cash', 'T123');
INSERT into FARE values(150.00, 53.22, 1903.22, 2000.00, 'online', 'T261');
INSERT into FARE values(90.00, 26.49, 1336.49, 1400.00, 'online', 'T433');
INSERT into FARE values(125.00, 57.03, 1732.03, 1800.00, 'card', 'T728');
INSERT into FARE values(110.00, 49.77, 2039.77, 2100.00, 'card', 'T153');
INSERT into FARE values(200.00, 91.04, 2391.04, 2500.00, 'online', 'T192');
INSERT into FARE values(80.00, 32.16, 1552.16, 1600.00, 'cash', 'T839');
INSERT into FARE values(75.00, 23.98, 1168.98, 1200.00, 'online', 'T523');
INSERT into FARE values(125.00, 56.12, 1681.12, 1750.00, 'cash', 'T222');
INSERT into FARE values(175.00, 69.25, 2194.25, 2300.00, 'card', 'T437');
INSERT into FARE values(125.00, 57.13, 1732.13, 1820.00, 'card', 'T325');



/*INSERT into GOES_TO values(airport_code, airplane_no)*/
INSERT into GOES_TO values('VIJU', 'A158');
INSERT into GOES_TO values('VAAH', 'B37M');
INSERT into GOES_TO values('VOBG', 'B748');
INSERT into GOES_TO values('VIDD', 'D328');
INSERT into GOES_TO values('VCCB', 'CONI');
INSERT into GOES_TO values('VCCK', 'T210');
INSERT into GOES_TO values('VGRJ', 'BL8');
INSERT into GOES_TO values('VHSS', 'E190');
INSERT into GOES_TO values('VNKT', 'F2TH');
INSERT into GOES_TO values('VQPR', 'GA8');
INSERT into GOES_TO values('VLPS', 'GA8');



/*INSERT into BOOKING values(travel_id, trip_id, PNR)*/
INSERT into BOOKING values('TA128101', 'T123', 'X37Q1C');
INSERT into BOOKING values('TA273518', 'T261', 'HS829V');
INSERT into BOOKING values('TA836374', 'T433', 'B927SH');
INSERT into BOOKING values('TA813576', 'T728', 'K88DGA');
INSERT into BOOKING values('TA528169', 'T153', 'SI0123');
INSERT into BOOKING values('TA252611', 'T192', 'UAG237');
INSERT into BOOKING values('TA826329', 'T839', '27GA7W');
INSERT into BOOKING values('TA361892', 'T523', '81GAJS');
INSERT into BOOKING values('TA173023', 'T222', 'V18WYB');
INSERT into BOOKING values('TA162416', 'T437', '9XBAU2');
INSERT into BOOKING values('TA817253', 'T325', 'U9DCB6');



/*INSERT into HOP values(hop_id, distance, dep_time, arrival_time, dep_airport, arrival_airport, airplane_no)*/
INSERT into HOP values('A122', 1235, '13:00:00', '15:20:00', 'VIJU', 'VAAH', 'A158');
INSERT into HOP values('B817', 967, '19:30:00', '22:00:00', 'VAAH', 'VOBG', 'B37M');
INSERT into HOP values('H412', 843, '23:40:00', '03:30:00', 'VOBG', 'VIDD', 'B748');
INSERT into HOP values('B019', 1249, '06:00:00', '10:15:00', 'VIDD', 'VCCB', 'D328');
INSERT into HOP values('L726', 2013, '11:45:00', '14:30:00', 'VCCB', 'VCCK', 'CONI');
INSERT into HOP values('N661', 1651, '08:10:00', '09:00:00', 'VCCK', 'VGRJ', 'T210');
INSERT into HOP values('I915', 702, '15:25:00', '16:55:00', 'VGRJ', 'VHSS', 'BL8');
INSERT into HOP values('Y524', 911, '21:20:00', '01:10:00', 'VHSS', 'VNKT', 'E190');
INSERT into HOP values('C880', 1393, '05:00:00', '08:35:00', 'VNKT', 'VQPR', 'F2TH');
INSERT into HOP values('D911', 1086, '17:50:00', '18:40:00', 'VQPR', 'VLPS', 'GA8');
INSERT into HOP values('J333', 1198, '09:35:00', '11:25:00', 'VLPS', 'VIJU', 'DOVE');



/*INSERT into HAS values(hop_id, trip_id)*/
INSERT into HAS values('A122', 'T123');
INSERT into HAS values('B817', 'T261');
INSERT into HAS values('H412', 'T433');
INSERT into HAS values('B019', 'T728');
INSERT into HAS values('L726', 'T153');
INSERT into HAS values('N661', 'T192');
INSERT into HAS values('I915', 'T839');
INSERT into HAS values('Y524', 'T523');
INSERT into HAS values('C880', 'T222');
INSERT into HAS values('D911', 'T437');
INSERT into HAS values('J333', 'T325');



INSERT into LOGIN_USER values('user_user1', 'pqrs');
INSERT into LOGIN_USER values('user_user2', '3456');



INSERT into LOGIN_AGENT values('travelling_agent_alex', '1234');
INSERT into LOGIN_AGENT values('travelling_agent_julia', 'abcd');


