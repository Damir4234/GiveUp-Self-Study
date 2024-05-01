from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from user.models import User
from materials.models import Answer, Course, Lesson


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
