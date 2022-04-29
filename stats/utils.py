import base64
from io import BytesIO

from django.contrib.auth import get_user_model
from auths.models import Zone, School, Subject
import matplotlib.pyplot as plt


User = get_user_model()


def get_user_from_id(val):
    user = User.objects.get(id=val)
    return user


def get_zone_from_id(val):
    zone = Zone.objects.get(id=val)
    return zone


def get_subject_from_id(val):
    subject = Subject.objects.get(id=val)
    return subject


def get_school_from_id(val):
    school = School.objects.get(id=val)
    return school


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph