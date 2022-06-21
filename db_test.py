from db import User
current_user = User.query.get(1)
print(current_user)
print(f'{current_user.id} | {current_user.username} | {current_user.password} | {current_user.TMDB_id}')
print(User.query.all())

