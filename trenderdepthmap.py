import util

from defines import SC_WIDTH, SC_HIGHT
from OpenGL.GL import *


class trenderdepthmap:
    def __init__(self):
        self.quad = util.loadmodel("models/TwoSidedPlane/glTF/TwoSidedPlane.gltf")
        for i in range(0, len(self.quad.matrial_parts)):
            self.quad.matrial_parts[i].load_shaders("shaders/map_vertex.txt", "shaders/map_fragement.txt", False)

    def render(self, texture):
        glViewport(0, 0, 512, 512)
        texture.use_texture(GL_TEXTURE0)
        self.quad.draw()
        glViewport(0, 0, SC_WIDTH, SC_HIGHT)
