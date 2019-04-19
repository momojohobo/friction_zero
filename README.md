Friction: Zero
==============

A racing game about hovering vehicles.


TODO
----

### Code

* Spawn point connectors
* Course gates
* Friction
* Refactoring: Move vehicle control logic into an ECU method
* Avionics (should come after ECU)
  * Gyroscopic stabilization
    * Angular damping works just fine, now proper logic for control and
      environment-sensitive stabilization has to be implemented.
  * Replacement of linear damping on repulsors
* Artist-defined repulsors
  * Find a better name than repulsor:*
    * Maybe fz_repulsor*?
* Artist-defined gravity
* Air drag
  * Artist-defined air density
* Aerodynamics
* Camera controls and automatics
* GUI
* Animations
* Gamepad support


### Art

* Add 'fz_spawn_point_connector' Empty
* After spawn point connectors are implemented: Move center of mass of Magnesium
  up
* Rename 'spawn_point' to 'fz_spawn_point' and change symbol value in code.