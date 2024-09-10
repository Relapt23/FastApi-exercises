from fastapi import FastAPI, Header



app = FastAPI()
@app.get("/headers")
def head(user_agent: str = Header(), accept_language: str = Header()):
    return {'User-agent': user_agent,
             "Accept-language": accept_language}