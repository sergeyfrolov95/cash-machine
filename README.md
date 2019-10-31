# cash-machine

This is cash machine application based on web.

There is test data available:
1. Card number: 1111-1111-1111-1111, PIN: 2222
2. Card number: 2222-2222-2222-2222, PIN: 3333

Application stores PIN codes in postgres DB as md5 hash. After successful authorization user gets JWT-token for further operations. Token validity period is 2 minutes. After that user have to log in again. 
