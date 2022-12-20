import random

import pytest
from django.conf import settings
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def students_limit():
    return settings.MAX_STUDENTS_PER_COURSE


@pytest.mark.django_db
def test_get_course(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.get(f"/api/v1/courses/{course[0].id}/")
    data = response.json()
    assert response.status_code == 200
    assert course[0].name == data['name']


@pytest.mark.django_db
def test_get_list(client, course_factory):
    course = course_factory(_quantity=10)
    response = client.get("/api/v1/courses/")
    data = response.json()
    assert response.status_code == 200
    assert type(course) == type(data)
    assert len(course) == len(data)


@pytest.mark.django_db
def test_id_filter(client, course_factory):
    course = course_factory(_quantity=10)
    random_id = random.choice([i.id for i in course])
    response = client.get(f"/api/v1/courses/?id={random_id}")
    data = response.json()
    assert response.status_code == 200
    assert 'id' and 'name' and 'students' in data[0]
    assert random_id == data[0]['id']


@pytest.mark.django_db
def test_name_filter(client, course_factory):
    course = course_factory(_quantity=10)
    random_name = random.choice([n.name for n in course])
    response = client.get(f"/api/v1/courses/?name={random_name}")
    data = response.json()
    assert response.status_code == 200
    assert 'id' and 'name' and 'students' in data[0]
    assert random_name == data[0]['name']


@pytest.mark.django_db
def test_create_course(client):
    course = Course.objects.create(name='Python')
    response = client.get("/api/v1/courses/")
    data = response.json()
    assert response.status_code == 200
    assert course.name == data[0]['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=10)
    course_id = random.choice(course).id
    request = client.patch(path=f"/api/v1/courses/{course_id}/", data={"name": "Django"})
    assert request.status_code == 200
    response = client.get(path=f"/api/v1/courses/{course_id}/")
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == 'Django'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=10)
    course_id = random.choice(course).id
    client.delete(f"/api/v1/courses/{course_id}/")
    response = client.get(f"/api/v1/courses/{course_id}/")
    assert response.status_code == 404
