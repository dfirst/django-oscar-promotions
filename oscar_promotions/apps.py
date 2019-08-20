from django.conf.urls import url
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from oscar.core.application import OscarConfig
from oscar.core.loading import get_class, get_model


class PromotionsConfig(OscarConfig):

    label = 'oscar_promotions'
    name = 'oscar_promotions'
    verbose_name = _("Promotions")

    namespace = 'promotions'

    def ready(self):
        super().ready()
        self.home_view = get_class('oscar_promotions.views', 'HomeView')
        self.record_click_view = get_class('oscar_promotions.views', 'RecordClickView')

        settings.OSCAR_DASHBOARD_NAVIGATION += {
            'label': _('Content blocks'),
            'icon': 'icon-folder-close',
            'children': [
                {
                    'label': _('Content blocks'),
                    'url_name': 'dashboard:promotion-list',
                },
                {
                    'label': _('Content blocks by page'),
                    'url_name': 'dashboard:promotion-list-by-page',
                },
            ]
        },

    def get_urls(self):
        PagePromotion = get_model('oscar_promotions', 'PagePromotion')
        KeywordPromotion = get_model('oscar_promotions', 'KeywordPromotion')
        urls = [
            url(
                r'page-redirect/(?P<page_promotion_id>\d+)/$',
                self.record_click_view.as_view(model=PagePromotion),
                name='page-click',
            ),
            url(
                r'keyword-redirect/(?P<keyword_promotion_id>\d+)/$',
                self.record_click_view.as_view(model=KeywordPromotion),
                name='keyword-click',
            ),
            url(r'^$', self.home_view.as_view(), name='home'),
        ]
        return self.post_process_urls(urls)
