from transform import transform

from mesh import mesh
from material import material
from OpenGL.GL import *


class staticmodel:
    def __init__(self):
        self.model_parts = []
        self.matrial_parts = []
        self.model_transform = transform()
        self.is_instance = False
        self.backfaceculling = True
        self.batch = 1
        self.matrix_buffer_object = 0  # for instancing

    def init_model(self, num_mesh, num_matrial):
        for ms in range(0, num_mesh):
            part = mesh()
            self.model_parts.append(part)

        for mt in range(0, num_matrial):
            matrial_part = material()
            self.matrial_parts.append(matrial_part)

    def generate_vbo_transform_instance(self, model_matrices):
        #create matrix buffer
        self.matrix_buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.matrix_buffer_object)
        glBufferData(GL_ARRAY_BUFFER, model_matrices.nbytes, model_matrices, GL_DYNAMIC_DRAW)

        for i in range(0, len(self.model_parts)):
            glBindVertexArray(self.model_parts[i].vertex_array_object)
            for j in range(0, 4):
                glVertexAttribPointer(3 + j, 4, GL_FLOAT, GL_FALSE, 16 * 4, ctypes.c_void_p(4 * 4 * j))
                glEnableVertexAttribArray(3 + j)
                glVertexAttribDivisor(3 + j, 1)
            glBindVertexArray(0)

    def generate_vbo_position_offset_instance(self, offsets):
        #create offset buffer
        self.matrix_buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.matrix_buffer_object)
        glBufferData(GL_ARRAY_BUFFER, offsets.nbytes, offsets, GL_DYNAMIC_DRAW)
        for i in range(0, len(self.model_parts)):
            glBindVertexArray(self.model_parts[i].vertex_array_object)
            glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
            glEnableVertexAttribArray(3)
            glVertexAttribDivisor(3, 1)
            glBindVertexArray(0)

    def updatelightdirection(self, x, y, z):
        for i in range(0, len(self.matrial_parts)):
            self.matrial_parts[i].bind_shader()
            self.matrial_parts[i].uniform3f("light_direction", x, y, z)
            self.matrial_parts[i].unbind()

    def updateshadowmapmatrices(self, proj, view):
        for i in range(0, len(self.matrial_parts)):
            self.matrial_parts[i].bind_shader()
            self.matrial_parts[i].uniformMatrix4("light_projection_matrix", proj)
            self.matrial_parts[i].uniformMatrix4("light_matrix", view)
            self.matrial_parts[i].unbind()

    def updatelightcolor(self, x, y, z):
        for i in range(0, len(self.matrial_parts)):
            self.matrial_parts[i].bind_shader()
            self.matrial_parts[i].uniform3f("light_color", x, y, z)
            self.matrial_parts[i].unbind()

    def updatecarapos(self, x, y, z):
        for i in range(0, len(self.matrial_parts)):
            self.matrial_parts[i].bind_shader()
            self.matrial_parts[i].uniform3f("camera_position", x, y, z)
            self.matrial_parts[i].unbind()

    def updateprojection(self, matrix4):
        for i in range(0, len(self.matrial_parts)):
            self.matrial_parts[i].bind_shader()
            self.matrial_parts[i].uniformMatrix4("projection_matrix", matrix4)
            self.matrial_parts[i].unbind()

    def updatemodeltransform(self):
        for i in range(0, len(self.matrial_parts)):
            self.matrial_parts[i].bind_shader()
            self.matrial_parts[i].uniformMatrix4("model_matrix", self.model_transform.getransformationasarray())
            self.matrial_parts[i].unbind()

    def updateview(self, matrix4):
        for i in range(0, len(self.matrial_parts)):
            self.matrial_parts[i].bind_shader()
            self.matrial_parts[i].uniformMatrix4("view_matrix", matrix4)
            self.matrial_parts[i].unbind()

    def updatetime(self, t):
        for i in range(0, len(self.matrial_parts)):
            self.matrial_parts[i].bind_shader()
            self.matrial_parts[i].uniform1f("time", t)
            self.matrial_parts[i].unbind()

    def draw(self):
        for i in range(0, len(self.model_parts)):
            self.matrial_parts[self.model_parts[i].matrial_index].bind_shader()
            self.matrial_parts[self.model_parts[i].matrial_index].material_use_albedo_texture()
            self.model_parts[i].draw()
            self.matrial_parts[self.model_parts[i].matrial_index].unbind()

    def draw_instance(self):
        for i in range(0, len(self.model_parts)):
            self.matrial_parts[self.model_parts[i].matrial_index].bind_shader()
            self.matrial_parts[self.model_parts[i].matrial_index].material_use_albedo_texture()
            self.model_parts[i].draw_instance(self.batch)
            self.matrial_parts[self.model_parts[i].matrial_index].unbind()

    def generaldraw(self):
        #this function is for shadow maps or other global effects
        for i in range(0, len(self.model_parts)):
            self.matrial_parts[self.model_parts[i].matrial_index].material_use_albedo_texture()
            self.model_parts[i].draw()

    def generaldraw_instance(self):
        #this function is for shadow maps or other global effects
        for i in range(0, len(self.model_parts)):
            self.matrial_parts[self.model_parts[i].matrial_index].material_use_albedo_texture()
            self.model_parts[i].draw_instance(self.batch)

    def add_mesh(self, meshvertices, meshindices, matrial_index, indx):
        self.model_parts[indx].matrial_index = matrial_index
        self.model_parts[indx].create_mesh_from_buffer(meshvertices, meshindices, 8)

    def attach_matrial_to_model_part(self, modelidx, material_instance):
        self.matrial_parts[self.model_parts[modelidx].matrial_index] = material_instance

    def set_model_position(self, x, y, z):
        self.model_transform.translate(x, y, z)
        self.model_transform.update()

    def set_model_scale(self, x, y, z):
        self.model_transform.scale(x, y, z)
        self.model_transform.update()

    def set_model_rotation(self, x, y, z):
        self.model_transform.rotate(x, y, z)
        self.model_transform.update()

    def inputs(self):
        pass
