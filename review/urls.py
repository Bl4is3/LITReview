from django.urls import path

from review import views

app_name = "review"

urlpatterns = [
    path("feed/", views.feed, name="feed"),
    path("posts/", views.posts, name="posts"),
    path("follows/", views.follows, name="follows"),
    path("follows/delete/", views.delete_follow, name="delete_follow"),
    path("ticket/create", views.create_edit_ticket, name="create_edit_ticket"),
    path("ticket/update/<int:ticket_id>/",views.create_edit_ticket,name="update_ticket"),
    path("ticket/delete/", views.delete_ticket, name="delete_ticket"),
    path("review/create_new/<int:ticket_id>", views.create_edit_review, name="create_edit_review"),
    path("review/update/<int:review_id>", views.create_edit_review, name="update_review"),
    path("review/delete/", views.delete_review, name="delete_review"),
]
