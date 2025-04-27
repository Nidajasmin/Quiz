from django.contrib import admin
from .models import Quiz, Question, Option, UserQuiz

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  
    min_num = 4
    max_num = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserQuiz)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


