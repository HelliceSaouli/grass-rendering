import numpy as np
from vectors import mat4, vec3
import math


class transform:
    def __init__(self):
        self.position = mat4()
        self.rotation = mat4()
        self.scaling = mat4()
        self.fulltransform = mat4()

    def getransformationasarray(self):
        return self.fulltransform.matrix

    def scale(self, sx, sy, sz):
        self.scaling.matrix[0] = sx
        self.scaling.matrix[5] = sy
        self.scaling.matrix[10] = sz

    def translate(self, x, y, z):
        self.position.matrix[12] = x
        self.position.matrix[13] = y
        self.position.matrix[14] = z

    def rotate(self, rx, ry, rz):
        x_angle_rad = math.radians(rx)
        y_angle_rad = math.radians(ry)
        z_angle_rad = math.radians(rz)

        c1 = np.cos(x_angle_rad)
        s1 = np.sin(x_angle_rad)
        c2 = np.cos(y_angle_rad)
        s2 = np.sin(y_angle_rad)
        c3 = np.cos(z_angle_rad)
        s3 = np.sin(z_angle_rad)

        self.rotation = mat4(c2 * c3, c1 * s3 + c3 * s1 * s2, s1 * s3 - c1 * c3 * s2, 0,
                             -c2 * s3, c1 * c3 - s1 * s2 * s3, c3 * s1 + c1 * s2 * s3, 0,
                             s2, -c2 * s1, c1 * c2, 0,
                             0, 0, 0, 1)

    def rotationfromaxes(self, forward, up, right):

        self.rotation.matrix[2] = forward.vec[0]
        self.rotation.matrix[6] = forward.vec[1]
        self.rotation.matrix[10] = forward.vec[2]

        self.rotation.matrix[1] = up.vec[0]
        self.rotation.matrix[5] = up.vec[1]
        self.rotation.matrix[9] = up.vec[2]

        self.rotation.matrix[0] = right.vec[0]
        self.rotation.matrix[4] = right.vec[1]
        self.rotation.matrix[8] = right.vec[2]

    def getpoisiton(self):
        return vec3(self.position.matrix[12], self.position.matrix[13], self.position.matrix[14])

    def getscale(self):
        return vec3(self.scaling.matrix[0], self.scaling.matrix[5], self.scaling.matrix[10])

    def getforward(self):
        return vec3(self.rotation.matrix[2], self.rotation.matrix[6], self.rotation.matrix[10])

    def getup(self):
        return vec3(self.rotation.matrix[1], self.rotation.matrix[5], self.rotation.matrix[9])

    def getright(self):
        return vec3(self.rotation.matrix[0], self.rotation.matrix[4], self.rotation.matrix[8])

    def update(self):
        self.fulltransform = (self.scaling.mult4x4(self.rotation)).mult4x4(self.position)

    def update_camera_view_matrix(self):
        self.fulltransform = self.position.mult4x4(self.rotation)

    pass
