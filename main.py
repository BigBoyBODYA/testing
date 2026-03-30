import logging, re, asyncio, os
import winsound
from datetime import datetime
logging.basicConfig(filename="actions.log",encoding="utf-8",level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

class Task():
    def __init__(self, date, text):
        self.__date = date
        self.__text = text
        self.done = False
    def __str__(self):
        return f"{self.__date} - {self.__text}"
    def __repr__(self):
        return f"Task({self.__date} - {self.__text})"
    def set_task_done(self):
        self.done = True
    def get_time(self):
        return self.__date
    def get_text(self):
        return self.__text


pattern = r'(\d{2}:\d{2})\s*-\s*(.+)'
def load_tasks():
    try:
        with open("output.txt", mode="r", encoding="utf-8") as fileread:
            lines = fileread.read()
            tasks = []

            matches = re.findall(pattern, lines)
            for match in matches:
                tasks.append(Task((match[0]),
                                  match[1]))
            return tasks
    except FileExistsError:
        logging.error("File output.txt Not Found")
async def notify_tasks(tasks):
    while True:
        await asyncio.sleep(5)
        now = f"{datetime.now().hour}:{datetime.now().minute}"
        for task in tasks:
            if not task.done and now >= task.get_time():
                winsound.Beep(1000, 200)
                winsound.Beep(1000, 200)
                winsound.Beep(4000, 200)
                winsound.Beep(5000, 200)
                winsound.Beep(2000, 200)
                winsound.Beep(2000, 200)

                print(f"Notify: {task}")
                task.set_task_done()

async def watch_file(tasks):
    last_edit_time = os.path.getmtime("output.txt")
    while True:
        await asyncio.sleep(5)
        current_edit_time = os.path.getmtime("output.txt")
        if last_edit_time != current_edit_time:
            last_edit_time = current_edit_time
            new_tasks = load_tasks()
            existing = {str(t) for t in tasks}
            for task in new_tasks:
                if str(task) not in existing:
                    tasks.append(task)
async def main():
    tasks = load_tasks()
    if not tasks:
        print("Задач нет")
        return
    for task in tasks:
        print(task)
    await asyncio.gather(notify_tasks(tasks), watch_file(tasks))

if __name__ == "__main__":
    asyncio.run(main())
