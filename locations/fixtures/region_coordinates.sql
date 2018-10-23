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
-- Data for Name: region_coordinates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.region_coordinates (id, created, last_updated, lat, lon, is_approved, region_id, user_id) FROM stdin;
\.


--
-- Name: region_coordinates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.region_coordinates_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

