from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.home_page_view, name="landingpage"),
    path(r"mockup", views.mockup, name="mockuppage"),
    path(r"search/", views.get_item, name="search"),
    path("sparql/", views.SearchSparqlView.as_view(), name="sparqlpage"),
    path(r"e/<str:key_str>", views.entity_view, name="entitypage"),
    path(r"debug", views.debug_view, name="debugpage0"),
    path(r"debug/<int:xyz>", views.debug_view, name="debugpage_with_argument"),
]
