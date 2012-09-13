INSERT INTO permissions VALUES('admin', 'balrogadmin', NULL, 1);

INSERT INTO rules (rule_id, priority, mapping, throttle, update_type, product, channel, data_version) VALUES(1, 100, 'Firefox-mozilla-central-nightly-latest', 100, 'minor', 'Firefox', 'nightly', 1);
INSERT INTO rules (rule_id, priority, mapping, throttle, update_type, product, channel, data_version) VALUES(2, 100, 'Firefox-mozilla-aurora-nightly-latest', 100, 'minor', 'Firefox', 'aurora', 1);
