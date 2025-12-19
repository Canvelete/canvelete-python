"""
Quickstart example for Canvelete Python SDK
Demonstrates basic usage with API key authentication.
"""

import os
from canvelete import CanveleteClient

def main():
    # Initialize client with API key
    api_key = os.getenv("CANVELETE_API_KEY", "cvt_your_api_key_here")
    client = CanveleteClient(api_key=api_key)
    
    print("Canvelete Python SDK Quickstart\n")
    
    # List existing designs
    print("Fetching your designs...")
    designs_response = client.designs.list(limit=5)
    designs = designs_response.get("data", [])
    print(f"✓ Found {len(designs)} designs")
    
    for design in designs:
        print(f"  - {design['name']} (ID: {design['id']})")
    
    # Create a new design
    print("\nCreating a new design...")
    canvas_data = {
        "elements": [
            {
                "type": "text",
                "text": "Hello from Canvelete SDK!",
                "x": 100,
                "y": 100,
                "fontSize": 48,
                "fontFamily": "Arial",
                "fill": "#000000",
            },
            {
                "type": "text",
                "text": "This design was created using the Python SDK",
                "x": 100,
                "y": 180,
                "fontSize": 24,
                "fontFamily": "Arial",
                "fill": "#666666",
            }
        ],
        "background": "#FFFFFF",
    }
    
    new_design = client.designs.create(
        name="SDK Test Design",
        description="Created via Python SDK quickstart",
        canvas_data=canvas_data,
        width=1920,
        height=1080,
    )
    
    print(f"✓ Created design: {new_design['name']} (ID: {new_design['id']})")
    
    # Render the design
    print("\nRendering design to PNG...")
    output_file = "quickstart_output.png"
    
    image_data = client.render.create(
        design_id=new_design["id"],
        format="png",
        quality=90,
        output_file=output_file,
    )
    
    print(f"✓ Rendered and saved to {output_file}")
    print(f"  File size: {len(image_data) / 1024:.2f} KB")
    
    # List templates
    print("\nFetching available templates...")
    templates_response = client.templates.list(limit=5)
    templates = templates_response.get("data", [])
    print(f"✓ Found {len(templates)} templates")
    
    for template in templates[:3]:
        print(f"  - {template['name']}")
    
    print("\n✅ Quickstart complete!")
    print(f"\nNext steps:")
    print("  1. View your design at: https://www.canvelete.com/dashboard")
    print(f"  2. Check the rendered image: {output_file}")
    print("  3. Explore more examples in the examples/ directory")


if __name__ == "__main__":
    main()
