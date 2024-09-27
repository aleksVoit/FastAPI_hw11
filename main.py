from fastapi import FastAPI
from src.routes import contacts, auth
import uvicorn

app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')


@app.get('/')
def read_root():
    return {'message': 'Hello World!'}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, reload=True)

