
import uvicorn
from product_recommentation.app import app

if __name__ == "__main__":
    uvicorn.run(app, debug=True)