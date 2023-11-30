import numpy as np
from OpenGL.GL import *


class mesh:
    def __init__(self):
        self.vertex_buffer_object = 0
        self.vertex_array_object = 0
        self.element_buffer_object = 0
        self.buffer_size = 0
        self.number_of_indices = 0
        self.matrial_index = 0

    def create_mesh_from_buffer(self, vertices, indices, vertixsize):
        self.buffer_size = len(vertices)
        self.number_of_indices = len(indices)

        # create vao
        self.vertex_array_object = glGenVertexArrays(1)
        glBindVertexArray(self.vertex_array_object)

        self.vertex_buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_object)

        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertixsize * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Normals
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertixsize * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)

        # uv
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, vertixsize * 4, ctypes.c_void_p(6 * 4))
        glEnableVertexAttribArray(2)

        self.element_buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer_object)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vertex_array_object)
        # passing 0 like C++ will not work None must be used
        glDrawElements(GL_TRIANGLES, self.number_of_indices, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def draw_instance(self, batch):
        glBindVertexArray(self.vertex_array_object)
        # passing 0 like C++ will not work None must be used
        glDrawElementsInstanced(GL_TRIANGLES, self.number_of_indices, GL_UNSIGNED_INT, None, batch)
        glBindVertexArray(0)