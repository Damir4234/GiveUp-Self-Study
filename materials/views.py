from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from user.models import CompletedTasks
from materials.models import Answer, Course, Lesson
from django.contrib import messages
from user.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'materials/index.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Получаем список курсов, созданных текущим пользователем
    #     user = self.request.user
    #     context['created_courses'] = Course.objects.filter(author=user)
    #     # Получаем список всех курсов
    #     context['courses'] = Course.objects.all()
    #     return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     user = self.request.user
    #     created_courses = Course.objects.filter(author=user)
    #     print("Created courses:", created_courses)

    #     all_courses = Course.objects.all()
    #     print("All courses:", all_courses)
    #     context['created_courses'] = created_courses
    #     context['courses'] = all_courses
    #     return context


class CourseCreateView(CreateView, LoginRequiredMixin):
    model = Course
    fields = ['title', 'description']

    def get_success_url(self):

        course_id = self.object.pk

        return reverse_lazy('materials:lesson_create', kwargs={'course_id': course_id})

    def form_valid(self, form):

        form.instance.author = self.request.user
        return super().form_valid(form)


class CourseListView(ListView, LoginRequiredMixin):
    model = Course
    template_name = 'materials/courses_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView, LoginRequiredMixin):
    model = Course
    template_name = 'materials/course_detail.html'
    context_object_name = 'course'


class LessonCreateView(CreateView, LoginRequiredMixin):
    model = Lesson
    fields = ['title', 'content']
    template_name = 'materials/lesson_form.html'

    def form_valid(self, form):
        course_id = self.kwargs['course_id']
        form.instance.course_id = course_id
        super().form_valid(form)
        data = self.request.POST
        for key, value in data.items():
            if key.startswith('question_'):
                index = key.split('_')[1]
                question = value
                answer = data['answer_' + index]
                Answer.objects.create(
                    lesson=form.instance, question=question, correct_answer=answer)

        return super().form_valid(form)

    def get_success_url(self):
        course_id = self.kwargs['course_id']
        return reverse_lazy('materials:lesson_list', kwargs={'course_id': course_id})


class LessonDetailView(DetailView, LoginRequiredMixin):
    model = Lesson
    template_name = 'materials/lesson_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        user = self.request.user
        context['questions'] = Answer.objects.filter(lesson=lesson)
        context['completed_tasks'] = CompletedTasks.objects.filter(user=user)
        return context

    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        user = request.user
        for question in lesson.answer_set.all():
            answer_text = request.POST.get(str(question.id))
            completed_task = CompletedTasks.objects.filter(
                user=user, answer=question).first()
            if completed_task and completed_task.is_correct:
                messages.error(request, f"You've already answered question '{
                               question.question}' correctly.")
            else:
                is_correct = self.check_answer_correctness(
                    question.id, answer_text)
                if is_correct:
                    CompletedTasks.objects.create(
                        user=user, answer=question, is_correct=True)
                else:
                    messages.error(request, f"Your answer to question '{
                                   question.question}' is incorrect.")
        return redirect('materials:lesson_detail', pk=lesson.pk)

    def check_answer_correctness(self, question_id, answer_text):
        question = Answer.objects.get(pk=question_id)
        correct_answer = question.correct_answer
        return answer_text.strip().lower() == correct_answer.strip().lower()


class LessonListView(ListView, LoginRequiredMixin):
    model = Lesson
    template_name = 'materials/lesson_list.html'
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)

        context['course'] = course
        return context


class DashboardView(TemplateView, LoginRequiredMixin):
    template_name = 'materials/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        created_courses = Course.objects.filter(author=self.request.user)
        context['created_courses'] = created_courses

        all_courses = Course.objects.all()
        context['courses'] = all_courses
        return context


class CourseUpdateView(UserPassesTestMixin, UpdateView):
    model = Course
    fields = ['title', 'description']
    template_name = 'materials/course_update.html'  # Имя вашего шаблона HTML
    context_object_name = 'course'
    success_url = reverse_lazy('materials:dashboard')

    def test_func(self):

        course = self.get_object()

        return self.request.user == course.author

    def handle_no_permission(self):

        return redirect('home')
