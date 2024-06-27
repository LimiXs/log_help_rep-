MAPPING = {
        'A': 'А',
        'B': 'В',
        'C': 'С',
        'E': 'Е',
        'H': 'Н',
        'K': 'К',
        'M': 'М',
        'O': 'О',
        'P': 'Р',
        'T': 'Т',
        'X': 'Х',
        'Y': 'У',
    }


class DataMixin:
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('posts'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context