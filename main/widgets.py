from django.forms.widgets import Textarea, CheckboxInput


class LimitedLengthTextarea(Textarea):
    def render(self, name, value, attrs, renderer, max_length=1000):
        symbols_left_label = f'<p class="symbols_left_label">осталось символов: {max_length}</p>'
        return super().render(name, value, attrs, renderer) + '\n' + symbols_left_label


class ACCheckBox(CheckboxInput):
    def __init__(self, label, attrs={}, check_test=None):
        super().__init__(attrs, check_test)
        self.label = label

    def render(self, name, value, attrs, renderer):
        attrs['class'] = 'checkbox_input'
        return f'<p class="checkbox_label">{super().render(name, value, attrs, renderer)} {self.label}</p>'
