"""
Analytics endpoints for usage tracking.
"""

from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.analytics import AnalyticsEvent
from app.schemas.analytics import (
    AnalyticsEventCreate,
    AnalyticsEventResponse,
    AnalyticsStatsResponse,
)

router = APIRouter()


@router.post("", response_model=AnalyticsEventResponse, status_code=201)
async def create_analytics_event(
    event: AnalyticsEventCreate, request: Request, db: AsyncSession = Depends(get_db)
):
    """
    Track an analytics event.

    Records user interaction events for analytics and monitoring.
    """
    try:
        # Extract request metadata
        client_host = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        referrer = request.headers.get("referer")

        # Create analytics event
        db_event = AnalyticsEvent(
            event_name=event.name,
            session_id=event.session_id,
            user_id=event.user_id,
            timestamp=event.timestamp,
            properties=event.properties,
            ip_address=client_host,
            user_agent=user_agent,
            referrer=referrer,
        )

        db.add(db_event)
        await db.commit()
        await db.refresh(db_event)

        return AnalyticsEventResponse(
            id=str(db_event.id),
            event_name=db_event.event_name,
            session_id=db_event.session_id,
            timestamp=db_event.timestamp,
            created_at=db_event.created_at,
        )

    except Exception as e:
        await db.rollback()
        # Don't fail the request for analytics errors
        raise HTTPException(
            status_code=500, detail=f"Failed to record analytics event: {str(e)}"
        )


@router.get("/stats", response_model=AnalyticsStatsResponse)
async def get_analytics_stats(days: int = 7, db: AsyncSession = Depends(get_db)):
    """
    Get analytics statistics.

    Returns aggregated usage metrics for the specified time period.
    """
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        start_timestamp = int(start_date.timestamp() * 1000)

        # Total unique sessions
        sessions_query = select(
            func.count(func.distinct(AnalyticsEvent.session_id))
        ).where(AnalyticsEvent.timestamp >= start_timestamp)
        sessions_result = await db.execute(sessions_query)
        total_sessions = sessions_result.scalar() or 0

        # Total events
        events_query = select(func.count(AnalyticsEvent.id)).where(
            AnalyticsEvent.timestamp >= start_timestamp
        )
        events_result = await db.execute(events_query)
        total_events = events_result.scalar() or 0

        # Total analyses (analyze_submit events)
        analyses_query = select(func.count(AnalyticsEvent.id)).where(
            AnalyticsEvent.timestamp >= start_timestamp,
            AnalyticsEvent.event_name == "analyze_submit",
        )
        analyses_result = await db.execute(analyses_query)
        total_analyses = analyses_result.scalar() or 0

        # Success rate (analyze_success / analyze_submit)
        success_query = select(func.count(AnalyticsEvent.id)).where(
            AnalyticsEvent.timestamp >= start_timestamp,
            AnalyticsEvent.event_name == "analyze_success",
        )
        success_result = await db.execute(success_query)
        total_successes = success_result.scalar() or 0
        success_rate = total_successes / total_analyses if total_analyses > 0 else 0.0

        # Top events
        top_events_query = (
            select(
                AnalyticsEvent.event_name, func.count(AnalyticsEvent.id).label("count")
            )
            .where(AnalyticsEvent.timestamp >= start_timestamp)
            .group_by(AnalyticsEvent.event_name)
            .order_by(func.count(AnalyticsEvent.id).desc())
            .limit(10)
        )
        top_events_result = await db.execute(top_events_query)
        top_events = [
            {"name": row.event_name, "count": row.count}
            for row in top_events_result.fetchall()
        ]

        # Recent activity (last 10 events)
        recent_query = (
            select(AnalyticsEvent)
            .where(AnalyticsEvent.timestamp >= start_timestamp)
            .order_by(AnalyticsEvent.timestamp.desc())
            .limit(10)
        )
        recent_result = await db.execute(recent_query)
        recent_events = recent_result.scalars().all()

        recent_activity = [
            AnalyticsEventResponse(
                id=str(event.id),
                event_name=event.event_name,
                session_id=event.session_id,
                timestamp=event.timestamp,
                created_at=event.created_at,
            )
            for event in recent_events
        ]

        return AnalyticsStatsResponse(
            total_sessions=total_sessions,
            total_events=total_events,
            total_analyses=total_analyses,
            success_rate=success_rate,
            top_events=top_events,
            recent_activity=recent_activity,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve analytics: {str(e)}"
        )
