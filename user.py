from os import environ


class User:
  def __init__(self, id, username, password):
    self.id = id
    self.username = username
    self.password = password
    
    def __repr__(self):
      return f'<User: {self.username}>'


users = []
users.append(User(id=1, username=environ.get('DEFAULT_USERNAME'), password=environ.get('DEFAULT_PASSWORD')))