from container import Container
from fastapi import FastAPI



class APP:
    def __init__(self):
        self.app = FastAPI()
        self.container = Container()
        self._initialize_routes()
            
    def _initialize_routes(self):
        """Initialize routes for the application."""
        cotegory_controller = self.container.category_controller()
        self.app.include_router(router=cotegory_controller.router, tags=["Category"])
    

    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance."""
        return self.app

Application = APP()
app = Application.get_app()
