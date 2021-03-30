from workshop.settings import settings
import uvicorn

uvicorn.run(
    'workshop.app:app',
    reload=False,
    host='0.0.0.0',
    workers=int(settings.workers)
)
