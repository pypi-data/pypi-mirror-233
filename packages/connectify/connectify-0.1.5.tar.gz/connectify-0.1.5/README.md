# Connectify

![Static Badge](https://img.shields.io/badge/version-0.1.5-green)

**Connectify** provides convenient Python interfaces to interact with popular **I**/**O** services such as **Slack**,
**Facebook**, databases etc.

## Slack services

### Supported actions

Currently, we support the following functionalities from Slack API inside SlackConnection/AsyncSlackConnection classes

- [x] [channel_conversation_history](https://github.com/muladzevitali/connectify/blob/main/connectify/slack_services/slack_connection.py) - Get channel conversion history for
  given channel
- [x] [get_channel_latest_message](https://github.com/muladzevitali/connectify/blob/main/connectify/slack_services/slack_connection.py) - Fetch latest message from specific
  channel
- [x] [send_text_message](https://github.com/muladzevitali/connectify/blob/main/connectify/slack_services/slack_connection.py) - Send text type message to specific channel
- [x] [send_scheduled_text_message](https://github.com/muladzevitali/connectify/blob/main/connectify/slack_services/slack_connection.py) - Schedule text message send for
  specific time
- [x] [send_file_message](https://github.com/muladzevitali/connectify/blob/main/connectify/slack_services/slack_connection.py) - Send file to channel

> [!NOTE]
> Full documentation is available in [readme.md](https://github.com/muladzevitali/connectify/blob/main/connectify/slack_services/readme.md)

## Facebook Graph API connection

### Supported actions

Currently, we support the following functionalities from Graph API inside FacebookConnection class

- [x] [get_login_url](https://github.com/muladzevitali/connectify/blob/main/connectify/facebook_services/facebook_connection.py) - Generate login URL with given scope of permissions to get access code
  and
  then access token from Graph API
- [x] [get_ads_related_auth_url](https://github.com/muladzevitali/connectify/blob/main/connectify/facebook_services/facebook_connection.py) - Generate login URL for ads related permissions
- [x] [get_access_token](https://github.com/muladzevitali/connectify/blob/main/connectify/facebook_services/facebook_connection.py) - Get access token from the access code fetched from the steps 1 or 2
- [x] [get_ad_accounts](https://github.com/muladzevitali/connectify/blob/main/connectify/facebook_services/facebook_connection.py) - Get ad accounts existing under the access token initialize the class
  with.
- [x] [get_ad_account_campaigns](https://github.com/muladzevitali/connectify/blob/main/connectify/facebook_services/facebook_connection.py) - Get campaigns under given ad account
- [x] [get_ad_campaign_ad_sets](https://github.com/muladzevitali/connectify/blob/main/connectify/facebook_services/facebook_connection.py) - Get ad sets under given campaign
- [x] [get_ad_set_ads](https://github.com/muladzevitali/connectify/blob/main/connectify/facebook_services/facebook_connection.py) - Get ads under given ad set

> [!NOTE]
> Full documentation is available in [readme.md](https://github.com/muladzevitali/connectify/blob/main/connectify/facebook_services/readme.md)
