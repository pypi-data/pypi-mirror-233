from typing import Tuple, Optional, List

import facebook


class FacebookConnection:
    def __init__(self, app_id: str = None, secret: str = None, access_token: str = None, version="3.0"):
        self.__api_version = version
        self.__app_id = app_id
        self.__app_secret = secret
        self.graph = facebook.GraphAPI(access_token=access_token, version=self.__api_version)

    def get_login_url(self, redirect_url: str, scope: str) -> str:
        """
        Generate login URL to fetch facebook access code (not access token)
        :param redirect_url: redirect url in case of successful authorization
        :param scope: permissions to ask to facebook
        :return: login url to facebook
        """
        login_url = self.graph.get_auth_url(
            app_id=self.__app_id,
            canvas_url=redirect_url,
            scope=scope,
        )

        return login_url

    def get_ads_related_auth_url(self, redirect_url: str):
        """
        Generate login url for ads related permissions: email,ads_read,ads_management,pages_show_list,pages_manage_ads
        :param redirect_url: redirect url in case of successful authorization
        :return: login url to facebook
        """
        return self.get_login_url(redirect_url, scope="email,ads_read,ads_management,pages_show_list,pages_manage_ads")

    def get_access_token(self, code: str, redirect_uri: str) -> Tuple[str, int]:
        """
        Generate access token for access code.
        :param code: access code from get_ads_related_auth_url or get_login_url functions
        :param redirect_uri: redirect url in case of successful authorization
        :return: access token, expiration duration in seconds
        """
        response = facebook.GraphAPI().get_access_token_from_code(
            app_id=self.__app_id,
            app_secret=self.__app_secret,
            redirect_uri=redirect_uri,
            code=code,
        )

        access_token = response["access_token"]
        expires_in = response["expires_in"]

        return access_token, expires_in

    def get_ad_accounts(self) -> Optional[List[dict]]:
        """
        Get ad accounts via access token.
        Response example: examples/ad_accounts.json
        """
        try:
            response = self.graph.get_object('me/adaccounts', fields='name')
            ad_accounts = response["data"]
            return ad_accounts
        except facebook.GraphAPIError:
            raise

    def get_ad_account_campaigns(self, account_id) -> Optional[List[dict]]:
        """
        Get campaigns via ad account id and access token.
        Response example: examples/campaigns.json
        """
        try:
            campaign_fields = ("id,account_id,adlabels,bid_strategy,boosted_object_id,brand_lift_studies,"
                               "budget_rebalance_flag,budget_remaining,buying_type,campaign_group_active_time,"
                               "can_create_brand_lift_study,can_use_spend_cap,configured_status,created_time,"
                               "daily_budget,effective_status,has_secondary_skadnetwork_reporting,"
                               "is_budget_schedule_enabled,is_skadnetwork_attribution,issues_info,"
                               "last_budget_toggling_time,lifetime_budget,name,objective,pacing_type,"
                               "primary_attribution,promoted_object,recommendations,smart_promotion_type,"
                               "source_campaign,source_campaign_id,special_ad_categories,special_ad_category,"
                               "special_ad_category_country,spend_cap,start_time,status,stop_time,topline_id,"
                               "updated_time")
            response = self.graph.get_object(f"{account_id}/campaigns", fields=campaign_fields)
            campaigns = response["data"]
            if not campaigns:
                return []

            return campaigns
        except facebook.GraphAPIError:
            raise

    def get_ad_campaign_ad_sets(self, campaign_id: str) -> Optional[List[dict]]:
        """
        Get ad sets via ad campaign id and access_token
        Response example: examples/adsets.json
        """
        try:
            adset_fields = ("id,account_id,adlabels,adset_schedule,asset_feed_id,attribution_spec,bid_adjustments,"
                            "bid_amount,bid_constraints,bid_info,bid_strategy,billing_event,budget_remaining,campaign,"
                            "campaign_active_time,campaign_attribution,campaign_id,configured_status,created_time,"
                            "creative_sequence,daily_budget,daily_min_spend_target,daily_spend_cap,destination_type,"
                            "dsa_beneficiary,dsa_payor,effective_status,end_time,frequency_control_specs,"
                            "instagram_actor_id,is_budget_schedule_enabled,is_dynamic_creative,issues_info,"
                            "learning_stage_info,lifetime_budget,lifetime_imps,lifetime_min_spend_target,"
                            "lifetime_spend_cap,multi_optimization_goal_weight,name,optimization_goal,"
                            "optimization_sub_event,pacing_type,promoted_object,recommendations,"
                            "recurring_budget_semantics,review_feedback,rf_prediction_id,source_adset,source_adset_id,"
                            "start_time,status,targeting,targeting_optimization_types,time_based_ad_rotation_id_blocks,"
                            "time_based_ad_rotation_intervals,updated_time,use_new_app_click")

            response = self.graph.get_object(f"/{campaign_id}/adsets", fields=adset_fields)
            ad_sets = response["data"]
            if not ad_sets:
                return []
            return ad_sets
        except facebook.GraphAPIError:
            raise

    def get_ad_set_ads(self, ad_set_id: str) -> Optional[List[dict]]:
        """
        Get ad via ad set id and access token.
        Response example: examples/ad.json
        """
        try:
            ad_set_response = self.graph.get_object(f"{ad_set_id}/ads", fields="id")
            data = ad_set_response["data"]
            ad_set_ad_ids = [ad["id"] for ad in ad_set_response["data"]]
            if not ad_set_ad_ids:
                return []

            ad_fields = ("id,account_id,ad_active_time,ad_review_feedback,ad_schedule_end_time,ad_schedule_start_time,"
                         "adlabels,adset,adset_id,bid_amount,campaign,campaign_id,configured_status,conversion_domain,"
                         "created_time,creative,effective_status,issues_info,last_updated_by_app_id,"
                         "meta_reward_adgroup_status,name,preview_shareable_link,recommendations,source_ad,"
                         "source_ad_id,status,tracking_specs,updated_time")

            ads = list()
            for ad_id in ad_set_ad_ids:
                ad_data = self.graph.get_object(str(ad_id), fields=ad_fields)
                if ad_data:
                    ads.append(ad_data)

            return ads
        except facebook.GraphAPIError:
            raise
