.. auto{directivetype}:: {{ fullname }}
    :noindex:
    {% if members %}
    :members:
    {% endif %}
    {% if inherited_members %}
    :inherited-members:
    {% endif %}
    {% if show_inheritance %}
    :show-inheritance:
    {% endif %}

{% block methods %}
.. rubric:: Methods

.. automethod:: {{ fullname }}
{% endblock %}

{% block properties %}
.. rubric:: Properties

.. autoattribute:: {{ fullname }}
{% endblock %}
