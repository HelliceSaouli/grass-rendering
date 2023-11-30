from staticmodel import staticmodel

import pyassimp as simp
import numpy as np
import pyassimp.postprocess as process


def loadmodel(path):
    fullmodel = staticmodel()
    print("start loading")
    scene = simp.load(path, processing=process.aiProcess_Triangulate | process.aiProcess_JoinIdenticalVertices)
    if scene is None:
        print(f" Failed to load the mesh {path}")
        return

    numberofmeshes = len(scene.meshes)
    numberofmatrials = len(scene.materials)
    fullmodel.init_model(numberofmeshes, numberofmatrials)

    for index, pmesh in enumerate(scene.meshes):
        buffer = []
        indices = []

        for idx in range(0, len(pmesh.vertices)):
            position = pmesh.vertices[idx]
            uvs = [0, 0]
            normal = [0, 1, 0]

            if pmesh.texturecoords.any():
                uvs = pmesh.texturecoords[0][idx]

            if pmesh.normals.any():
                normal = pmesh.normals[idx]

            buffer.append(position[0])
            buffer.append(position[1])
            buffer.append(position[2])

            buffer.append(normal[0])
            buffer.append(normal[1])
            buffer.append(normal[2])

            buffer.append(uvs[0])
            buffer.append(uvs[1])

        for idx in range(0, len(pmesh.faces)):
            face = pmesh.faces[idx]
            indices.append(face[0])
            indices.append(face[1])
            indices.append(face[2])

        npbuffer = np.array(buffer, dtype=np.float32)
        npindices = np.array(indices, dtype=np.int32)
        del buffer
        del indices
        fullmodel.add_mesh(npbuffer, npindices, pmesh.materialindex, index)
    print("loading Model complete")
    return fullmodel
