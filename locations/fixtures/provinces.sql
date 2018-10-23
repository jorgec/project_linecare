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
-- Data for Name: provinces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.provinces (id, name, slug, created, last_updated, country_id, region_id) FROM stdin;
1	Abra	abra	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	14
2	Agusan del Norte	agusan-del-norte	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	16
3	Agusan del Sur	agusan-del-sur	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	16
4	Aklan	aklan	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	6
5	Albay	albay	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	5
6	Antique	antique	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	6
7	Apayao	apayao	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	14
8	Aurora	aurora	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	3
9	Basilan	basilan	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	15
10	Bataan	bataan	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	3
11	Batanes	batanes	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	2
12	Batangas	batangas	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	4
13	Benguet	benguet	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	14
14	Biliran	biliran	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	8
15	Bohol	bohol	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	7
16	Bukidnon	bukidnon	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	10
17	Bulacan	bulacan	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	3
18	Cagayan	cagayan	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	2
19	Camarines Norte	camarines-norte	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	5
20	Camarines Sur	camarines-sur	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	5
21	Camiguin	camiguin	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	10
22	Capiz	capiz	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	6
23	Catanduanes	catanduanes	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	5
24	Cavite	cavite	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	4
25	Cebu	cebu	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	7
26	Compostela Valley	compostela-valley	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	11
27	Cotabato	cotabato	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	12
28	Davao del Norte	davao-del-norte	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	11
29	Davao del Sur	davao-del-sur	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	11
30	Davao Oriental	davao-oriental	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	11
31	Eastern Samar	eastern-samar	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	8
32	Guimaras	guimaras	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	6
33	Ifugao	ifugao	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	14
34	Ilocos Norte	ilocos-norte	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	1
35	Ilocos Sur	ilocos-sur	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	1
36	Iloilo	iloilo	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	6
37	Isabela	isabela	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	2
38	Kalinga	kalinga	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	14
39	La Union	la-union	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	1
40	Laguna	laguna	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	4
41	Lanao del Norte	lanao-del-norte	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	10
42	Lanao del Sur	lanao-del-sur	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	15
43	Leyte	leyte	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	8
44	Maguindanao	maguindanao	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	15
45	Marinduque	marinduque	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	17
46	Masbate	masbate	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	5
47	Metro Manila	metro-manila	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	13
48	Misamis Occidental	misamis-occidental	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	10
49	Misamis Oriental	misamis-oriental	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	10
50	Mountain Province	mountain-province	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	14
51	Negros Occidental	negros-occidental	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	6
52	Negros Oriental	negros-oriental	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	7
53	Northern Samar	northern-samar	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	8
54	Nueva Ecija	nueva-ecija	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	3
55	Nueva Vizcaya	nueva-vizcaya	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	2
56	Occidental Mindoro	occidental-mindoro	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	17
57	Oriental Mindoro	oriental-mindoro	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	17
58	Palawan	palawan	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	17
59	Pampanga	pampanga	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	3
60	Pangasinan	pangasinan	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	1
61	Quezon	quezon	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	4
62	Quirino	quirino	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	4
63	Rizal	rizal	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	4
64	Romblon	romblon	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	17
65	Samar	samar	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	8
66	Sarangani	sarangani	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	12
67	Siquijor	siquijor	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	7
68	Sorsogon	sorsogon	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	5
69	South Cotabato	south-cotabato	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	12
70	Southern Leyte	southern-leyte	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	8
71	Sultan Kudarat	sultan-kudarat	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	12
72	Sulu	sulu	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	15
73	Surigao del Norte	surigao-del-norte	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	16
74	Surigao del Sur	surigao-del-sur	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	16
75	Tarlac	tarlac	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	3
76	Tawi-Tawi	tawi-tawi	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	15
77	Zambales	zambales	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	3
78	Zamboanga del Norte	zamboanga-del-norte	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	9
79	Zamboanga del Sur	zamboanga-del-sur	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	9
80	Zamboanga Sibugay	zamboanga-sibugay	2018-06-09 06:09:33+00	2018-06-09 06:09:33+00	169	9
\.


--
-- Name: provinces_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.provinces_id_seq', 80, true);


--
-- PostgreSQL database dump complete
--

