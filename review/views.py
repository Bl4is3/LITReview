from itertools import chain
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import formset_factory
from django.db.models import CharField, Value, Q
from django.core.paginator import Paginator

from .forms import TicketForm, ReviewForm, FollowUsersForm
from review.models import Ticket, Review, UserFollows
from authentication.models import User


@login_required
def feed(request):
    follows = UserFollows.objects.filter(user=request.user)
    followed = []
    for follow in follows:
        followed.append(follow.followed_user)
    my_follows = User.objects.filter(username__in=followed)

    tickets = Ticket.objects.filter(Q(user=request.user) |Q(user__in=my_follows))
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    reviews = Review.objects.filter(Q(user=request.user) | Q(user__in=my_follows) | Q(ticket__in=tickets))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    # on récupère les tickets qui ont déjà une critique
    tickets_in_review = Ticket.objects.filter(review__in=reviews)

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True,
    )

    paginator = Paginator(posts, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "review/feed.html", locals())


@login_required
def create_edit_review(request, review_id=None, ticket_id=0):
    if review_id:
        ticket_id = Ticket.objects.get(pk=Review.objects.get(pk=review_id).ticket.id).id
    ticket_form = TicketForm(
        request.POST if request.method == "POST" else None,
        request.FILES if request.method == "POST" else None,
        instance=Ticket.objects.get(pk=ticket_id) if ticket_id != 0  else None,
    )
    review_form = ReviewForm(
        request.POST if request.method == "POST" else None,
        instance=Review.objects.get(pk=review_id) if review_id else None,
    )
    if request.method == "POST" and review_form.is_valid() and ticket_form.is_valid():
        ticket = ticket_form.save(commit=False)
        if not ticket.user:
            ticket.user = request.user
        ticket.save()
        review = review_form.save(commit=False)
        review.user = request.user
        review.ticket = ticket
        review.save()
        return redirect("review:feed")
    return render(request, "review/create_edit_review.html", locals())


@login_required
# @permission_required('review.delete', raise_exception=True)
@require_http_methods(["POST"])  # penser aux permissions
def delete_review(request, review_id=None):
    try:
        Review.objects.filter(
            pk=request.POST.get('review_id'), user=request.user
        ).delete()
    except Review.DoesNotExist:
        raise Http404()
    return redirect("review:feed")


@login_required
# ajouter @permission_required()
def create_edit_ticket(request, ticket_id=None):
    ticket_form = TicketForm(
        request.POST if request.method == "POST" else None,
        request.FILES if request.method == "POST" else None,
        instance=Ticket.objects.get(pk=ticket_id) if ticket_id else None,
    )
    if request.method == "POST" and ticket_form.is_valid():
        ticket = ticket_form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect("review:feed")
    return render(request, "review/create_edit_ticket.html", locals())


@login_required
@require_http_methods(["POST"])  # penser aux permissions
def delete_ticket(request):
    try:
        Ticket.objects.filter(
            pk=request.POST.get('ticket_id'), user=request.user
        ).delete()
    except Ticket.DoesNotExist:
        raise Http404()
    return redirect("review:feed")


@login_required
def follows(request):
    follow_form = FollowUsersForm(
        request.POST if request.method == "POST" else None
    )
    if request.method == "POST" and follow_form.is_valid():
        # if follow_form.user in User.objects.all():
        follow = follow_form.save(commit=False)
        follow.user = request.user
        follow.save()
        return redirect("review:follows")
    follows = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    return render(request, "review/follows.html",locals())

@login_required
@require_http_methods(["POST"])  # penser aux permissions
def delete_follow(request):
    try:
        UserFollows.objects.filter(
            pk=request.POST.get('follow_id'), user=request.user
        ).delete()
    except UserFollows.DoesNotExist:
        raise Http404()
    return redirect("review:follows")

@login_required
def posts(request):
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    tickets = Ticket.objects.filter(user=request.user).exclude(
        review__in=reviews
    )
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True,
    )  
    return render(request, "review/posts.html", locals())
