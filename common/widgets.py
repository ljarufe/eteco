#-*- coding: utf-8 -*-

from django.forms.widgets import SelectMultiple, CheckboxInput
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


class CheckboxServicios(SelectMultiple):
    """
    Muestra un lista de checkbox de lso servicios ordenados por sistemas
    """
    def __init__(self, servicios, *args, **kwargs):
        self.servicios = servicios
        super(self.__class__, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        str_values = set([force_unicode(v) for v in value])
        i = 0
        for sistema in self.servicios:
            output.append(u"<h3>%s</h3>" % sistema["sistema"])
            choices = [(servicio.id, servicio.nombre) for servicio in sistema["servicios"]]
            for (option_value, option_label) in choices:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
                cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
                option_value = force_unicode(option_value)
                rendered_cb = cb.render(name, option_value)
                option_label = conditional_escape(force_unicode(option_label))
                output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
                i += 1
        output.append(u'</ul>')

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_