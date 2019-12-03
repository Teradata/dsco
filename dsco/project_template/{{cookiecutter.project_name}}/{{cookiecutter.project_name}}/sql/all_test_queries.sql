CREATE MULTISET VOLATILE TABLE {{ vt_table }}
AS ( 
    WITH
    test_summary AS (
        SELECT *
        FROM tqst_analytics.systemtestsummary AS sts
        WHERE sts.run_id = {{ run_id }}
    )
    , dbql_rough AS (
        SELECT dbql.*
        FROM {{ db }}.{{ dbql }} AS dbql
        JOIN test_summary AS sts
        ON dbql.wlasystemid = sts.systemid
           AND dbql.logdate BETWEEN sts.logdate AND sts.max_logdate
           AND dbql.starttime BETWEEN sts.start_time AND sts.end_time
    )
    , dbql_test AS (
        SELECT 
            dbql.*
        FROM dbql_rough AS dbql
        WHERE upper(dbql.StatementType) NOT IN ('SET QUERY_BAND')
              AND upper(dbql.Requestmode) IN ('EXEC', 'BOTH')
              AND dbql.QueryText LIKE '%/*%'
              AND lower(TRIM(REGEXP_SUBSTR(dbql.QueryText, '(?<=/\*).*?(?=\*/)')))
                  NOT IN ('delete_opt_cost_table',
                          'delete_opt_dbsctl_table',
                          'diagnostic_dump_costs',
                          'get_opt_dbsctl_data')
              AND upper(dbql.UserName) <> 'TEST_DETAILS_COLLECTOR'
    ) 
    select *
    from dbql_test
)
WITH DATA NO PRIMARY INDEX
ON COMMIT PRESERVE ROWS;