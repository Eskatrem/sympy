from __future__ import division

from sympy.physics.optics.utils import refraction_angle, deviation
from sympy.physics.optics.medium import Medium

from sympy import symbols, sqrt, Matrix
from sympy.geometry.point3d import Point3D
from sympy.geometry.line3d import Ray3D
from sympy.geometry.plane import Plane
from sympy.utilities.pytest import XFAIL


def test_refraction_angle():
    n1, n2 = symbols('n1, n2')
    m1 = Medium('m1')
    m2 = Medium('m2')
    r1 = Ray3D(Point3D(-1, -1, 1), Point3D(0, 0, 0))
    i = Matrix([1, 1, 1])
    n = Matrix([0, 0, 1])
    normal_ray = Ray3D(Point3D(0, 0, 0), Point3D(0, 0, 1))
    P = Plane(Point3D(0, 0, 0), normal_vector=[0, 0, 1])
    assert refraction_angle(r1, 1, 1, n) == Matrix([
                                            [ 1],
                                            [ 1],
                                            [-1]])
    assert refraction_angle([1, 1, 1], 1, 1, n) == Matrix([
                                            [ 1],
                                            [ 1],
                                            [-1]])
    assert refraction_angle((1, 1, 1), 1, 1, n) == Matrix([
                                            [ 1],
                                            [ 1],
                                            [-1]])
    assert refraction_angle(i, 1, 1, [0, 0, 1]) == Matrix([
                                            [ 1],
                                            [ 1],
                                            [-1]])
    assert refraction_angle(i, 1, 1, (0, 0, 1)) == Matrix([
                                            [ 1],
                                            [ 1],
                                            [-1]])
    assert refraction_angle(i, 1, 1, normal_ray) == Matrix([
                                            [ 1],
                                            [ 1],
                                            [-1]])
    assert refraction_angle(i, 1, 1, plane=P) == Matrix([
                                            [ 1],
                                            [ 1],
                                            [-1]])
    assert refraction_angle(r1, 1, 1, plane=P) == \
        Ray3D(Point3D(0, 0, 0), Point3D(1, 1, -1))
    assert refraction_angle(r1, m1, 1.33, plane=P) == \
        Ray3D(Point3D(0, 0, 0), Point3D(100/133, 100/133, -789378201649271*sqrt(3)/1000000000000000))
    assert refraction_angle(r1, 1, m2, plane=P) == \
        Ray3D(Point3D(0, 0, 0), Point3D(1, 1, -1))
    assert refraction_angle(r1, n1, n2, plane=P) == \
        Ray3D(Point3D(0, 0, 0), Point3D(n1/n2, n1/n2, -sqrt(3)*sqrt(-2*n1**2/(3*n2**2) + 1)))
    assert refraction_angle(r1, 1.33, 1, plane=P) == 0  # TIR
    assert refraction_angle(r1, 1, 1, normal_ray) == \
        Ray3D(Point3D(0, 0, 0), direction_ratio=[1, 1, -1])


def test_deviation():
    n1, n2 = symbols('n1, n2')
    m1 = Medium('m1')
    m2 = Medium('m2')
    r1 = Ray3D(Point3D(-1, -1, 1), Point3D(0, 0, 0))
    n = Matrix([0, 0, 1])
    i = Matrix([-1, -1, -1])
    normal_ray = Ray3D(Point3D(0, 0, 0), Point3D(0, 0, 1))
    P = Plane(Point3D(0, 0, 0), normal_vector=[0, 0, 1])
    assert deviation(r1, 1, 1, normal=n) == 0
    assert deviation(r1, 1, 1, plane=P) == 0
    assert deviation(r1, 1, 1.1, plane=P).evalf(3) + 0.119 < 1e-3
    assert deviation(i, 1, 1.1, normal=normal_ray).evalf(3) + 0.119 < 1e-3
    assert deviation(r1, 1.33, 1, plane=P) is None  # TIR
    assert deviation(r1, 1, 1, normal=[0, 0, 1]) == 0
    assert deviation([-1, -1, -1], 1, 1, normal=[0, 0, 1]) == 0
