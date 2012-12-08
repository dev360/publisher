#
# Address
# ---------
#
class publisher.models.Address extends Backbone.Model

  defaults:
    id: ""

  url: ->
    id = @.get('id')
    return "/api/1.0/account/profile/addresses/#{id}/?format=json"


#
# AddressList
# -----------
#
class publisher.models.AddressList extends Backbone.Collection

  defaults:
    id: ""

  url: ->
    return "/api/1.0/account/profile/addresses/?format=json"


