#!/usr/bin/env python
import sys
import json
from app import app, load_exams_from_file

# Test loading exams
print("Testing data loading...")
exams = load_exams_from_file()
print(f"Loaded {len(exams)} exams")

if exams:
    first = exams[0]
    print("\nFirst exam record:")
    print(json.dumps(first, indent=2, default=str, ensure_ascii=False))

# Test with Flask test client
print("\n\nTesting API endpoints...")
with app.test_client() as client:
    # Test dropdown-data
    resp = client.get('/api/dropdown-data')
    print(f"\n/api/dropdown-data: {resp.status_code}")
    data = json.loads(resp.data)
    print(f"  Success: {data.get('success')}")
    if data.get('data'):
        print(f"  Levels: {len(data['data'].get('levels', []))} items")
        print(f"  Streams: {len(data['data'].get('streams', {}))} groups")
        print(f"  Substreams: {len(data['data'].get('substreams', {}))} groups")
    
    # Test exams list
    resp = client.get('/api/exams?level=10')
    print(f"\n/api/exams?level=10: {resp.status_code}")
    data = json.loads(resp.data)
    print(f"  Status: {data.get('status')}")
    print(f"  Total: {data.get('total')}")
    if data.get('exams'):
        first = data['exams'][0]
        print(f"  First exam name: {first.get('name')}")
        print(f"  First exam fields: {list(first.keys())}")
    
    # Test exam by slug
    resp = client.get('/api/exams/cbse-(10th)')
    print(f"\n/api/exams/cbse-(10th): {resp.status_code}")
    data = json.loads(resp.data)
    print(f"  Status: {data.get('status')}")
    if data.get('exam'):
        exam = data['exam']
        print(f"  Name: {exam.get('name')}")
        print(f"  Category: {exam.get('category')}")
        print(f"  Website: {exam.get('website')}")
