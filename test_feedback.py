#!/usr/bin/env python3
"""
Quick test for feedback collection endpoint.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
from datetime import datetime
from app.schemas.feedback import MeterFeedback, FeedbackResponse
from app.api.v1.endpoints.feedback import submit_meter_feedback, get_meter_feedback_stats

async def test_feedback():
    """Test feedback submission."""

    print("=" * 70)
    print("FEEDBACK COLLECTION TEST")
    print("=" * 70)

    # Create test feedback (user corrects الرجز to الطويل)
    feedback = MeterFeedback(
        text="قفا نبك من ذكرى حبيب ومنزل",
        normalized_text="قفا نبك من ذكري حبيب ومنزل",
        detected_meter="الرجز",
        detected_confidence=0.9581,
        user_selected_meter="الطويل",
        alternatives_shown=["الرجز", "الطويل", "السريع"],
        has_tashkeel=False,
        user_comment="This is the famous Mu'allaqah verse by Imru' al-Qais",
        timestamp=datetime.now()
    )

    print("\nSubmitting feedback:")
    print(f"  Text: {feedback.text}")
    print(f"  Detected: {feedback.detected_meter} ({feedback.detected_confidence:.2%})")
    print(f"  User selected: {feedback.user_selected_meter}")
    print(f"  Comment: {feedback.user_comment}")
    print()

    # Submit feedback
    try:
        response = await submit_meter_feedback(feedback)
        print("✓ Feedback submitted successfully!")
        print(f"  Status: {response.status}")
        print(f"  Message: {response.message}")
        print(f"  Feedback ID: {response.feedback_id}")
    except Exception as e:
        print(f"✗ Failed to submit feedback: {e}")
        return

    # Submit another feedback (validation - user agrees with detection)
    print("\n" + "-" * 70)
    print("Submitting validation feedback (user agrees):")

    feedback2 = MeterFeedback(
        text="أَلا لَيتَ الشَبابَ يَعودُ يَوماً",
        normalized_text="ألا ليت الشباب يعود يوما",
        detected_meter="الطويل",
        detected_confidence=0.97,
        user_selected_meter="الطويل",  # Same as detected
        alternatives_shown=["الطويل"],
        has_tashkeel=True,
        user_comment="Detection is correct",
        timestamp=datetime.now()
    )

    try:
        response2 = await submit_meter_feedback(feedback2)
        print("✓ Validation feedback submitted!")
        print(f"  Feedback ID: {response2.feedback_id}")
    except Exception as e:
        print(f"✗ Failed to submit feedback: {e}")

    # Get statistics
    print("\n" + "=" * 70)
    print("FEEDBACK STATISTICS")
    print("=" * 70)

    try:
        stats = await get_meter_feedback_stats()
        print(f"\nTotal feedback: {stats.get('total_feedback', 0)}")
        print(f"Corrections: {stats.get('corrections', 0)}")
        print(f"Validations: {stats.get('validations', 0)}")
        print(f"Correction rate: {stats.get('correction_rate', 0)}%")

        if stats.get('most_corrected_meters'):
            print("\nMost corrected meters:")
            for item in stats['most_corrected_meters']:
                print(f"  - {item['meter']}: {item['count']} times")

        if stats.get('confused_pairs'):
            print("\nMost confused meter pairs:")
            for item in stats['confused_pairs']:
                print(f"  - {item['pair']}: {item['count']} times")

    except Exception as e:
        print(f"✗ Failed to get stats: {e}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_feedback())
