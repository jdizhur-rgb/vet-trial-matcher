# Production receipt correction

The release2 retry helper reused a raw filename from release1. When curl failed before writing a new file, it could read the old successful payload and attach its bytes/hash to the new failure timestamp. The failed request still retained exit28/HTTP000 and overall NOT VERIFIED; it was never a successful production result. Source traversal evidence is unaffected because run.py always uses a timestamp-derived unique raw filename.

Corrected readback.py and retry-production.py to use a unique path for every actual request. The release2 failed catalog retry is marked no fresh payload; release1 successful catalog hash remains valid only at its original04:33 timestamp. One final bounded post-deploy readback is performed with the corrected helper; no source traversal is repeated. Old attempt timestamps/results are retained, not converted into successes.
