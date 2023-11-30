from transform import transform
from vectors import vec3, mat4
import numpy as np
import pygame as pg


class camera:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.mtransfrom = transform()
        self.projection = mat4()
        self.projection.zero()

    def setprojection(self, fov=45.0, near=0.01, far=1000.0):
        aratio = self.w / self.h
        hfov = np.deg2rad(fov) * 0.5
        viewrange = near - far
        focallength = np.tan(hfov)
        self.projection.matrix[0] = 1.0 / focallength
        self.projection.matrix[5] = 1.0 / focallength * aratio
        self.projection.matrix[10] = (-near - far) / viewrange
        self.projection.matrix[14] = 2.0 * near * far / viewrange
        self.projection.matrix[11] = 1.0

    def updatetransform(self):
        self.mtransfrom.update_camera_view_matrix()
        self.mtransfrom.fulltransform.matrix[12] = - self.mtransfrom.fulltransform.matrix[12]
        self.mtransfrom.fulltransform.matrix[13] = - self.mtransfrom.fulltransform.matrix[13]
        self.mtransfrom.fulltransform.matrix[14] = - self.mtransfrom.fulltransform.matrix[14]

    def setcameraposition(self, x, y, z):
        self.mtransfrom.translate(x, y, z)

    def getcameraleft(self):
        up = self.mtransfrom.getup().normalized()
        forward = self.mtransfrom.getforward().normalized()
        return forward.cross(up).normalized()

    def getcameraright(self):
        up = self.mtransfrom.getup().normalized()
        forward = self.mtransfrom.getforward().normalized()
        return up.cross(forward).normalized()

    def cameralookat(self, target):
        foraward = target.sub(self.getcameraposition())
        foraward = foraward.normalized()
        yaxis = vec3(0.0, 1.0, 0.0)
        haxis = yaxis.cross(foraward)
        up = foraward.cross(haxis)
        up = up.normalized()
        right = up.cross(foraward).normalized()
        self.mtransfrom.rotationfromaxes(foraward, up, right)
        self.updatetransform()

    def getcameraposition(self):
        return self.mtransfrom.getpoisiton()

    def movecamera(self, direction, distance):
        currentpos = self.getcameraposition()
        newpos = currentpos.add(direction.mul_scalar(distance))
        self.mtransfrom.translate(newpos.vec[0], newpos.vec[1], newpos.vec[2])

    def camera_add_input_pitch(self, senstive, amount):
        pitch = np.deg2rad(senstive * amount)
        yaxis = vec3(0.0, 1.0, 0.0)
        forward = self.mtransfrom.getforward()
        haxis = yaxis.cross(forward)
        haxis = haxis.normalized()
        forward = forward.rotate(pitch, haxis)
        forward = forward.normalized()
        up = forward.cross(haxis)
        up = up.normalized()
        self.mtransfrom.rotationfromaxes(forward, up, self.getcameraright())

    def camera_add_input_yaw(self, senstive, amount):
        yaw = np.deg2rad(senstive * amount)
        yaxis = vec3(0.0, 1.0, 0.0)
        forward = self.mtransfrom.getforward()
        haxis = yaxis.cross(forward)
        forward = forward.rotate(yaw, yaxis)
        forward = forward.normalized()
        up = forward.cross(haxis)
        up = up.normalized()
        self.mtransfrom.rotationfromaxes(forward, up, self.getcameraright())

    def inputs(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_q]:
            left = self.getcameraleft()
            self.movecamera(left, 1.5 * 1 / 60)
            print(self.mtransfrom.getpoisiton())

        if keys[pg.K_d]:
            right = self.getcameraright()
            self.movecamera(right, 1.5 * 1 / 60)
            print(self.mtransfrom.getpoisiton())

        if keys[pg.K_z]:
            forward = self.mtransfrom.getforward()
            self.movecamera(forward, 1.5 * 1 / 60)
            print(self.mtransfrom.getpoisiton())

        if keys[pg.K_s]:
            backward = (self.mtransfrom.getforward()).mul_scalar(-1.0)
            self.movecamera(backward, 1.5 * 1 / 60)
            print(self.mtransfrom.getpoisiton())

        if keys[pg.K_UP]:
            self.camera_add_input_pitch(1.0, 0.5)

        if keys[pg.K_DOWN]:
            self.camera_add_input_pitch(-1.0, 0.5)

        if keys[pg.K_RIGHT]:
            self.camera_add_input_yaw(1.0, 0.5)

        if keys[pg.K_LEFT]:
            self.camera_add_input_yaw(-1.0, 0.5)
