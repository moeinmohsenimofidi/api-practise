import ytube


Access_token = "F1SoyVG94-M48GOkXl4sv97eQR0dfCzBoP3NSKPZOAY"

api_client = patreon.API(Access_token)

#get the campaign id

campaign_response = api_client.fetch_campaign()
campaign_id = campaign_response.data()[0].id


pledges_response = api_client.fetch_page_of_pledges(compaign_id, 25)
print(pledges_response.data())
