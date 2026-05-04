# Session Log - 2026-05-04

## Task: Audit Database & Web Page (Final Deep Dive)
David requested a fix for 'brand_model' column errors appearing in 'audit_entries'.

### Solution implemented:
- Validated that `schema_v4.sql` is correct: `brand_model` exists ONLY in `devices`.
- Created `index_v5.html`: Refactored the submission logic to use a two-step process. 
  1. `upsert` to `devices` (includes brand_model).
  2. `insert` to `audit_entries` (strictly excludes brand_model).
- Provided `schema_sync.sql` to drop legacy columns from `audit_entries` if they were added during debugging attempts.
- Created error handling in the UI to capture and display PostgREST errors.

### Next Steps:
- User to apply `schema_sync.sql` in Supabase SQL editor.
- User to test `index_v5.html`.













