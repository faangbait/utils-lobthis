# Lob This - A CLI Application to Send Postal Mail

![img](https://img.shields.io/badge/build-passable-green) This actually works pretty well! Does what it says on the tin. Doesn't do any error-handling.

## Installation
1. Create a file called secrets.py with the following information
```python 
LIVE_API_KEY="live_lobapikeygoeshere"
TEST_API_KEY="test_lobapikeygoesheretoo"
DEFAULT_FROM="Name,Address,City,ST,ZipCo"
AWS_S3_BUCKET="bucket-name-here"
TEST_SERVER_MY_ADDRESS="adr_212c98aadb7c8c40" # From Lob's API
LIVE_SERVER_MY_ADDRESS="adr_d90325af84b06a46" # From Lob's API
```

2. Debug whatever breaks.
