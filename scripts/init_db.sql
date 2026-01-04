-- Database Initialization Script
-- Execute these commands in a superuser session (e.g., via DBeaver connected as 'postgres' or CLI 'psql')

-- ============================================================================
-- 1. DEVELOPMENT ENVIRONMENT (caramello_dev)
-- ============================================================================

-- Create the user (if not exists)
-- DROP USER IF EXISTS caramello_user_dev;
CREATE USER caramello_user_dev WITH PASSWORD 'changeme';

-- Create the database with the user as owner
-- This ensures the user has full control over the DB.
-- DROP DATABASE IF EXISTS caramello_dev;
CREATE DATABASE caramello_dev OWNER caramello_user_dev;

-- Grant Connection privileges (Redundant if Owner, but good practice)
GRANT ALL PRIVILEGES ON DATABASE caramello_dev TO caramello_user_dev;

-- CRITICAL STEP FOR POSTGRES 15+:
-- You must connect to the specific database ('caramello_dev') to grant schema privileges.
-- Run the following command AFTER connecting to 'caramello_dev':
-- GRANT ALL ON SCHEMA public TO caramello_user_dev;

-- ============================================================================
-- 2. PRODUCTION ENVIRONMENT (caramello_prod)
-- ============================================================================

-- Create the user with a strong password
CREATE USER caramello_user_prod WITH PASSWORD 'STRONG_PASSWORD_HERE';

-- Create the database
CREATE DATABASE caramello_prod OWNER caramello_user_prod;

-- Grant Connection privileges
GRANT ALL PRIVILEGES ON DATABASE caramello_prod TO caramello_user_prod;

-- Connect to 'caramello_prod' and run:
-- GRANT ALL ON SCHEMA public TO caramello_user_prod;
