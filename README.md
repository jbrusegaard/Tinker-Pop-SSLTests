# TinkerPop-SSLTests
Test for SSL connection to tinkerpop

`docker compose up`

Run either:

`python3 testConnectStandardSSL.py`
  - Test a "standard" SSL approach using only a cert the server can validate.

`python3 testConnectValidateChainSSL.py`
  - Test connecting, but also verify the cert chain before doing so.
