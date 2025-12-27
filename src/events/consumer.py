import asyncio
import asyncpg


CREATE_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION notify_outbox_event()
RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('outbox_channel', NEW.id::text);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

CREATE_TRIGGER_SQL = """
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'outbox_notify'
    ) THEN
        CREATE TRIGGER outbox_notify
        AFTER INSERT ON outbox_events
        FOR EACH ROW
        EXECUTE FUNCTION notify_outbox_event();
    END IF;
END;
$$;
"""


async def setup_trigger(pool):
    async with pool.acquire() as conn:
        await conn.execute(CREATE_FUNCTION_SQL)
        await conn.execute(CREATE_TRIGGER_SQL)
