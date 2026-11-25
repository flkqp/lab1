from fastapi import FastAPI
from uvicorn import run

from src.routers import post_router, user_router


app = FastAPI(
    title='My Blog API',
    description='API для управления публикациями и пользователями',
    version='3.0.0',
)

app.include_router(post_router)
app.include_router(user_router)


@app.get('/')
async def hello_world():
    return {'message': 'Привет, мир!'}


@app.get('/about')
async def about_page():
    return {'name': 'Мой блог', 'version': '3.0'}


def main():
    run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()