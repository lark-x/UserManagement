from django import forms


class BootStrapModelForm(forms.ModelForm):
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件,添加class
        for name, field in self.fields.items():
            # if name in ['create_time']:
            #     continue
            if name in self.bootstrap_exclude_fields:
                continue
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': '请输入' + field.label
                }


class BootStrapForm(forms.Form):
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件,添加class
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            # if name in ['create_time']:
            #     continue
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': '请输入' + field.label
                }
