import time
import json
import os


def error(text, is_exit=True):
    print(text)
    if is_exit:
        exit(1)

if __name__ == "__main__":

    TASKS_DIR = os.path.dirname(__file__) + '_Сотрудники'
    path = 'todos.json'

    try:
        with open(path, 'r') as f:
            data = f.read()
    except:
        error("Не удалось открыть файл с пользователями.")

    try:
        parsed_tasks = json.loads(data)
    except:
        error('Не удалось получить пользователей.')

# process each task
    users = {}
    for task in parsed_tasks:
        if (not("userId" in task and "id" in task and
                "title" in task and "completed" in task)):
            continue;

        if (task["userId"] not in users):
            newUser = {}
            newUser["current"] = []
            newUser["completed"] = []
            users[task["userId"]] = newUser

        if (task["completed"]):
            users[task["userId"]]["completed"].append(task["title"])
        else:
            users[task["userId"]]["current"].append(task["title"])

# create dir for user files
    if not os.path.isdir(TASKS_DIR):
        try:
            os.mkdir(TASKS_DIR)
        except:
            error('Не удалось создать боевую директорию')


# save each user in file
    for user_id in users:
        file_path = TASKS_DIR + '/' + str(user_id) + '_' + \
                    time.strftime('%Y-%m-%dT%H-%M') + '.txt'

        user_file = open(file_path, "w")

        user_file.write("# Сотрудник №" + str(user_id) + '\n')
        user_file.write(time.strftime('%d.%m.%Y %H:%M', time.localtime()) + '\n\n')
        user_file.write("## Завершённые задачи:\n")

        for task_title in users[user_id]["completed"]:
            if len(task_title) > 50:
                user_file.write(task_title[:50] + '...\n')
            else:
                user_file.write(task_title + '\n')

        user_file.write("\n## Оставшиеся задачи:\n")

        for task_title in users[user_id]["current"]:
            if len(task_title) > 50:
                user_file.write(task_title[:50] + '...\n')
            else:
                user_file.write(task_title + '\n')

        user_file.close()