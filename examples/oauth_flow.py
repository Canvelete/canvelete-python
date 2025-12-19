"""
OAuth2 Flow Example
Demonstrates user authentication using OAuth2.
"""

import os
from canvelete import CanveleteClient

def main():
    # Initialize client with OAuth2 credentials
    client_id = os.getenv("CANVELETE_CLIENT_ID", "your_client_id")
    client_secret = os.getenv("CANVELETE_CLIENT_SECRET", "your_client_secret")
    
    client = CanveleteClient(
        client_id=client_id,
        client_secret=client_secret,
    )
    
    print("Canvelete OAuth2 Authentication Example\n")
    
    # Authenticate (will open browser)
    print("Starting OAuth2 flow...")
    print("Your browser will open for authorization.")
    print("After authorizing, return to this terminal.\n")
    
    try:
        token_data = client.authenticate()
        print("✓ Successfully authenticated!")
        print(f"  Access token expires in: {token_data.get('expires_in')} seconds")
        print(f"  Scopes: {token_data.get('scope')}\n")
        
        # Now you can make API calls
        print("Fetching your designs...")
        designs_response = client.designs.list(limit=5)
        designs = designs_response.get("data", [])
        print(f"✓ Found {len(designs)} designs")
        
        for design in designs:
            print(f"  - {design['name']}")
        
        # Token will be automatically stored and reused
        print("\n💡 Your tokens have been saved.")
        print("Next time you run this, you won't need to authenticate again")
        print("(unless the tokens have expired).")
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return
    
    print("\n✅ OAuth2 flow complete!")


if __name__ == "__main__":
    main()
