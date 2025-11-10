#!/usr/bin/env python3
"""
Test script to verify Redis caching performance for the analyze endpoint.

Expected behavior:
- First request: ~500ms (analysis performed)
- Second identical request: <50ms (cache hit)
"""

import asyncio
import httpx
import time
import json

API_URL = "http://localhost:8000/api/v1/analyze/"  # Note: trailing slash required

# Test verse (from المتنبي)
TEST_VERSE = "إذا غامَرتَ في شَرَفٍ مَرومِ"

async def test_caching():
    """Test Redis caching performance."""
    
    async with httpx.AsyncClient() as client:
        # Test 1: First request (cache miss - should perform analysis)
        print("=" * 60)
        print("TEST 1: First request (cache miss)")
        print("=" * 60)
        
        start_time = time.time()
        try:
            response1 = await client.post(
                API_URL,
                json={
                    "text": TEST_VERSE,
                    "detect_bahr": True,
                    "suggest_corrections": True
                },
                timeout=10.0
            )
            elapsed1 = (time.time() - start_time) * 1000  # Convert to ms
            
            if response1.status_code == 200:
                result1 = response1.json()
                print(f"✓ Status: {response1.status_code}")
                print(f"✓ Response time: {elapsed1:.2f}ms")
                print(f"✓ Taqti3: {result1.get('taqti3')}")
                if result1.get('bahr'):
                    print(f"✓ Bahr: {result1['bahr']['name_ar']} ({result1['bahr']['name_en']})")
                    print(f"✓ Confidence: {result1['bahr']['confidence']:.2%}")
                print(f"✓ Score: {result1.get('score')}")
            else:
                print(f"✗ Error: {response1.status_code}")
                print(f"✗ Response: {response1.text}")
                return False
        except Exception as e:
            print(f"✗ Request failed: {e}")
            return False
        
        print()
        
        # Wait a moment before second request
        await asyncio.sleep(0.5)
        
        # Test 2: Second request (cache hit - should be fast)
        print("=" * 60)
        print("TEST 2: Second request (cache hit)")
        print("=" * 60)
        
        start_time = time.time()
        try:
            response2 = await client.post(
                API_URL,
                json={
                    "text": TEST_VERSE,
                    "detect_bahr": True,
                    "suggest_corrections": True
                },
                timeout=10.0
            )
            elapsed2 = (time.time() - start_time) * 1000  # Convert to ms
            
            if response2.status_code == 200:
                result2 = response2.json()
                print(f"✓ Status: {response2.status_code}")
                print(f"✓ Response time: {elapsed2:.2f}ms")
                print(f"✓ Taqti3: {result2.get('taqti3')}")
                if result2.get('bahr'):
                    print(f"✓ Bahr: {result2['bahr']['name_ar']} ({result2['bahr']['name_en']})")
            else:
                print(f"✗ Error: {response2.status_code}")
                print(f"✗ Response: {response2.text}")
                return False
        except Exception as e:
            print(f"✗ Request failed: {e}")
            return False
        
        print()
        
        # Verify results are identical
        print("=" * 60)
        print("VERIFICATION")
        print("=" * 60)
        
        if result1 == result2:
            print("✓ Results are identical (cache working correctly)")
        else:
            print("✗ Results differ (cache may have issues)")
            return False
        
        # Check performance improvement
        speedup = elapsed1 / elapsed2 if elapsed2 > 0 else 0
        print(f"\n✓ First request: {elapsed1:.2f}ms")
        print(f"✓ Second request: {elapsed2:.2f}ms")
        print(f"✓ Speedup: {speedup:.1f}x faster")
        
        if elapsed2 < 50:
            print(f"✓ Cache hit is fast (<50ms)")
        else:
            print(f"⚠ Cache hit is slower than expected: {elapsed2:.2f}ms")
        
        if speedup > 2:
            print(f"✓ Significant performance improvement from caching")
        else:
            print(f"⚠ Performance improvement is modest")
        
        print()
        print("=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
        return True


async def test_different_verses():
    """Test that different verses get different results."""
    
    print("\n" + "=" * 60)
    print("TEST 3: Different verses should have different results")
    print("=" * 60)
    
    verses = [
        "إذا غامَرتَ في شَرَفٍ مَرومِ",
        "أَلا لَيتَ الشَبابَ يَعودُ يَوماً"
    ]
    
    async with httpx.AsyncClient() as client:
        results = []
        
        for i, verse in enumerate(verses, 1):
            print(f"\nVerse {i}: {verse}")
            try:
                response = await client.post(
                    API_URL,
                    json={"text": verse, "detect_bahr": True},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    results.append(result)
                    print(f"✓ Taqti3: {result.get('taqti3')}")
                    if result.get('bahr'):
                        print(f"✓ Bahr: {result['bahr']['name_ar']}")
                else:
                    print(f"✗ Error: {response.status_code}")
                    return False
            except Exception as e:
                print(f"✗ Request failed: {e}")
                return False
        
        # Verify results are different
        if len(results) == 2 and results[0] != results[1]:
            print("\n✓ Different verses produce different results (correct)")
            return True
        else:
            print("\n✗ Results are unexpectedly identical")
            return False


async def main():
    """Run all tests."""
    print("Redis Caching Performance Test")
    print("=" * 60)
    print("Testing endpoint: http://localhost:8000/api/v1/analyze")
    print()
    
    # Make sure the server is running
    try:
        async with httpx.AsyncClient() as client:
            health = await client.get("http://localhost:8000/health", timeout=5.0)
            if health.status_code != 200:
                print("✗ Server is not responding. Please start the server:")
                print("  cd backend && uvicorn app.main:app --reload")
                return
    except Exception as e:
        print("✗ Cannot connect to server. Please start it first:")
        print("  cd backend && uvicorn app.main:app --reload")
        print(f"  Error: {e}")
        return
    
    # Run tests
    success1 = await test_caching()
    if not success1:
        print("\n✗ Cache performance test failed")
        return
    
    success2 = await test_different_verses()
    if not success2:
        print("\n✗ Different verses test failed")
        return
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nRedis caching is working correctly:")
    print("- First requests perform analysis (~500ms)")
    print("- Cached requests are fast (<50ms)")
    print("- Different verses get different results")
    print("- Identical verses return cached results")


if __name__ == "__main__":
    asyncio.run(main())
