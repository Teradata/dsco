WITH 
    qentry AS (
        SELECT
            FirstStepTime as EventTime
            , min(FirstStepTime) over() AS StartTime
            , 1 AS qcount
        FROM vt_all_test_queries
    )
    , qexit AS (
        SELECT
            FirstRespTime AS EventTime
            , min(FirstStepTime) over() AS StartTime
            , -1 AS qcount
        FROM vt_all_test_queries
    )
    , eventLog AS (
        SELECT 
            (EventTime - StartTime) second(4,6) as TTime
            , qcount
        FROM qentry
        UNION ALL
        SELECT
            (EventTime - StartTime) second(4,6) as TTime
            , qcount
        FROM qexit
    )
    , active AS (
        SELECT
            round(cast(TTime as NUMBER), -1) as TestTime
            , CSUM(qcount, TTime ASC) AS qsum
        FROM eventLog
    )
SELECT TestTime
    , median(qsum) as qmed
    , max(qsum) as qmax
    , min(qsum) as qmin
FROM active
group by TestTime
;