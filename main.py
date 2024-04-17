from texturebackend import server
import uvicorn
import os

app = server.get_server()

# # Similar to uvicorn --factory texturebackend.server:get_server --reload
# if __name__ == "__main__":
#     print(">>>> Launching FASTAPI server from main.py")
#     app = server.get_server()

#     uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
