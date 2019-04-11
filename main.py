import os
import sys

from direct.showbase.ShowBase import ShowBase
import panda3d
import pman.shim

from panda3d.core import NodePath
from panda3d.core import Vec3
from panda3d.core import VBase4
from panda3d.core import DirectionalLight
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletDebugNode

panda3d.core.load_prc_file(
    panda3d.core.Filename.expand_from('$MAIN_DIR/settings.prc')
)


class GameApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        pman.shim.init(self)
        self.accept('escape', sys.exit)

        self.physics_world = BulletWorld()
        self.physics_world.setGravity(Vec3(0, 0, -9.81))
        base.taskMgr.add(self.update_physics, 'physics', sort=0)

        environment = Environment(self)
        vehicle = Vehicle(self, "assets/diamond")
        vehicle.place(Vec3(0, 0, 3))
        camera = CameraController(self, base.cam, vehicle)
        base.task_mgr.add(camera.update, "camera", sort=1)

        self.bullet_debug()

    def update_physics(self, task):
        dt = globalClock.getDt()
        self.physics_world.doPhysics(dt)
        return task.cont

    def bullet_debug(self):
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = self.render.attachNewNode(debugNode)
        debugNP.show()

        self.physics_world.setDebugNode(debugNP.node())


class Environment:
    def __init__(self, app):
        self.app = app

        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        node = BulletRigidBodyNode('Ground')
        node.addShape(shape)
        np = self.app.render.attach_new_node(node)
        np.setPos(0, 0, 0)
        self.app.physics_world.attachRigidBody(node)

        model = loader.load_model("models/box")
        model.reparent_to(np)
        model.set_pos(-50, -50, -1)
        model.set_sx(100)
        model.set_sy(100)

        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(0.8, 0.8, 0.5, 1))
        dlnp = self.app.render.attachNewNode(dlight)
        dlnp.setHpr(20, -75, 0)
        self.app.render.setLight(dlnp)


class Vehicle:
    def __init__(self, app, model_file):
        self.app = app

        model = app.loader.load_model(model_file)

        self.physics_node = BulletRigidBodyNode('vehicle')
        self.physics_node.setMass(1.0)
        # mesh = BulletTriangleMesh()
        # for geom in model.node().get_child(0).get_geoms():
        #     mesh.addGeom(geom)
        # shape = BulletTriangleMeshShape(mesh, dynamic=False)
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        self.physics_node.addShape(shape)
        self.vehicle = NodePath(self.physics_node)

        model.reparent_to(self.vehicle)

    def place(self, coordinate):
        self.vehicle.reparent_to(self.app.render)
        self.vehicle.set_pos(coordinate)
        self.app.physics_world.attachRigidBody(self.physics_node)

    def np(self):
        return self.vehicle


class CameraController:
    def __init__(self, app, camera, vehicle):
        self.app = app
        self.camera = camera
        self.vehicle = vehicle
        self.camera.reparent_to(self.app.render)

    def update(self, task):
        horiz_dist = 7
        cam_offset = Vec3(0, 0, 2)
        focus_offset = Vec3(0, 0, 1)
        vehicle_pos = self.vehicle.np().get_pos(self.app.render)
        vehicle_back = self.app.render.get_relative_vector(
            self.vehicle.np(),
            Vec3(0, -1, 0),
        )
        vehicle_back.z = 0
        vehicle_back = vehicle_back / vehicle_back.length()

        cam_pos = vehicle_pos + vehicle_back * horiz_dist + cam_offset
        focus = vehicle_pos + focus_offset
        base.cam.set_pos(cam_pos)
        base.cam.look_at(focus)

        return task.cont


def main():
    app = GameApp()
    app.run()

if __name__ == '__main__':
    main()
