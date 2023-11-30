from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from texture2D import texture2D


class material:
    def __init__(self):
        self.shader_program = None
        self.uniforms = {}
        self.albedomap = None

    def load_shaders(self, vertex_shader_path, fragement_shader_path, load_uniforms=True):
        with open(vertex_shader_path, 'r') as f:
            vertex_src = f.readlines()

        with open(fragement_shader_path, 'r') as f:
            fragement_src = f.readlines()

        self.shader_program = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                             compileShader(fragement_src, GL_FRAGMENT_SHADER))
        # by default all shaders has  model, view and projection matrices
        if load_uniforms:
            self.add_uniform("model_matrix")
            self.add_uniform("view_matrix")
            self.add_uniform("projection_matrix")
            self.add_uniform("light_direction")
            self.add_uniform("light_color")
            self.add_uniform("camera_position")
            self.add_uniform("light_matrix")
            self.add_uniform("light_projection_matrix")

    def clear_uniforms(self):
        self.uniforms.clear()

    def add_uniform(self, uniform_name):
        uniform_location = glGetUniformLocation(self.shader_program, uniform_name)
        if uniform_location == -1:
            print(f'No uniform with name {uniform_name} is found')
            return
        self.uniforms[uniform_name] = uniform_location

    def uniform1f(self, uniform_name, x):
        glUniform1f(self.uniforms[uniform_name], x)

    def uniform3f(self, uniform_name, x, y, z):
        glUniform3f(self.uniforms[uniform_name], x, y, z)

    def uniformMatrix4(self, uniform_name, matrix4, transpose=GL_FALSE):
        glUniformMatrix4fv(self.uniforms[uniform_name], 1, transpose, matrix4)

    def bind_shader(self):
        glUseProgram(self.shader_program)

    @staticmethod
    def unbind():
        glUseProgram(0)

    # Albedo
    def set_albedo_texture(self, image_name):
        self.albedomap = texture2D()
        self.albedomap.generate_texture_srgb_from_file(image_name)

    def material_use_albedo_texture(self):
        if self.albedomap is not None:
            self.albedomap.use_texture(GL_TEXTURE1)

    pass
