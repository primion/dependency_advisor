# SQL


# Basics

The database is ~/.cache/grype/db/5/vulnerability.db

Listing tables:

sqlite> .tables
id                             vulnerability_match_exclusion
vulnerability                  vulnerability_metadata

## id

sqlite> PRAGMA table_info(id);
0|build_timestamp|TEXT|0||0
1|schema_version|INTEGER|0||0

Current schema version is 5

## vulnerability

sqlite> PRAGMA table_info( vulnerability);
0|pk|INTEGER|0||1
1|id|TEXT|0||0
2|package_name|TEXT|0||0
3|namespace|TEXT|0||0
4|package_qualifiers|TEXT|0||0
5|version_constraint|TEXT|0||0
6|version_format|TEXT|0||0
7|cpes|TEXT|0|null|0
8|related_vulnerabilities|TEXT|0|null|0
9|fixed_in_versions|TEXT|0|null|0
10|fix_state|TEXT|0||0
11|advisories|TEXT|0|null|0

SELECT * from vulnerability limit 5000;
4979|GHSA-53hp-jpwq-2jgq|org.apache.tomcat:tomcat|github:language:java||>=10.0.0-M1,<=10.0.0-M4|unknown||[{"id":"CVE-2020-11996","namespace":"nvd:cpe"}]|["10.0.0-M5"]|fixed|
4980|GHSA-53hp-jpwq-2jgq|org.apache.tomcat:tomcat|github:language:java||>=9.0.0.M1,<9.0.35|unknown||[{"id":"CVE-2020-11996","namespace":"nvd:cpe"}]|["9.0.35"]|fixed|

LIKE. And search for rtos

