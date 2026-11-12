-- Spotify Charts, 2017–2021 | Robyn Moore
-- PostgreSQL. Input is the prepared charts table for the study period.
-- Required columns are date, artist, title, region, and streams.
-- Each query returns one named result set for the dashboard analysis.

-- Result set: top_artists
SELECT
    artist,
    SUM(streams) AS total_streams
FROM charts
WHERE streams IS NOT NULL
    AND region != 'Global'
GROUP BY artist
ORDER BY total_streams DESC
LIMIT 10;

-- Result set: top_tracks
SELECT
    artist,
    title,
    SUM(streams) AS total_streams
FROM charts
WHERE streams IS NOT NULL
    AND region != 'Global'
GROUP BY artist, title
ORDER BY total_streams DESC
LIMIT 10;

-- Result set: ed_sheeran_yearly
SELECT
    EXTRACT(YEAR FROM date) AS year,
    SUM(streams) AS total_streams
FROM charts
WHERE streams IS NOT NULL
    AND region != 'Global'
    AND artist = 'Ed Sheeran'
GROUP BY year
ORDER BY year ASC;

-- Result set: top_markets
SELECT
    region,
    SUM(streams) AS total_streams
FROM charts
WHERE streams IS NOT NULL
    AND region != 'Global'
GROUP BY region
ORDER BY total_streams DESC
LIMIT 10;

-- Result set: artist_market_overindex
WITH Artist_Region AS (
    SELECT
        artist,
        region,
        SUM(streams) AS Artist_Region_Streams
    FROM charts
    WHERE streams IS NOT NULL
        AND region != 'Global'
        AND region != 'South Korea'
        AND EXTRACT(YEAR FROM date) = 2021
    GROUP BY artist, region
),
Artist_Total AS (
    SELECT
        artist,
        SUM(streams) AS Artist_Total_Streams
    FROM charts
    WHERE streams IS NOT NULL
        AND region != 'Global'
        AND region != 'South Korea'
        AND EXTRACT(YEAR FROM date) = 2021
    GROUP BY artist
),
Region_Total AS (
    SELECT
        region,
        SUM(streams) AS Region_Total_Streams
    FROM charts
    WHERE streams IS NOT NULL
        AND region != 'Global'
        AND region != 'South Korea'
        AND EXTRACT(YEAR FROM date) = 2021
    GROUP BY region
),
All_Market_Total AS (
    SELECT
        SUM(streams) AS All_Market_Streams
    FROM charts
    WHERE streams IS NOT NULL
        AND region != 'Global'
        AND region != 'South Korea'
        AND EXTRACT(YEAR FROM date) = 2021
    ),
Shares AS (
    SELECT
        Artist_Region.artist,
        Artist_Region.region,
        Artist_Region.Artist_Region_Streams,
        Artist_Total.Artist_Total_Streams,
        Region_Total.Region_Total_Streams,
        All_Market_Total.All_Market_Streams,
        Artist_Region.Artist_Region_Streams * 100.0
            / Artist_Total.Artist_Total_Streams AS Artist_Region_Share,
        Region_Total.Region_Total_Streams * 100.0
            / All_Market_Total.All_Market_Streams AS Region_Market_Share
    FROM Artist_Region
    JOIN Artist_Total
        ON Artist_Region.artist = Artist_Total.artist
    JOIN Region_Total
        ON Artist_Region.region = Region_Total.region
    CROSS JOIN All_Market_Total
)
SELECT
    *,
    Artist_Region_Share / Region_Market_Share AS Over_Index
FROM Shares
WHERE Artist_Total_Streams >= 100000000
    AND Artist_Region_Streams >= 10000000
ORDER BY Over_Index DESC;

-- Result set: artist_momentum_2021
WITH Half_Year_Streams AS (
    SELECT
        artist,
        SUM(CASE WHEN EXTRACT(MONTH FROM date) <= 6 THEN streams ELSE 0 END) AS H1_Streams,
        SUM(CASE WHEN EXTRACT(MONTH FROM date) >= 7 THEN streams ELSE 0 END) AS H2_Streams
    FROM charts
    WHERE streams IS NOT NULL
        AND region != 'Global'
        AND region != 'South Korea'
        AND EXTRACT(YEAR FROM date) = 2021
    GROUP BY artist
)
SELECT
    artist,
    H1_Streams,
    H2_Streams,
    H2_Streams - H1_Streams AS Stream_Increase,
    ROUND((H2_Streams - H1_Streams) * 100.0 / H1_Streams, 1) AS Growth_Percent
FROM Half_Year_Streams
WHERE H1_Streams >= 1000000
    AND H2_Streams >= 10000000
    AND H2_Streams > H1_Streams
    AND H2_Streams - H1_Streams >= 100000000
ORDER BY Growth_Percent DESC
LIMIT 20;

-- Result set: joao_gomes_track_momentum
SELECT
    INITCAP(LOWER(title)) AS title,
    SUM(CASE 
        WHEN EXTRACT(MONTH FROM date) <= 6 THEN streams 
        ELSE 0 
    END) AS H1_Streams,
    SUM(CASE 
        WHEN EXTRACT(MONTH FROM date) >= 7 THEN streams 
        ELSE 0 
    END) AS H2_Streams
FROM charts
WHERE streams IS NOT NULL
    AND region != 'Global'
    AND region != 'South Korea'
    AND EXTRACT(YEAR FROM date) = 2021
    AND artist = 'João Gomes'
GROUP BY LOWER(title)
ORDER BY H2_Streams DESC;

-- Result set: baby_keem_track_momentum
SELECT
    INITCAP(LOWER(title)) AS title,
    SUM(CASE 
        WHEN EXTRACT(MONTH FROM date) <= 6 THEN streams 
        ELSE 0 
    END) AS H1_Streams,
    SUM(CASE 
        WHEN EXTRACT(MONTH FROM date) >= 7 THEN streams 
        ELSE 0 
    END) AS H2_Streams
FROM charts
WHERE streams IS NOT NULL
    AND region != 'Global'
    AND region != 'South Korea'
    AND EXTRACT(YEAR FROM date) = 2021
    AND artist = 'Baby Keem'
GROUP BY LOWER(title)
ORDER BY H2_Streams DESC;
