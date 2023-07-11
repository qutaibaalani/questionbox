from django.urls import path, include
from questions import views


urlpatterns = [
    # GET|POST
    path("questions/", views.QuestionViewSet.as_view(), name="questions"),
    # GET
    path(
        "questions/user/", views.QuestionByUserViewSet.as_view(), name="user_questions"
    ),
    # GET|POST
    path("questions/answer/", views.AnswerByQuestionViewSet.as_view(), name="answers"),
    # GET
    path(
        "questions/<int:pk>/",
        views.QuestionWithAnswerViewSet.as_view(),
        name="question_details",
    ),
    # PATCH
    path(
        "answers/accept/<int:pk>/",
        views.AcceptAnswerViewSet.as_view(),
        name="accept_answer",
    ),
    # GET
    path("user/answers/", views.UserAnswersViewSet.as_view(), name="user_answers"),
    # DELETE
    path(
        "questions/delete/<int:pk>/",
        views.DeleteQuestionViewSet.as_view(),
        name="delete_question",
    ),
    # GET
    path(
        "questions/search/",
        views.QuestionSearchViewSet.as_view(),
        name="questions_search",
    ),
    # POST
    path("uploads/", views.UploadCreateView.as_view()),
    # GET|POST
    path("questions/tag/", views.TagCreateView.as_view()),
    # GET
    path(
        "tag/search/",
        views.TagSearchViewSet.as_view(),
        name="tag_search",
    ),
]
