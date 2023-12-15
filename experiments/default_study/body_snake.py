from revolve2.core.modular_robot import ModularRobot, ActiveHinge, Body, Brick
import numpy as np


def make_body_snake():

    body = Body()
    body.core._id = 1

    body.core.left = ActiveHinge(0.0)
    body.core.left._id = 2

    body.core.left.attachment = Brick(0.0)
    body.core.left.attachment._id = 3

    body.core.left.attachment.front = ActiveHinge(np.pi / 2.0)
    body.core.left.attachment.front._id = 4

    body.core.left.attachment.front.attachment = Brick(-np.pi / 2.0)
    body.core.left.attachment.front.attachment._id = 5

    body.core.left.attachment.front.attachment.front = ActiveHinge(0.0)
    body.core.left.attachment.front.attachment.front._id = 6

    body.core.left.attachment.front.attachment.front.attachment = Brick(0.0)
    body.core.left.attachment.front.attachment.front.attachment._id = 7

    body.core.left.attachment.front.attachment.front.attachment.front = ActiveHinge(np.pi / 2.0)
    body.core.left.attachment.front.attachment.front.attachment.front._id = 8

    body.core.left.attachment.front.attachment.front.attachment.front.attachment = (Brick(-np.pi / 2.0))
    body.core.left.attachment.front.attachment.front.attachment.front.attachment._id = 9

    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front = ActiveHinge(0.0)
    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front._id = 10

    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment = Brick(0.0)
    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment._id = 11

    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front = ActiveHinge(np.pi / 2.0)
    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front._id = 12

    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment = Brick(-np.pi / 2.0)
    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment._id = 13

    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front = ActiveHinge(0.0)
    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front._id = 14

    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment = Brick(0.0)
    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment._id = 15

    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front = ActiveHinge(np.pi / 2.0)
    body.core.left.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front._id = 16

    body.finalize()
    return body