select * from vulnerability where package_name like "rtos";
49858|CVE-2006-0620|rtos|nvd:cpe||= 6.2.1b || = 6.2.1a || = 6.2.1|unknown|["cpe:2.3:a:qnx:rtos:6.2.1b:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.2.1a:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.2.1:*:*:*:*:*:*:*"]|||unknown|
73751|CVE-2002-2407|rtos|nvd:cpe||= 6.2a || = 6.2|unknown|["cpe:2.3:a:qnx:rtos:6.2:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.2a:*:*:*:*:*:*:*"]|||unknown|
74200|CVE-2004-1390|rtos|nvd:cpe||= 6.2.0 || = 4.25 || = 6.2.0a || = 2.4 || = 6.1.0|unknown|["cpe:2.3:a:qnx:rtos:6.2.0a:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:2.4:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.1.0:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.2.0:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:4.25:*:*:*:*:*:*:*"]|||unknown|
74202|CVE-2004-1391|rtos|nvd:cpe||= 6.2.0 || = 6.2.1b || = 6.3.0 || = 6.1.0a || = 6.2.1a || = 6.1.0|unknown|["cpe:2.3:a:qnx:rtos:6.1.0:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.2.0:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.2.1b:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.3.0:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.1.0a:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.2.1a:*:*:*:*:*:*:*"]|||unknown|
75425|CVE-2005-2725|rtos|nvd:cpe||= 6.3.0 || = 6.1.0|unknown|["cpe:2.3:a:qnx:rtos:6.3.0:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.1.0:*:*:*:*:*:*:*"]|||unknown|
191600|CVE-2002-0793|rtos|nvd:cpe||= 4.25|unknown|["cpe:2.3:a:qnx:rtos:4.25:*:*:*:*:*:*:*"]|||unknown|
191775|CVE-2002-1239|rtos|nvd:cpe||= 6.2.0|unknown|["cpe:2.3:a:qnx:rtos:6.2.0:*:*:*:*:*:*:*"]|||unknown|
192109|CVE-2002-1983|rtos|nvd:cpe||= 6.1.0|unknown|["cpe:2.3:a:qnx:rtos:6.1.0:*:*:*:*:*:*:*"]|||unknown|
192138|CVE-2002-2039|rtos|nvd:cpe||= 4.25 || = 6.1.0|unknown|["cpe:2.3:a:qnx:rtos:4.25:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.1.0:*:*:*:*:*:*:*"]|||unknown|
192139|CVE-2002-2040|rtos|nvd:cpe||= 4.25 || = 6.1.0|unknown|["cpe:2.3:a:qnx:rtos:4.25:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.1.0:*:*:*:*:*:*:*"]|||unknown|
192140|CVE-2002-2041|rtos|nvd:cpe||= 6.1.0|unknown|["cpe:2.3:a:qnx:rtos:6.1.0:*:*:*:*:*:*:*"]|||unknown|
192141|CVE-2002-2042|rtos|nvd:cpe||= 4.25 || = 6.1.0|unknown|["cpe:2.3:a:qnx:rtos:4.25:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.1.0:*:*:*:*:*:*:*"]|||unknown|
192179|CVE-2002-2120|rtos|nvd:cpe||= 4.25|unknown|["cpe:2.3:a:qnx:rtos:4.25:*:*:*:*:*:*:*"]|||unknown|
194609|CVE-2005-1528|rtos|nvd:cpe||= 6.2.1|unknown|["cpe:2.3:a:qnx:rtos:6.2.1:*:*:*:*:*:*:*"]|||unknown|
195735|CVE-2005-3928|rtos|nvd:cpe||= 6.3.0 || = 6.2.1|unknown|["cpe:2.3:a:qnx:rtos:6.3.0:*:*:*:*:*:*:*","cpe:2.3:a:qnx:rtos:6.2.1:*:*:*:*:*:*:*"]|||unknown|
196544|CVE-2006-0619|rtos|nvd:cpe||= 6.3.0|unknown|["cpe:2.3:a:qnx:rtos:6.3.0:*:*:*:*:*:*:*"]|||unknown|
196545|CVE-2006-0621|rtos|nvd:cpe||= 6.2.0|unknown|["cpe:2.3:a:qnx:rtos:6.2.0:*:*:*:*:*:*:*"]|||unknown|
196546|CVE-2006-0622|rtos|nvd:cpe||= 6.3.0|unknown|["cpe:2.3:a:qnx:rtos:6.3.0:*:*:*:*:*:*:*"]|||unknown|
196547|CVE-2006-0623|rtos|nvd:cpe||= 6.3.0|unknown|["cpe:2.3:a:qnx:rtos:6.3.0:*:*:*:*:*:*:*"]|||unknown|

The percent sign % wildcard matches any sequence of zero or more characters.

select * from vulnerability where package_name like "%rtos%";

...
175516|CVE-2018-16523|freertos|nvd:cpe||<= 10.0.1|unknown|["cpe:2.3:a:amazon:freertos:*:*:*:*:*:*:*:*"]|||unknown|

...

## vulnerability_metadata

PRAGMA table_info(vulnerability_metadata);
0|id|TEXT|0||1
1|namespace|TEXT|0||2
2|data_source|TEXT|0||0
3|record_source|TEXT|0||0
4|severity|TEXT|0||0
5|urls|TEXT|0|null|0
6|description|TEXT|0||0
7|cvss|TEXT|0|null|0

SELECT * from vulnerability_metadata LIMIT 5;
GHSA-3v43-877x-qgmq|github:language:php|https://github.com/advisories/GHSA-3v43-877x-qgmq|github:github:composer|Medium|["https://github.com/advisories/GHSA-3v43-877x-qgmq"]|Moderate severity vulnerability that affects league/commonmark|[]
GHSA-g4m9-5hpf-hx72|github:language:php|https://github.com/advisories/GHSA-g4m9-5hpf-hx72|github:github:composer|High|["https://github.com/advisories/GHSA-g4m9-5hpf-hx72"]|Firewall configured with unanimous strategy was not actually unanimous in Symfony|[]


