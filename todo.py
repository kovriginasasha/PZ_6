from fastapi import (
    APIRouter,
    Path,
    HTTPException,
    status,
    Request,
    Depends
)

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model import Todo, TodoItem


todo_router = APIRouter()

todo_list = []

templates = Jinja2Templates(directory="templates/")


# 1. Добавление задачи
@todo_router.post("/todo")
async def add_todo(
    todo: Todo = Depends(Todo.as_form)
):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)

    return RedirectResponse(
        url="/todo",
        status_code=303
    )


# 2. Получение всех задач
@todo_router.get("/todo")
async def retrieve_todo(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={
            "todos": todo_list
        }
    )


# 3. Удаление всех задач
@todo_router.delete("/todo")
async def delete_all_todo() -> dict:

    todo_list.clear()

    return {
        "message": "Александра Ковригина успешно удалила все задачи."
    }


# 4. Получение одной задачи
@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
    request: Request,
    todo_id: int = Path(
        ...,
        title="The ID of the todo to retrieve"
    )
):

    for todo in todo_list:

        if todo.id == todo_id:

            return templates.TemplateResponse(
                request=request,
                name="todo.html",
                context={
                    "todo": todo
                }
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача с указанным ID не существует.",
    )


# 5. Изменение задачи
@todo_router.put("/todo/{todo_id}")
async def update_todo(
    todo_data: TodoItem,
    todo_id: int = Path(
        ...,
        title="The ID of the todo to be updated"
    )
) -> dict:

    for todo in todo_list:

        if todo.id == todo_id:

            todo.item = todo_data.item

            return {
                "message": "Александра Ковригина успешно обновила задачу."
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача с указанным ID не существует.",
    )


# 6. Удаление одной задачи
@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:

    for index in range(len(todo_list)):

        todo = todo_list[index]

        if todo.id == todo_id:

            todo_list.pop(index)

            return {
                "message": "Александра Ковригина успешно удалила задачу."
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача с указанным ID не существует.",
    )