from fastapi import FastAPI
from caramello.api.generated import user_router, family_router, familymember_router, familyinvitation_router

app = FastAPI(
    title="Caramello Backend",
    description="Backend API for Caramello",
    version="0.1.0",
)

# Include generated routers
app.include_router(user_router.router)
app.include_router(family_router.router)
app.include_router(familymember_router.router)
app.include_router(familyinvitation_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to Caramello API"}
