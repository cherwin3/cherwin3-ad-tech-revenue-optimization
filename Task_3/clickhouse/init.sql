CREATE DATABASE IF NOT EXISTS adstream;

CREATE TABLE IF NOT EXISTS adstream.ad_events
(
    user_id String,
    page_id String,
    recommended_position String,
    ad_format String,
    predicted_viewability Float32,
    estimated_rpm Float32,
    source String,
    llm_used UInt8,
    latency_ms Float32,
    event_time DateTime
)
ENGINE = MergeTree
ORDER BY (event_time, page_id);