import hashlib, hmac

def universal_sign(path, query, expiry, body, secret):
    # Manifold String: Standardizes any signing sequence
    s = f"{path}{query}{expiry}{body}"
    return hmac.new(secret.encode(), s.encode(), hashlib.sha256).hexdigest()

secret = "REDACTED_CORE_SECRET"

# Vector 1: Standard Manifold
path, query, expiry, body = "/api/v1/action", "", "1740540000", '{"amount":1}'
sig1 = universal_sign(path, query, expiry, body, secret)

# Vector 2: Warped Manifold (Testing for Logic Fractures)
# Shifting bytes between variables to test for collision
expiry2, body2 = "174054000", '0{"amount":1}'
sig2 = universal_sign(path, query, expiry2, body2, secret)

print(f"Sig 1: {sig1}")
print(f"Sig 2: {sig2}")
print(f"Collision: {sig1 == sig2}") # If True, God-Mode is active