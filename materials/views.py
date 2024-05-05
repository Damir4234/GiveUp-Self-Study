from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from user.models import CompletedTasks, User
from materials.models import Answer, Course, Lesson
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'materials/index.html'


class CourseCreateView(CreateView):
    model = Course
    fields = ['title', 'description', 'author']

    def get_success_url(self):
        return reverse_lazy('user:profile', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Добавляем текущего пользователя как автора курса
        form.instance.author = self.request.user
        return super().form_valid(form)


class CourseListView(ListView):
    model = Course
    template_name = 'materials/courses_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'materials/course_detail.html'  # Имя вашего шаблона HTML
    context_object_name = 'course'


class LessonCreateView(CreateView):
    model = Lesson
    fields = ['title', 'content']
    template_name = 'materials/lesson_form.html'

    def get_success_url(self):
        return reverse_lazy('user:profile', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Получаем ID курса из URL
        course_id = self.kwargs['course_id']
        # Сохраняем урок и устанавливаем курс
        form.instance.course_id = course_id
        # Сохраняем урок
        super().form_valid(form)
        # Получаем данные из формы
        data = self.request.POST
        # Итерируемся по данным, чтобы найти вопросы и ответы
        for key, value in data.items():
            if key.startswith('question_'):
                # Получаем индекс вопроса
                index = key.split('_')[1]
                # Получаем текст вопроса и ответа по этому индексу
                question = value
                answer = data['answer_' + index]
                # Создаем объект Answer и сохраняем его в базе данных
                Answer.objects.create(
                    lesson=form.instance, question=question, correct_answer=answer)
        return redirect(self.get_success_url('user:profile', kwargs={'pk': self.object.pk}))


class LessonDetailView(DetailView):
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


class LessonListView(ListView):
    model = Lesson
    template_name = 'materials/lesson_list.html'
    context_object_name = 'lessons'
