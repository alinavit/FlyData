--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

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
-- Name: clean_data_m(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.clean_data_m()
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO DATA_HST SELECT * FROM DATA_M ON CONFLICT DO NOTHING;
    DELETE FROM DATA_M WHERE reg_timestamp < CURRENT_DATE;
END;
$$;


ALTER PROCEDURE public.clean_data_m() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
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
-- Name: v_data_m; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_data_m AS
 SELECT data_m.load_id,
        CASE data_m.source
            WHEN 'KTW'::bpchar THEN 'Katowice'::text
            WHEN 'SZZ'::bpchar THEN 'Szczecin'::text
            WHEN 'WMI'::bpchar THEN 'Warsaw Modlin'::text
            WHEN 'KRK'::bpchar THEN 'Kraków'::text
            WHEN 'POZ'::bpchar THEN 'Poznań'::text
            WHEN 'LCJ'::bpchar THEN 'Łódż'::text
            WHEN 'GDN'::bpchar THEN 'Gdańsk'::text
            ELSE NULL::text
        END AS source,
    data_m.reg_timestamp,
    data_m.f_time,
    data_m.f_flight,
        CASE data_m.f_start_airport
            WHEN 'KTW'::text THEN 'Katowice'::character varying
            WHEN 'SZZ'::text THEN 'Szczecin'::character varying
            WHEN 'WMI'::text THEN 'Warsaw Modlin'::character varying
            WHEN 'KRK'::text THEN 'Kraków'::character varying
            WHEN 'POZ'::text THEN 'Poznań'::character varying
            WHEN 'LCJ'::text THEN 'Łódż'::character varying
            WHEN 'GDN'::text THEN 'Gdańsk'::character varying
            ELSE data_m.f_start_airport
        END AS f_start_airport,
        CASE data_m.f_dest_airport
            WHEN 'KTW'::text THEN 'Katowice'::character varying
            WHEN 'SZZ'::text THEN 'Szczecin'::character varying
            WHEN 'WMI'::text THEN 'Warsaw Modlin'::character varying
            WHEN 'KRK'::text THEN 'Kraków'::character varying
            WHEN 'POZ'::text THEN 'Poznań'::character varying
            WHEN 'LCJ'::text THEN 'Łódż'::character varying
            WHEN 'GDN'::text THEN 'Gdańsk'::character varying
            ELSE data_m.f_dest_airport
        END AS f_dest_airport,
    replace((data_m.f_state)::text, 'Flight details'::text, ''::text) AS f_state
   FROM public.data_m
  WHERE ((data_m.f_flight IS NOT NULL) AND ((data_m.f_flight)::text <> ''::text) AND (to_char(data_m.reg_timestamp, 'YYYYMMDDHH24MM'::text) = ( SELECT to_char(max(data_m_1.reg_timestamp), 'YYYYMMDDHH24MM'::text) AS to_char
           FROM public.data_m data_m_1)));


ALTER TABLE public.v_data_m OWNER TO postgres;

--
-- Name: data_hst data_hst_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.data_hst
    ADD CONSTRAINT data_hst_pk PRIMARY KEY (load_id);


--
-- Name: data_m data_m_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.data_m
    ADD CONSTRAINT data_m_pk PRIMARY KEY (load_id);


--
-- PostgreSQL database dump complete
--

