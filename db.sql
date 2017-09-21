DROP TABLE IF EXISTS "betrieb";
CREATE SEQUENCE betrieb_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 557 CACHE 1;

CREATE TABLE "public"."betrieb" (
    "id" integer DEFAULT nextval('betrieb_id_seq') NOT NULL,
    "bid" character varying(255),
    CONSTRAINT "betrieb_bid_unique" UNIQUE ("bid"),
    CONSTRAINT "betrieb_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE INDEX "betrieb_bid_index" ON "public"."betrieb" USING btree ("bid");


DROP TABLE IF EXISTS "posten";
CREATE SEQUENCE posten_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 10035 CACHE 1;

CREATE TABLE "public"."posten" (
    "id" integer DEFAULT nextval('posten_id_seq') NOT NULL,
    "schlachthof" character varying(255),
    "schlachtdatum" date,
    "betrieb_id" integer,
    CONSTRAINT "posten_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "posten_betrieb_id_foreign" FOREIGN KEY (betrieb_id) REFERENCES betrieb(id) NOT DEFERRABLE
) WITH (oids = false);

CREATE INDEX "posten_schlachtdatum_index" ON "public"."posten" USING btree ("schlachtdatum");


DROP TABLE IF EXISTS "konfiskate";
CREATE SEQUENCE konfiskate_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."konfiskate" (
    "id" integer DEFAULT nextval('konfiskate_id_seq') NOT NULL,
    "posten_id" integer,
    "anzahl" integer,
    "bezeichnung" character varying(255),
    "label" character varying(255),
    CONSTRAINT "konfiskate_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "konfiskate_posten_id_foreign" FOREIGN KEY (posten_id) REFERENCES posten(id) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "schwein";
CREATE SEQUENCE schwein_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 323211 CACHE 1;

CREATE TABLE "public"."schwein" (
    "id" integer DEFAULT nextval('schwein_id_seq') NOT NULL,
    "posten_id" integer,
    "label" character varying(255),
    "gewicht" real,
    "mfa" real,
    "jodzahl" real,
    "pufa" real,
    "speckmass" real,
    "fleischmass" real,
    CONSTRAINT "schwein_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "schwein_posten_id_foreign" FOREIGN KEY (posten_id) REFERENCES posten(id) NOT DEFERRABLE
) WITH (oids = false);
