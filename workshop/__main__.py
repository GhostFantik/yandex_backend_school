import uvicorn

uvicorn.run(
    'workshop.app:app',
    reload=False,
    host='0.0.0.0'
)
