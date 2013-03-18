define [], ->
  class User extends Backbone.Model
    defaults:
      email: 'yefim323@gmail.com'
      first_name: 'Geoffrey'
      last_name: 'Vedernikoff'
      logged_in: false

    logout: ->
      @url = 'api/logout'
      @save(logged_in: false)

  class Users extends Backbone.Collection
    model: Users
    url: '/api/users'

  return {model: User, collection: Users}
