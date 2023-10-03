from cms.models.pagemodel import Page, TreeNode
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from .models import HtmlSitemapPluginConf


class HtmlSitemapPlugin(CMSPluginBase):
    model = HtmlSitemapPluginConf
    name = _("HTML Sitemap")

    render_template = "djangocms_htmlsitemap/sitemap.html"

    def render(self, context, instance, placeholder):
        request = context["request"]
        language = request.LANGUAGE_CODE

        site = Site.objects.get_current()

        path_column = "node__path"
        node_column = "node__depth"

        pages = (
            Page.objects.public()
            .published(site=site)
            .order_by(path_column)
            .filter(login_required=False, **{node_column + "__gte": instance.min_depth})
            .filter(title_set__language=language)
            .distinct()
        )

        if instance.max_depth:
            pages = pages.filter(**{node_column + "__lte": instance.max_depth})
        if instance.in_navigation is not None:
            pages = pages.filter(in_navigation=instance.in_navigation)

        context["instance"] = instance
        context["pages"] = pages

        nodes = [page.node for page in pages.select_related("node")]
        annotated_nodes = TreeNode.get_annotated_list_qs(nodes)
        annotated_pages = [
            (pages[x], annotated_nodes[x][1]) for x in range(0, len(nodes))
        ]

        context["annotated_pages"] = annotated_pages

        return context


plugin_pool.register_plugin(HtmlSitemapPlugin)
