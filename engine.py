import numpy as np
import pygame as pg
import random as rng
import util

from OpenGL.GL import *

from camera import camera
from vectors import vec3
from transform import transform

from trenderdepthmap import trenderdepthmap
from scene import scene
from defines import SC_WIDTH, SC_HIGHT


class engine:
    def __init__(self, screen=(SC_WIDTH, SC_HIGHT), app_title='Demo'):
        pg.init()
        pg.display.set_caption(app_title)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 2)

        pg.display.set_mode(screen, pg.OPENGL | pg.DOUBLEBUF | pg.OPENGLBLIT)
        self.clock = pg.time.Clock()
        glClearColor(0.5, 0.7, 1.0, 1.0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)

        # set up camera
        cam = camera(screen[0], screen[1])
        cam.setprojection(39.5978, 0.5, 1000.0)
        cam.setcameraposition(5.0, 2.5, -5.0)
        cam.cameralookat(vec3(0.0, 0.0, 0.0))

        self.myscene = scene(cam)
        del cam

        self.myscene.light_color = vec3(0.8, 0.8, 0.8)
        self.myscene.light_transform.rotate(45.0, 0.0, 45.0)
        self.myscene.setup_shadow_map()

        mymodel = util.loadmodel("models/TestCube/Box.gltf")
        mymodel2 = util.loadmodel("models/TestCube/Box.gltf")
        mygrass = util.loadmodel("models/grassblade/blade2.gltf")

        mymodel.backfaceculling = True
        mymodel2.backfaceculling = True
        mygrass.backfaceculling = False

        mygrass.is_instance = True

        plane_size = 300
        unit_distance = 0.1
        center_offset = plane_size / 2.0 - 0.5

        mygrass.batch = plane_size * plane_size

        model_instances = []
        #offsetposition = []
        for x in range(plane_size):
            for z in range(plane_size):
                grasstrans = transform()
                posx = (x - center_offset) * unit_distance
                posz = (z - center_offset) * unit_distance
                #position = vec3(posx + rng.random(), 0.0, posz + rng.random())
                grasstrans.translate(posx + rng.random(), 0.5,  posz + rng.random())
                grasstrans.rotate(rng.uniform(-35.0, 45.0), rng.uniform(0.0, 360), 0.0)
                grasstrans.scale(3, rng.uniform(0.5, 5.5), 1)
                grasstrans.update()
                model_instances.extend(grasstrans.getransformationasarray())
                # the offset will contain scale in w
                #offsetposition.extend([position.vec[0], position.vec[1], position.vec[2], 0.5 + rng.random()])
        model_instances = np.array(model_instances, dtype=np.float32)
        #offsetposition = np.array(offsetposition, dtype=np.float32)

        for i in range(0, len(mymodel.matrial_parts)):
            mymodel.matrial_parts[i].load_shaders("shaders/simple_vertex.txt", "shaders/simple_fragement.txt")
            mymodel.matrial_parts[i].set_albedo_texture("models/TestCube/dirt_texture.jpg")

        for i in range(0, len(mymodel2.matrial_parts)):
            mymodel2.matrial_parts[i].load_shaders("shaders/simple_vertex.txt", "shaders/simple_fragement.txt")
            mymodel2.matrial_parts[i].set_albedo_texture("models/grassblade/grass-green-color.png")

        for i in range(0, len(mygrass.matrial_parts)):
            mygrass.matrial_parts[i].load_shaders("shaders/instancing_vertex.txt",
                                                  "shaders/instancing_fragement.txt")
            mygrass.matrial_parts[i].set_albedo_texture("models/grassblade/grass-green-color.png")
            mygrass.matrial_parts[i].add_uniform("time")

        mygrass.generate_vbo_transform_instance(model_instances)
        #mygrass.generate_vbo_position_offset_instance(offsetposition)
        mymodel.set_model_position(0.0, -0.5, 0.0)
        mymodel2.set_model_position(0.0, 1.5, 0.0)
        mymodel.set_model_scale(300, 2, 300)

        #mygrass.set_model_position(0.0, 1.5, 0.0)
        #mygrass.set_model_rotation(0, 45, 0)
        #mygrass.set_model_scale(3, 5, 1)

        self.myscene.add_object(mymodel)
        self.myscene.add_object(mymodel2)
        self.myscene.add_object(mygrass)

        del mymodel
        del mygrass

        #self.rendershadwomap = trenderdepthmap()
        self.run()

    def run(self):
        running = True
        while running:
            # check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.inputs()

            self.update()

            self.render()

        self.stop()

    @staticmethod
    def stop():
        pg.quit()

    def inputs(self):
        self.myscene.inputs()

    def update(self):
        self.myscene.update(pg.time.get_ticks())

    def render(self):
        self.myscene.render_shadow_map()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.myscene.render()
        # self.rendershadwomap.render(self.myscene.shadowmap.depth_texture)
        pg.display.flip()
        self.clock.tick(60)
        fps = self.clock.get_fps()
        pg.display.set_caption("FPS Demo - FPS: {:.2f}".format(fps))

