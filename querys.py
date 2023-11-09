CREATE_TABLE_EVENTO_ODD_ARENA = '''CREATE TABLE [dbo].[eventooddarena](
                    [eventoid] [int]  NULL,
                    [evento] [nvarchar](1000) NULL,
                    [mercadoid] [int] NULL,
                    [nomemercado] [nvarchar](500) NULL,
                    [nomeodd] [nvarchar](500) NULL,
                    [cotacao] [float] NULL,
                    [inicioevento] [nvarchar](100) NULL,
                    [torneioid] [int] NULL,
                    [torneio] [nvarchar](1000) NULL,
                    [dataatualizacao] [datetime2](7) NULL,
                    [id] [int] IDENTITY(1,1) primary key NOT NULL )
                '''

CREATE_TABLE_EVENTO_ODD_ARENA_HISTORY = '''CREATE TABLE public.EventoOddArenaHistory
                ( 
                eventoid integer NOT NULL,
                evento character varying(1000) COLLATE pg_catalog."default" NOT NULL,
                mercadoid integer NOT NULL,
                nomemercado character varying(500) COLLATE pg_catalog."default" NOT NULL,
                nomeodd character varying(500) COLLATE pg_catalog."default" NOT NULL,
                cotacao double precision NOT NULL,
                inicioevento character varying(100) COLLATE pg_catalog."default",
                torneioid integer NOT NULL,
                torneio character varying(1000) COLLATE pg_catalog."default" NOT NULL,
                dataatualizacao timestamp with time zone NOT NULL,
                id SERIAL PRIMARY KEY
                )'''