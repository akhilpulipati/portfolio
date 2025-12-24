import os
import smtplib
from email.message import EmailMessage
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/contact")
async def contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    msg = EmailMessage()
    msg["Subject"] = f"Portfolio Contact from {name}"
    msg["From"] = os.environ["GMAIL_USER"]
    msg["To"] = os.environ["GMAIL_USER"]
    msg.set_content(
        f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(
            os.environ["GMAIL_USER"],
            os.environ["GMAIL_APP_PASSWORD"]
        )
        server.send_message(msg)

    return RedirectResponse(url="/", status_code=303)
