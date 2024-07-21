from flask import Flask, render_template, HTTPException
from models import db, Users, TheGoods, UserDate, UserIn
import uvicorn

users = []
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('NICE')


@app.cli.command('user-db')
def add_data():
    for i in range(1, 4):
        the_goods = TheGoods(
            name=f'goods_{i}'
        )
        db.session.add(the_goods)

    for i in range(0, 10):
        user = Users(
            firstname=f'firstname{i}',
            lastname=f'lastname{i}',
            email=f'{i}@gmail.com',
            password=f'{i}123')
        db.session.add(user)
    db.session.commit()
    print("Datas added")


@app.get('/')
def get_student():
    user = Users.query.all()
    context = {
        'students': user
    }
    return render_template('index.html', **context)


@app.post("/users/", response_model=list[UserDate])
async def create_user(new_user: UserIn):
    users.append(UserDate(id=len(users) + 1,
                 name=new_user.name,
                 surname=new_user.surname)
                 )
    return users


@app.put("/users/", response_model=list[UserDate])
async def edit_user(user_id: int, new_user: UserIn):
    for i in range(0, len(users)):
        if users[i].id == user_id:
            current_user = users[user_id - 1]
            current_user.name = new_user.title
            current_user.surname = new_user.description
            return current_user
    raise HTTPException(status_code=404, detail='User not found')


@app.delete("/users/", response_model=dict)
async def delete_user(user_id: int):
    for i in range(0, len(users)):
        if users[i].id == user_id:
            users.remove(users[i])
            return {'message': "User was deleted"}

        raise HTTPException(status_code=404, detail='User not found')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )