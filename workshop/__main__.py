import uvicorn

uvicorn.run(
    'workshop.app:app',
    reload=False,
)
