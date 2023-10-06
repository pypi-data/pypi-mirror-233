import argparse

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from auth.router import auth_router
from users.router import user_router

app = FastAPI(title='AuthApi')

origins = [
	"http://localhost:3005",
	"https://localhost:3005",
	"http://localhost",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--template", required=False, action=argparse.BooleanOptionalAction)
args = parser.parse_args()

if args.template:
	from page import page_router

	app.mount("/static", StaticFiles(directory="static"), name="static")
	app.include_router(page_router)

app.include_router(user_router)
app.include_router(auth_router)

if __name__ == '__main__':
	uvicorn.run('__main__:app', host="localhost", port=3000, reload=True)
