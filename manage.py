#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investsite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from investments.models import InvestmentPlan, Investment


@login_required
def plans(request):
    plans = InvestmentPlan.objects.all()
    return render(request, "plans.html", {"plans": plans})


@login_required
def invest(request, plan_id):
    plan = get_object_or_404(InvestmentPlan, id=plan_id)

    if request.method == "POST":
        amount = request.POST.get('amount')

        Investment.objects.create(
            user=request.user,
            plan=plan,
            amount=amount
        )

        return redirect('/dashboard')

    return render(request, "invest.html", {"plan": plan})
