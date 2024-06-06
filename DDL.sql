--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

-- Started on 2024-06-06 17:30:29

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 212 (class 1255 OID 45264)
-- Name: clean_data_m(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.clean_data_m()
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO DATA_HST SELECT * FROM DATA_M;
    DELETE FROM DATA_M WHERE reg_timestamp < CURRENT_DATE;
END;
$$;


ALTER PROCEDURE public.clean_data_m() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 211 (class 1259 OID 45247)
-- Name: data_hst; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.data_hst (
    load_id integer NOT NULL,
    source character(3),
    reg_timestamp timestamp without time zone,
    f_time character varying(50),
    f_flight character varying(50),
    f_start_airport character varying(50),
    f_dest_airport character varying(50),
    f_state character varying(50)
);


ALTER TABLE public.data_hst OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 45235)
-- Name: data_m; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.data_m (
    load_id integer NOT NULL,
    source character(3),
    reg_timestamp timestamp without time zone,
    f_time character varying(50),
    f_flight character varying(50),
    f_start_airport character varying(50),
    f_dest_airport character varying(50),
    f_state character varying(50)
);


ALTER TABLE public.data_m OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 45238)
-- Name: load_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.load_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.load_id_seq OWNER TO postgres;

--
-- TOC entry 3172 (class 2606 OID 45256)
-- Name: data_hst data_hst_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.data_hst
    ADD CONSTRAINT data_hst_pk PRIMARY KEY (load_id);


--
-- TOC entry 3170 (class 2606 OID 45258)
-- Name: data_m data_m_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.data_m
    ADD CONSTRAINT data_m_pk PRIMARY KEY (load_id);


-- Completed on 2024-06-06 17:30:29

--
-- PostgreSQL database dump complete
--

