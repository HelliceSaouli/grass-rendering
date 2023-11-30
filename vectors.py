import numpy as np


class quaternion:
    def __init__(self, x, y, z, w):
        self.q = np.array([x, y, z, w], dtype=np.float32)

    def __repr__(self):
        return f"q{self.vec}"

    def magnitude(self):
        return np.sqrt(self.q[0] * self.q[0] + self.q[1] * self.q[1] + self.q[2] * self.q[2] + self.q[3] * self.q[3])

    def normalize(self):
        mag = self.magnitude()
        self.q[0] = self.q[0] / mag
        self.q[1] = self.q[1] / mag
        self.q[2] = self.q[2] / mag
        self.q[3] = self.q[3] / mag

    def conjugate(self):
        return quaternion(-self.q[0], -self.q[1], -self.q[2], self.q[3])

    def qmulq(self, b):
        _w = self.q[3] * b.q[3] - self.q[0] * b.q[0] - self.q[1] * b.q[1] - self.q[2] * b.q[2]
        _x = self.q[0] * b.q[3] + self.q[3] * b.q[0] + self.q[1] * b.q[2] - self.q[2] * b.q[1]
        _y = self.q[1] * b.q[3] + self.q[3] * b.q[1] + self.q[2] * b.q[0] - self.q[0] * b.q[2]
        _z = self.q[2] * b.q[3] + self.q[3] * b.q[2] + self.q[0] * b.q[1] - self.q[1] * b.q[0]
        return quaternion(_x, _y, _z, _w)

    def qmulv(self, b):
        _w = -self.q[0] * b.vec[0] - self.q[1] * b.vec[1] - self.q[2] * b.vec[2]
        _x = self.q[3] * b.vec[0] + self.q[1] * b.vec[2] - self.q[2] * b.vec[1]
        _y = self.q[3] * b.vec[1] + self.q[2] * b.vec[0] - self.q[0] * b.vec[2]
        _z = self.q[3] * b.vec[2] + self.q[0] * b.vec[1] - self.q[1] * b.vec[0]
        return quaternion(_x, _y, _z, _w)


class vec3:
    def __init__(self, x, y, z):
        self.vec = np.array([x, y, z], dtype=np.float32)

    def __repr__(self):
        return f"vec3{self.vec}"

    def mul_scalar(self, scalar):
        return vec3(self.vec[0] * scalar, self.vec[1] * scalar, self.vec[2] * scalar)

    def add(self, b):
        if isinstance(b, vec3):
            return vec3(self.vec[0] + b.vec[0], self.vec[1] + b.vec[1], self.vec[2] + b.vec[2])
        else:
            return vec3(self.vec[0] + b, self.vec[1] + b, self.vec[2] + b)

    def sub(self, b):
        if isinstance(b, vec3):
            return vec3(self.vec[0] - b.vec[0], self.vec[1] - b.vec[1], self.vec[2] - b.vec[2])
        else:
            return vec3(self.vec[0] - b, self.vec[1] - b, self.vec[2] - b)

    def dot(self, b):
        if isinstance(b, vec3):
            return self.vec[0] * b.vec[0] + self.vec[1] * b.vec[1] + self.vec[2] * b.vec[2]
        else:
            b = vec3(b, b, b)
            return self.vec[0] * b.vec[0] + self.vec[1] * b.vec[1] + self.vec[2] * b.vec[2]

    def cross(self, b):
        if isinstance(b, vec3):
            b = b
        else:
            b = vec3(b, b, b)

        c = vec3(0.0, 0.0, 0.0)
        c.vec[0] = self.vec[1] * b.vec[2] - self.vec[2] * b.vec[1]
        c.vec[1] = self.vec[2] * b.vec[0] - self.vec[0] * b.vec[2]
        c.vec[2] = self.vec[0] * b.vec[1] - self.vec[1] * b.vec[0]
        return c

    def magnitude(self):
        return np.sqrt(self.dot(self))

    def normalized(self):
        mag = 1.0 / self.magnitude()
        return self.mul_scalar(mag)

    def rotate(self, angleinradiant, axis):
        sinhalfangle = np.sin(angleinradiant * 0.5)
        coshalfangle = np.cos(angleinradiant * 0.5)
        rotation = quaternion(axis.vec[0] * sinhalfangle, axis.vec[1] * sinhalfangle, axis.vec[2] * sinhalfangle,
                              coshalfangle)
        rotconj = rotation.conjugate()
        rotator = (rotation.qmulv(self)).qmulq(rotconj)
        return vec3(rotator.q[0], rotator.q[1], rotator.q[2])


class mat4:
    def __init__(self, m00=1.0, m01=0.0, m02=0.0, m03=0.0,
                 m10=0.0, m11=1.0, m12=0.0, m13=0.0,
                 m20=0.0, m21=0.0, m22=1.0, m23=0.0,
                 m30=0.0, m31=0.0, m32=0.0, m33=1.0):
        self.matrix = np.array([m00, m01, m02, m03,
                                m10, m11, m12, m13,
                                m20, m21, m22, m23,
                                m30, m31, m32, m33], dtype=np.float32)

    def zero(self):
        self.matrix = np.array([0, 0, 0, 0,
                                0, 0, 0, 0,
                                0, 0, 0, 0,
                                0, 0, 0, 0], dtype=np.float32)

    def __repr__(self):
        return f"[{self.matrix[0]}, {self.matrix[4]}, {self.matrix[8]}, {self.matrix[12]},\n" \
               f"{self.matrix[1]}, {self.matrix[5]}, {self.matrix[9]}, {self.matrix[13]},\n" \
               f"{self.matrix[2]}, {self.matrix[6]}, {self.matrix[10]}, {self.matrix[14]},\n" \
               f"{self.matrix[3]}, {self.matrix[7]}, {self.matrix[11]}, {self.matrix[15]}]"

    def mult4x4(self, b):
        res = mat4()
        res.zero()
        for col in range(0, 4):
            for row in range(0, 4):
                i = row + col * 4
                res.matrix[i] = (self.matrix[0 + col * 4] * b.matrix[row + 0 * 4]) + \
                                (self.matrix[1 + col * 4] * b.matrix[row + 1 * 4]) + \
                                (self.matrix[2 + col * 4] * b.matrix[row + 2 * 4]) + \
                                (self.matrix[3 + col * 4] * b.matrix[row + 3 * 4])
        return res

    pass
