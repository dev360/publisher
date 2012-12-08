#
# Profile
# -------
#
class publisher.models.Profile extends Backbone.Model

  defaults:
    id: ""

  url: ->
    return "/api/1.0/account/profile/?format=json"

publisher.app.data.profile = new publisher.models.Profile()
