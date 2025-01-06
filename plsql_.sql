DO $$
DECLARE
    tabela_dzis    TEXT;
    tabela_wczoraj   TEXT;
    v_sql          TEXT;
BEGIN
    tabela_dzis := 'a'||replace(to_char(CURRENT_DATE, 'YYYYMMDD'), '-', '');
    tabela_wczoraj := 'a'||replace(to_char(CURRENT_DATE- 1, 'YYYYMMDD'), '-', '');

    v_sql := 'CREATE OR REPLACE VIEW dzienne_porownanie AS
              SELECT T1.imie, T1.plemie, T1.punkty - T2.punkty AS roznica
              FROM '||quote_ident(tabela_dzis)||' T1
              LEFT JOIN '||quote_ident(tabela_wczoraj)||' T2 ON T1.imie = T2.imie
              ORDER BY roznica DESC';

    BEGIN
        EXECUTE v_sql;
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'Wystąpił błąd: %', SQLERRM;
    END;
END $$;

