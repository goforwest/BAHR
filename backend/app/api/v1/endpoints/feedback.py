"""
Feedback collection endpoints.

This module provides endpoints for collecting user feedback on:
- Meter detection accuracy
- Correction suggestions
- General feedback on the system

The feedback is stored in JSONL format for later analysis and model improvement.
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from app.schemas.feedback import MeterFeedback, FeedbackResponse

logger = logging.getLogger(__name__)

router = APIRouter()

# Feedback storage location
FEEDBACK_DIR = Path("data/feedback")
METER_FEEDBACK_FILE = FEEDBACK_DIR / "meter_feedback.jsonl"


def ensure_feedback_dir():
    """Ensure feedback directory exists."""
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Feedback directory ensured: {FEEDBACK_DIR}")


@router.post(
    "/meter",
    response_model=FeedbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit meter detection feedback",
    description="""
    Collect user feedback on meter detection accuracy.

    **Use cases:**
    - User selects a different meter than what was detected (correction)
    - User confirms the detected meter was correct (validation)
    - User provides additional context or comments

    **Data usage:**
    This data helps improve the system by:
    1. Identifying problematic verses or patterns
    2. Training future ML models
    3. Improving detection rules and heuristics
    4. Understanding confusion patterns (e.g., الطويل vs الرجز)

    **Privacy:**
    - Feedback is stored locally in JSONL format
    - No personally identifiable information is collected
    - Timestamps are used only for deduplication and analysis
    """,
    responses={
        200: {
            "description": "Feedback submitted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "شكراً لملاحظاتك! | Thank you for your feedback!",
                        "feedback_id": "fb_1731409800"
                    }
                }
            }
        },
        400: {"description": "Invalid input"},
        500: {"description": "Server error during feedback storage"}
    }
)
async def submit_meter_feedback(feedback: MeterFeedback) -> FeedbackResponse:
    """
    Submit feedback on meter detection.

    Args:
        feedback: MeterFeedback object with detection results and user selection

    Returns:
        FeedbackResponse with success status and feedback ID

    Raises:
        HTTPException: 400 for invalid input, 500 for storage errors
    """
    try:
        # Ensure feedback directory exists
        ensure_feedback_dir()

        # Convert feedback to dict for storage
        feedback_dict = feedback.model_dump()

        # Convert datetime to ISO format string for JSON serialization
        if isinstance(feedback_dict.get('timestamp'), datetime):
            feedback_dict['timestamp'] = feedback_dict['timestamp'].isoformat()

        # Generate unique feedback ID (timestamp-based)
        feedback_id = f"fb_{int(datetime.now().timestamp())}"
        feedback_dict['feedback_id'] = feedback_id

        # Append to JSONL file (one JSON object per line)
        with open(METER_FEEDBACK_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback_dict, ensure_ascii=False) + '\n')

        logger.info(
            f"Feedback submitted: {feedback_id} | "
            f"Detected: {feedback.detected_meter} ({feedback.detected_confidence:.2%}), "
            f"User selected: {feedback.user_selected_meter}"
        )

        # Check if this is a correction or validation
        is_correction = feedback.detected_meter != feedback.user_selected_meter

        if is_correction:
            logger.info(
                f"CORRECTION: User corrected {feedback.detected_meter} → {feedback.user_selected_meter} "
                f"for text: {feedback.text[:50]}..."
            )

        return FeedbackResponse(
            status="success",
            message="شكراً لملاحظاتك! | Thank you for your feedback!",
            feedback_id=feedback_id
        )

    except ValueError as e:
        logger.error(f"Invalid feedback data: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid feedback data: {str(e)}"
        )
    except IOError as e:
        logger.error(f"Failed to write feedback to file: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save feedback. Please try again."
        )
    except Exception as e:
        logger.error(f"Unexpected error during feedback submission: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )


@router.get(
    "/meter/stats",
    summary="Get meter feedback statistics",
    description="""
    Get aggregated statistics about meter detection feedback.

    **Returns:**
    - Total feedback count
    - Correction rate (% of times users corrected the detection)
    - Most corrected meters
    - Most confused meter pairs (e.g., الطويل ↔ الرجز)

    **Note:** This endpoint is for internal use/monitoring.
    """
)
async def get_meter_feedback_stats():
    """
    Get aggregated statistics from meter feedback.

    Returns:
        Dictionary with feedback statistics

    Raises:
        HTTPException: 500 if unable to read feedback file
    """
    try:
        if not METER_FEEDBACK_FILE.exists():
            return {
                "total_feedback": 0,
                "correction_rate": 0.0,
                "most_corrected_meters": [],
                "confused_pairs": [],
                "message": "No feedback data available yet"
            }

        # Read all feedback
        feedbacks = []
        with open(METER_FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    feedbacks.append(json.loads(line))

        total = len(feedbacks)
        corrections = sum(
            1 for fb in feedbacks
            if fb.get('detected_meter') != fb.get('user_selected_meter')
        )

        correction_rate = (corrections / total * 100) if total > 0 else 0.0

        # Count corrections by meter
        correction_counts = {}
        for fb in feedbacks:
            if fb.get('detected_meter') != fb.get('user_selected_meter'):
                detected = fb.get('detected_meter', 'unknown')
                correction_counts[detected] = correction_counts.get(detected, 0) + 1

        most_corrected = sorted(
            correction_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # Find confused pairs (A detected as B, or B detected as A)
        pair_counts = {}
        for fb in feedbacks:
            detected = fb.get('detected_meter')
            selected = fb.get('user_selected_meter')
            if detected and selected and detected != selected:
                # Normalize pair order (alphabetically) to avoid duplicates
                pair = tuple(sorted([detected, selected]))
                pair_counts[pair] = pair_counts.get(pair, 0) + 1

        confused_pairs = sorted(
            [(f"{p[0]} ↔ {p[1]}", count) for p, count in pair_counts.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            "total_feedback": total,
            "corrections": corrections,
            "validations": total - corrections,
            "correction_rate": round(correction_rate, 2),
            "most_corrected_meters": [
                {"meter": meter, "count": count}
                for meter, count in most_corrected
            ],
            "confused_pairs": [
                {"pair": pair, "count": count}
                for pair, count in confused_pairs
            ]
        }

    except Exception as e:
        logger.error(f"Failed to get feedback stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve feedback statistics"
        )
