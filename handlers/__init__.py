from handlers.product_handlers import router as product_router
from handlers.auth_handlers import router as auth_router
from handlers.user_handlers import router as user_router


routers = [product_router, user_router, auth_router]
