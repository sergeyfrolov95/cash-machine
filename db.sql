create table card (
	id serial primary key,
	number varchar(16) not null,
	password varchar not null,
	balance decimal(12,2) not null,
	lock bool not null
);

create table log (
	id serial primary key,
	card_id integer references card(id),
	date timestamp,
	details varchar(256)
);
