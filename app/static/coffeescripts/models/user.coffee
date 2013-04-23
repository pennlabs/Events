define [], ->
  class User extends Backbone.Model
    idAttribute: "_id"
    defaults: ->
      return {
        description: ''
        email: ''
        logged_in: false
        events: []
        event_queue: []
        followers: []
        following: []
      }

    logout: ->
      @url = 'logout'
      @save(logged_in: false)

    add_to: (arr, el) ->
      a = _.clone @get(arr)
      a.push el
      @set(arr, a)

    subscribe: (user) ->
      $.ajax(
        url: "/api/users/#{user.id}/subscriptions"
        type: 'POST'
      ).done (event_ids) =>
        event_ids = $.parseJSON event_ids
        event_queue = _.clone @get("event_queue")
        event_queue = event_queue.concat event_ids
        @set(event_queue: event_queue)

        # add user to list of users that this user is following
        following = _.clone @get("following")
        following.push user.id
        @set(following: following)

        # add this user to the followers of the other user
        followers = _.clone user.get("followers")
        followers.push @id
        user.set(followers: followers)

  class Users extends Backbone.Collection
    model: Users
    url: '/api/users'

  return {model: User, collection: Users}
