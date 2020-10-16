create table if not exists users
(
	id bigint not null
		constraint users_pk
			primary key,
	name varchar(64)
);

alter table users owner to postgres;

create table if not exists actions
(
	user_id bigint not null
		constraint actions_users_id_fk
			references users
				on update cascade on delete restrict,
	actions varchar(128) not null,
	time timestamp default now() not null
);

alter table actions owner to postgres;

