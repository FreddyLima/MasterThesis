from revolve2.core.modular_robot import ModularRobot, ActiveHinge, Body, Brick
import numpy as np


def make_body_salamander():
    body = Body()
    body.core._id = 1

    body.core.left = ActiveHinge(np.pi / 2.0)
    body.core.left._id = 2

    body.core.left.attachment = ActiveHinge(-np.pi / 2.0)
    body.core.left.attachment._id = 3

    body.core.right = ActiveHinge(0.0)
    body.core.right._id = 4

    body.core.back = ActiveHinge(np.pi / 2.0)
    body.core.back._id = 5

    body.core.back.attachment = Brick(-np.pi / 2.0)
    body.core.back.attachment._id = 6

    body.core.back.attachment.left = ActiveHinge(0.0)
    body.core.back.attachment.left._id = 7

    body.core.back.attachment.front = Brick(0.0)
    body.core.back.attachment.front._id = 8


    body.core.back.attachment.front.left = ActiveHinge(0.0)
    body.core.back.attachment.front.left._id = 9

    body.core.back.attachment.front.front = ActiveHinge(np.pi / 2.0)
    body.core.back.attachment.front.front._id = 10

    body.core.back.attachment.front.front.attachment = Brick(-np.pi / 2.0)
    body.core.back.attachment.front.front.attachment._id = 11

    body.core.back.attachment.front.front.attachment.left = ActiveHinge(0.0)
    body.core.back.attachment.front.front.attachment.left._id = 12

    body.core.back.attachment.front.front.attachment.left.attachment = Brick(0.0)
    body.core.back.attachment.front.front.attachment.left.attachment._id = 13

    body.core.back.attachment.front.front.attachment.left.attachment.left = Brick(0.0)
    body.core.back.attachment.front.front.attachment.left.attachment.left._id = 14

    body.core.back.attachment.front.front.attachment.left.attachment.front = (
        ActiveHinge(np.pi / 2.0)
    )
    body.core.back.attachment.front.front.attachment.left.attachment.front._id = 15

    body.core.back.attachment.front.front.attachment.left.attachment.front.attachment = ActiveHinge(
        -np.pi / 2.0
    )
    body.core.back.attachment.front.front.attachment.left.attachment.front.attachment._id = 16

    body.core.back.attachment.front.front.attachment.front = Brick(0.0)
    body.core.back.attachment.front.front.attachment.front._id = 17

    body.core.back.attachment.front.front.attachment.front.left = ActiveHinge(0.0)
    body.core.back.attachment.front.front.attachment.front.left._id = 18

    body.core.back.attachment.front.front.attachment.front.front = Brick(0.0)
    body.core.back.attachment.front.front.attachment.front.front._id = 19

    body.core.back.attachment.front.front.attachment.front.front.left = ActiveHinge(0.0)
    body.core.back.attachment.front.front.attachment.front.front.left._id = 20

    body.core.back.attachment.front.front.attachment.front.front.front = Brick(0.0)
    body.core.back.attachment.front.front.attachment.front.front.front._id = 21

    body.core.back.attachment.front.front.attachment.front.front.front.front = (
        ActiveHinge(np.pi / 2.0)
    )
    body.core.back.attachment.front.front.attachment.front.front.front.front._id = 22

    body.core.back.attachment.front.front.attachment.front.front.front.front.attachment = Brick(
        -np.pi / 2.0
    )
    body.core.back.attachment.front.front.attachment.front.front.front.front.attachment._id = 23

    body.core.back.attachment.front.front.attachment.front.front.front.front.attachment.left = Brick(
        0.0
    )
    body.core.back.attachment.front.front.attachment.front.front.front.front.attachment.left._id = 24

    body.core.back.attachment.front.front.attachment.front.front.front.front.attachment.front = ActiveHinge(
        np.pi / 2.0
    )
    body.core.back.attachment.front.front.attachment.front.front.front.front.attachment.front._id = 25

    body.finalize()
    return body

