from django.forms.widgets import Textarea

class LimitedLengthTextarea(Textarea):
    def render(self, name, value, attrs, renderer, max_length=1000):
        symbols_left_label = f'<p class="symbols_left_label">осталось символов: {max_length}</p>'
        return super().render(name, value, attrs, renderer) + '\n' + symbols_left_label
