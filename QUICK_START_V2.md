# Canvelete Python SDK v2.0 - Quick Start Guide

## Installation

```bash
pip install canvelete
```

## Basic Usage

### Initialize Client

```python
from canvelete import CanveleteClient

client = CanveleteClient(api_key="cvt_your_api_key")
```

## New Features in v2.0

### 1. Canvas Manipulation

```python
# Add text element
element = client.canvas.add_element(
    design_id="design_123",
    element={
        "type": "text",
        "text": "Hello World",
        "x": 100,
        "y": 100,
        "fontSize": 48,
        "fontFamily": "Arial"
    }
)

# Update element
client.canvas.update_element(
    design_id="design_123",
    element_id=element["id"],
    updates={"text": "Updated Text", "fontSize": 64}
)

# Delete element
client.canvas.delete_element(
    design_id="design_123",
    element_id=element["id"]
)

# Resize canvas
client.canvas.resize(
    design_id="design_123",
    width=1920,
    height=1080
)
```

### 2. Asset Management

```python
# Upload asset
asset = client.assets.upload(
    file_path="logo.png",
    name="Company Logo",
    asset_type="IMAGE"
)

# Search stock images
images = client.assets.search_stock_images(
    query="business meeting",
    per_page=10
)

# Search icons
icons = client.assets.search_icons(query="arrow")

# List fonts
fonts = client.assets.list_fonts(category="sans-serif")
```

### 3. Template Operations

```python
# Apply template with dynamic data
design = client.templates.apply(
    template_id="tmpl_123",
    name="John's Certificate",
    dynamic_data={
        "name": "John Doe",
        "date": "2024-01-01",
        "company": "Acme Corp"
    }
)

# Create template from design
template = client.templates.create(
    design_id="design_123",
    name="Certificate Template",
    category="certificates"
)
```

### 4. Async Rendering with Queue

```python
# Create async render job
job = client.render.create_async(
    design_id="design_123",
    format="pdf",
    webhook_url="https://myapp.com/webhooks/render"
)

# Check status
status = client.render.get_status(job["id"])

# Wait for completion
result = client.render.wait_for_completion(job["id"], timeout=300)
print(f"Render complete: {result['url']}")

# Batch rendering
jobs = client.render.batch_create([
    {"design_id": "design_1", "format": "png"},
    {"design_id": "design_2", "format": "pdf"},
    {"design_id": "design_3", "format": "jpg"}
])

results = client.render.wait_for_batch(jobs, timeout=600)
```

### 5. Usage Tracking

```python
# Get usage stats
stats = client.usage.get_stats()
print(f"Credits: {stats['creditsUsed']}/{stats['creditLimit']}")
print(f"API Calls: {stats['apiCalls']}/{stats['apiCallLimit']}")

# Get usage history
from datetime import datetime, timedelta

history = client.usage.get_history(
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now()
)

# Get analytics
analytics = client.usage.get_analytics(period="month")
```

### 6. Billing Management

```python
# Get billing info
billing = client.billing.get_info()
print(f"Plan: {billing['plan']}")
print(f"Next billing: {billing['nextBillingDate']}")

# Get invoices
invoices = client.billing.get_invoices()

# Purchase credits
purchase = client.billing.purchase_credits(amount=5000)

# Manage team seats
seats = client.billing.get_seats()
client.billing.add_seats(count=5)
```

## Utilities

### Retry Logic

```python
from canvelete.utils import with_retry
from canvelete.exceptions import RateLimitError, ServerError

@with_retry(
    max_attempts=5,
    backoff_factor=2,
    retry_on=(RateLimitError, ServerError)
)
def make_api_call():
    return client.designs.list()

# Automatic retry with exponential backoff
designs = make_api_call()
```

### Webhook Handling

```python
from canvelete.utils import WebhookHandler
from flask import Flask, request

app = Flask(__name__)
handler = WebhookHandler(secret="your_webhook_secret")

@app.route("/webhooks/canvelete", methods=["POST"])
def handle_webhook():
    signature = request.headers.get("X-Canvelete-Signature")
    
    # Verify and parse in one step
    try:
        event = handler.construct_event(
            request.data,
            signature,
            request.headers.get("X-Canvelete-Timestamp")
        )
        
        if event.type == "render.completed":
            print(f"Render completed: {event.data['url']}")
        elif event.type == "render.failed":
            print(f"Render failed: {event.data['error']}")
        
        return "OK", 200
    except ValueError:
        return "Invalid signature", 401
```

### Element Validation

```python
from canvelete.utils import validate_element

element = {
    "type": "text",
    "text": "Hello",
    "x": 100,
    "y": 100,
    "fontSize": 24,
    "fontFamily": "Arial"
}

errors = validate_element(element)
if errors:
    print(f"Validation errors: {errors}")
else:
    client.canvas.add_element(design_id, element)
```

## Complete Example

```python
from canvelete import CanveleteClient
from canvelete.utils import with_retry, validate_element

# Initialize
client = CanveleteClient(api_key="cvt_your_key")

# Create design
design = client.designs.create(
    name="Marketing Banner",
    canvas_data={"elements": []},
    width=1920,
    height=1080
)

# Add background
client.canvas.update_background(
    design_id=design["id"],
    background="#FFFFFF"
)

# Search and add stock image
images = client.assets.search_stock_images("technology", per_page=1)
if images["data"]:
    image_element = {
        "type": "image",
        "src": images["data"][0]["largeImageURL"],
        "x": 0,
        "y": 0,
        "width": 1920,
        "height": 1080,
        "objectFit": "cover"
    }
    
    errors = validate_element(image_element)
    if not errors:
        client.canvas.add_element(design["id"], image_element)

# Add text overlay
text_element = {
    "type": "text",
    "text": "Innovation Starts Here",
    "x": 100,
    "y": 500,
    "fontSize": 72,
    "fontFamily": "Arial",
    "fontWeight": "bold",
    "fill": "#FFFFFF",
    "textShadowX": 2,
    "textShadowY": 2,
    "textShadowBlur": 4,
    "textShadowColor": "rgba(0,0,0,0.5)"
}

client.canvas.add_element(design["id"], text_element)

# Render with retry
@with_retry(max_attempts=3)
def render():
    return client.render.create(
        design_id=design["id"],
        format="png",
        quality=100,
        output_file="banner.png"
    )

render()

# Check usage
stats = client.usage.get_stats()
print(f"Credits remaining: {stats['creditsRemaining']}")
```

## Migration from v1.0

All v1.0 code continues to work. New features are additive:

```python
# v1.0 code still works
designs = client.designs.list()
design = client.designs.create(name="Test", canvas_data={})
image = client.render.create(design_id=design["id"])

# v2.0 adds new capabilities
client.canvas.add_element(design["id"], element)
client.assets.search_stock_images("business")
client.usage.get_stats()
```

## Error Handling

```python
from canvelete.exceptions import (
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    InsufficientCreditsError
)

try:
    design = client.designs.get("invalid_id")
except NotFoundError:
    print("Design not found")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except InsufficientCreditsError:
    print("Out of credits. Please upgrade.")
```

## Support

- **Documentation**: https://docs.canvelete.com
- **API Reference**: https://docs.canvelete.com/api
- **GitHub**: https://github.com/canvelete/canvelete-python
- **Email**: support@canvelete.com
