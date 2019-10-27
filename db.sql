create table card (
	id serial primary key,
	number varchar(16) not null,
	password varchar(32) not null,
	balance decimal(12,2) not null,
	lock bool not null,

	CONSTRAINT unique_number UNIQUE (number)
);

create table log (
	id serial primary key,
	card_id integer references card(id),
	date timestamp,
	details varchar(256)
);

-- password: 2222
insert into card (number, password, balance, lock) values (
	'1111111111111111',
	'934b535800b1cba8f96a5d72f72f1611',
	10000.00,
	false
);

-- password: 3333
insert into card (number, password, balance, lock) values (
	'2222222222222222',
	'2be9bd7a3434f7038ca27d1918de58bd',
	20000.00,
	false
);
