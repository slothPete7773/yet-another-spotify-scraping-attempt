from datetime import datetime

with open("./cronjob.txt", "a") as file:
    text = f"Hello World @ {datetime.now()}\n"
    file.write(text)