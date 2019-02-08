CREATE OR REPLACE FUNCTION write_to_s3() RETURNS integer AS '$libdir/gps3ext.so', 's3_export' LANGUAGE C STABLE;
CREATE OR REPLACE FUNCTION read_from_s3() RETURNS integer AS '$libdir/gps3ext.so', 's3_import' LANGUAGE C STABLE;
DROP PROTOCOL s3 CASCADE;
CREATE PROTOCOL s3 (writefunc = write_to_s3, readfunc = read_from_s3);