import numpy as np

from OpenGL.GL import *
from vectors import vec3
from transform import transform
from material import material
from texture2D import renderTargetDepth


class scene:
    def __init__(self, cam):
        self.objects = []
        self.light_transform = transform()
        self.orthographic_projection = None
        self.light_color = vec3(0.5, 0.5, 0.5)
        self.cam = cam
        self.shadowmap_material = material()
        self.shadowmap_material.load_shaders("shaders/shadow_vertex.txt", "shaders/shadow_fragement.txt", False)

        self.shadowmap = renderTargetDepth(2048, 2048)

        self.shadowmap_material.add_uniform("model_matrix")
        self.shadowmap_material.add_uniform("light_matrix")
        self.shadowmap_material.add_uniform("light_projection_matrix")

    def setup_shadow_map(self):
        self.light_transform.update()

        self.shadowmap_material.bind_shader()
        self.shadowmap_material.uniformMatrix4("light_matrix", self.light_transform.getransformationasarray())
        # set up orthographic projection since it is directional light
        l = -10
        r = 10
        b = -10
        t = 10
        n = -10
        f = 10
        self.orthographic_projection = np.array([2.0 / (r - l), 0.0, 0.0, 0.0,
                                                 0.0, 2.0 / (t - b), 0.0, 0.0,
                                                 0.0, 0.0, -2.0 / (f - n), 0.0,
                                                 -(r + l) / (r - l), -(t + b) / (t - b), -(f + n) / (f - n), 1.0],
                                                dtype=np.float32)
        self.shadowmap_material.uniformMatrix4("light_projection_matrix", self.orthographic_projection)
        self.shadowmap_material.unbind()

    def add_object(self, obj):
        lightdir = self.light_transform.getforward()
        obj.updatelightdirection(lightdir.vec[0], lightdir.vec[1], lightdir.vec[2])
        obj.updateprojection(self.cam.projection.matrix)
        obj.updatelightcolor(self.light_color.vec[0], self.light_color.vec[1], self.light_color.vec[2])
        obj.updateshadowmapmatrices(self.orthographic_projection, self.light_transform.getransformationasarray())
        self.objects.append(obj)

    def inputs(self):
        self.cam.inputs()
        for _, obj in enumerate(self.objects):
            obj.inputs()

    def update(self, tick_time):
        self.cam.updatetransform()
        campos = self.cam.getcameraposition()
        for _, obj in enumerate(self.objects):
            obj.updateview(self.cam.mtransfrom.getransformationasarray())
            obj.updatecarapos(campos.vec[0], campos.vec[1], campos.vec[2])
            obj.updatemodeltransform()
            if obj.is_instance:
                obj.updatetime(tick_time)

    def render_shadow_map(self):
        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        self.shadowmap.userendertarget()
        glClear(GL_DEPTH_BUFFER_BIT)
        for _, obj in enumerate(self.objects):
            self.shadowmap_material.bind_shader()
            self.shadowmap_material.uniformMatrix4("model_matrix", obj.model_transform.getransformationasarray())
            if obj.is_instance:
                obj.generaldraw_instance()
            else:
                obj.generaldraw()
            self.shadowmap_material.unbind()
        self.shadowmap.stoperendertarget()
        glCullFace(GL_BACK)
        glDisable(GL_CULL_FACE)

    def render(self):
        self.shadowmap.use_target_texture(GL_TEXTURE0)
        for _, obj in enumerate(self.objects):
            if obj.backfaceculling:
                glEnable(GL_CULL_FACE)
                glFrontFace(GL_CW)
                glCullFace(GL_BACK)
            else:
                glDisable(GL_CULL_FACE)

            if obj.is_instance:
                obj.draw_instance()
            else:
                obj.draw()




