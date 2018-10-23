--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.14
-- Dumped by pg_dump version 9.5.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: regions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.regions (id, name, slug, created, last_updated, country_id, extra_1) FROM stdin;
1	Region I (Ilocos Region)	region-i	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
2	Region II (Cagayan Valley)	region-ii	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
3	Region III (Central Luzon)	region-iii	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
4	Region IV-A (CALABARZON)	region-iv-a	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
5	Region V (Bicol Region)	region-v	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
6	Region VI (Western Visayas)	region-vi	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
7	Region VII (Central Visayas)	region-vii	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
8	Region VIII (Eastern Visayas)	region-viii	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
9	Region IX (Zamboanga Peninsula)	region-ix	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
10	Region X (Nothern Mindanao)	region-x	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
11	Region XI (Davao Region)	region-xi	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
12	Region XII (SOCCSKSARGEN)	region-xii	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
13	National Capital Region (NCR)	ncr	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
14	Cordillera Administrative Region (CAR)	car	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
15	Autonomous Region in Muslim Mindanao (ARMM)	armm	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
16	Region XIII (Caraga)	region-xiii	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
17	Region IV-B (MIMAROPA)	region-iv-b	2018-06-09 06:09:25+00	2018-06-09 06:09:25+00	169	\N
\.


--
-- Name: regions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.regions_id_seq', 17, true);


--
-- PostgreSQL database dump complete
--

