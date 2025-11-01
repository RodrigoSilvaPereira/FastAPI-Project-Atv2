from fastapi import FastAPI
from app.routes.students import router as students_router

app = FastAPI(title="AT1 - FastAPI Demo")

app.include_router(students_router)


@app.get("/")
async def root():
    return {
        "message": """API rodando. Próximo passo: rotas de alunos.
            /students/ping para verificar."""
    }
