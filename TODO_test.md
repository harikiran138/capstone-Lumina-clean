# TODO: Fix Failing Tests and Deprecation Warnings

## Step 1: Fix Path Resolution Issues ✅
- [x] Update file paths in test files from "app/sample_data/documents.txt" to "backend/app/sample_data/documents.txt"
- [x] Files updated:
  - backend/tests/test_ingest.py
  - backend/tests/test_query.py
  - backend/tests/test_integration.py

## Step 2: Fix /ingest + /query Combined Test (400 Bad Request)
- [x] Added error handling in ingest and query endpoints to catch exceptions
- [ ] Test is currently running to identify the exact error
- [ ] If 500 error with details, fix the underlying service issue

## Step 3: Fix Deprecation Warnings ✅
- [x] Update Pydantic Config to v2 style in backend/config/settings.py
- [x] Check and update any deprecated FAISS usage
- [x] No deprecated FAISS usage found

## Step 4: Future Improvements
- [ ] Add end-to-end test
- [ ] Add performance test
