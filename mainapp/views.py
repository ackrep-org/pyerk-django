from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from django.urls import reverse
from django.db.models import Q
import pyerk

from ipydex import IPS

from .models import Entity


def reload_data():
    """
    Load data from python-module into data base to allow simple searching
    :return:
    """

    # delete all existing data
    Entity.objects.all().delete()

    mod = pyerk.erkloader.load_mod_from_path("../controltheory_experiments/knowledge_base1.py", "knowledge_base1")

    for itm in pyerk.ds.items.values():
        Entity.objects.create(
            key_str=itm.short_key,
            label=getattr(itm, "R1", None),
            description=getattr(itm, "R2", None),
        )

    for rel in pyerk.ds.relations.values():
        Entity.objects.create(
            key_str=rel.short_key,
            label=getattr(rel, "R1", None),
            description=getattr(rel, "R2", None),
        )


def home_page_view(request):

    # TODO: in the future this should not be triggered on every page refresh
    reload_data()

    context = dict(greeting_message="Hello, World!")

    return render(request, 'mainapp/landing-page.html', context)


# /search/?q=...
def get_item(request):

    q = request.GET.get("q")
    template = get_template("mainapp/entity-list-entry.html")

    payload = []
    if q:
        entities = Entity.objects.filter(Q(label__icontains=q) | Q(key_str__icontains=q))

        for idx, db_entity in enumerate(entities):
            db_entity: Entity
            ctx = {
                "key_str": db_entity.key_str,
                "label": db_entity.label,
                "description": db_entity.description,
                "url": reverse("entitypage", kwargs={"key_str": db_entity.key_str}),
                "idx": idx
            }
            rendered_entity = template.render(context=ctx)
            payload.append(rendered_entity)

    return JsonResponse({"status": 200, "data": payload})


def mockup(request):
    db_entity = get_object_or_404(Entity, key_str="I5")
    template = get_template("mainapp/entity-list-entry.html")
    ctx = {
        "key_str": db_entity.key_str,
        "label": db_entity.label,
        "description": db_entity.description,
        "url": reverse("entitypage", kwargs={"key_str": db_entity.key_str}),
        "idx": 23
    }

    rendered_entity = template.render(context=ctx)

    context = dict(greeting_message="Hello, World!", rendered_entity=rendered_entity)

    return render(request, 'mainapp/searchresult-test-page.html', context)


def entity_view(request, key_str=None):
    db_entity = get_object_or_404(Entity, key_str=key_str)
    template = get_template("mainapp/entity-list-entry.html")
    ctx = {
        "key_str": db_entity.key_str,
        "label": db_entity.label,
        "description": db_entity.description,
    }
    rendered_entity = template.render(context=ctx)

    context = dict(rendered_entity=rendered_entity, entity=db_entity)
    return render(request, 'mainapp/entity-detail-page.html', context)


def debug_view(request, xyz=0):

    z = 1

    if xyz == 1:
        # start interactive shell for debugging (helpful if called from the unittests)
        IPS()

    elif xyz == 2:
        return HttpResponseServerError("Errormessage")

    return HttpResponse(f'Some plain message {xyz}')
