from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import plotly.express as px
from plotly.offline import plot
import pandas as pd

from .models import Recipe, Step


def _gaant_from_steps(steps, width, display_step_titles=True):
    df = [
        {
            "Start": pd.Timestamp(step.start, unit="m"),
            "End": pd.Timestamp(step.end, unit="m"),
            "Title": step.title if display_step_titles else "",
        }
        for step in steps
    ]
    gaant = px.timeline(
        df,
        x_start="Start",
        x_end="End",
        y="Title",
        color="Title",
        width=width,
        height=(width * 3) // 4,
        labels={"Title": " "},
    )

    gaant.update_yaxes(autorange="reversed")
    gaant.update_xaxes(tickformat="%H:%M")
    gaant.update_layout(showlegend=False)
    gaant.update_traces(width=0.2)

    return plot(gaant, output_type="div", config={"staticPlot": True})


def index(request):
    recipes = Recipe.objects.all()
    cards = [
        {
            "recipe": recipe,
            "gaant": _gaant_from_steps(Step.objects.filter(recipe=recipe), 300),
        }
        for recipe in recipes
    ]
    context = {"cards": cards}

    return render(request, "recipes/index.html", context)


def edit(request, recipe_id):
    context = {
        "recipe": get_object_or_404(Recipe, pk=recipe_id),
        "steps": get_list_or_404(Step, recipe=recipe_id),
    }

    return render(request, "recipes/edit.html", context)


def create(request):
    context = {
        "recipe": {"id": "new", "name": "New Recipe", "Ingredients": ""},
        "steps": [
            {
                "recipe": "new",
                "start": "0",
                "end": "10",
                "title": "New Step",
                "description": "",
            }
        ],
    }

    return render(request, "recipes/edit.html", context)


def detail(request, recipe_id):
    steps = get_list_or_404(Step, recipe=recipe_id)

    context = {
        "recipe": get_object_or_404(Recipe, pk=recipe_id),
        "steps": steps,
        "gaant": _gaant_from_steps(steps, 800),
    }

    return render(request, "recipes/detail.html", context)


def submit(request, recipe_id):
    i = 1
    steps = []
    invalid_step_titles = []

    while f"start-{i}" in request.POST:
        title = request.POST[f"title-{i}"]
        start = request.POST[f"start-{i}"]
        end = request.POST[f"end-{i}"]

        try:
            int(start)
            int(end)
        except ValueError:
            invalid_step_titles.append(title)

        steps.append(
            {
                "start": start,
                "end": end,
                "title": title,
                "description": request.POST[f"description-{i}"],
            }
        )
        i += 1

    name = request.POST["recipename"]
    ingredients = request.POST["ingredients"]

    if invalid_step_titles:
        return render(
            request,
            "recipes/edit.html",
            {
                "recipe": {"name": name, "ingredients": ingredients, "id": "new"},
                "steps": steps,
                "error_message": f"Invalid time boundaries for steps {', '.join(invalid_step_titles)}",
            },
        )

    try:
        recipe = Recipe.objects.get(pk=recipe_id)
    except ValueError:
        recipe = Recipe.objects.create()

    recipe.name = name
    recipe.ingredients = ingredients
    recipe.save()

    Step.objects.filter(recipe=recipe).delete()

    Step.objects.bulk_create([Step(**step, recipe=recipe) for step in steps])

    return HttpResponseRedirect(reverse("recipes:detail", args=(recipe.id,)))


def delete(_, recipe_id):
    Recipe.objects.get(pk=recipe_id).delete()
    return HttpResponseRedirect(reverse("recipes:index"))
