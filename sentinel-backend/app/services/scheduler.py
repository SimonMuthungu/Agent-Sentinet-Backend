from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.persistence.db import supabase
from app.agents.graph_runner import run_vendor_evaluation

scheduler = AsyncIOScheduler()

async def scheduled_vendor_scan():
    vendors = supabase.table("vendors").select("id").execute().data
    for v in vendors:
        await run_vendor_evaluation(
            vendor_id=v["id"],
            query="Scheduled compliance re-evaluation"
        )

def start_scheduler():
    scheduler.add_job(
        scheduled_vendor_scan,
        trigger="cron",
        hour=2,   # nightly
    )
    scheduler.start()
