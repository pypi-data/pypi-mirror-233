Example how to generate verification string for your domain

```python
from verifyaname.verification_string import generate_verification_string

DOMAIN = "fetch-ai.com"
WALLET_ADDRESS = "fetchabc"

# Generate verification string for Alice
verification_string = generate_verification_string(
    domain=DOMAIN, address=WALLET_ADDRESS
)
```

This string needs to be stored to domain DNS TXT record under key `fetch-ans-token=`
