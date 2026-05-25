bl_info = {
    "name": "Instances Animator",
    "author": "Kll7a",
    "version": (2, 0, 0), # Final Stable Build
    "blender": (4, 2, 1),
    "location": "View3D > Sidebar > Instances Animator",
    "description": "Adds a panel to apply instances animator to selected object",
    "category": "Node",
}

import bpy

# =================================================================================
# UI ПАНЕЛЬ И ЛОГИКА ОТОБРАЖЕНИЯ
# =================================================================================

class InstancesAnimatorPanel(bpy.types.Panel):
    bl_label = "Instances Animator"
    bl_idname = "VIEW3D_PT_instances_animator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Instances Animator'

    def draw(self, context):
        layout = self.layout
        
        is_applied = False
        if context.object and "Instances animator" in context.object.modifiers:
            is_applied = True
            
        if not is_applied:
            op_row = layout.row()
            op_row.operator("node.instances_animator")
            if not context.object:
                op_row.enabled = False

        if is_applied:
            layout.operator("node.delete_instances_animator")
            layout.separator()
            layout.label(text="Main Parameters")
            layout.prop(context.scene, "instances_animator_show_main_mesh")
            layout.prop(context.scene, "instances_animator_subdivide_mesh")
            layout.prop(context.scene, "instances_animator_collection_for_instances")
            layout.prop(context.scene, "instances_animator_set_material")
            layout.prop(context.scene, "instances_animator_material")
            
            layout.separator()
            layout.label(text="Instance Parameters")
            layout.prop(context.scene, "instances_animator_random_instances")
            layout.prop(context.scene, "instances_animator_random_density")
            layout.prop(context.scene, "instances_animator_random_seed")
            layout.prop(context.scene, "instances_animator_x_rotation")
            layout.prop(context.scene, "instances_animator_y_rotation")
            layout.prop(context.scene, "instances_animator_z_rotation")
            layout.prop(context.scene, "instances_animator_random_rotation")
            layout.prop(context.scene, "instances_animator_value_of_random")
            layout.prop(context.scene, "instances_animator_seed_rr")
            layout.prop(context.scene, "instances_animator_scale_instance")
            layout.prop(context.scene, "instances_animator_random_scale")
            layout.prop(context.scene, "instances_animator_min_scale")
            layout.prop(context.scene, "instances_animator_max_scale")
            layout.prop(context.scene, "instances_animator_seed_rs")
            
            layout.separator()
            layout.label(text="Animation Parameters")
            layout.prop(context.scene, "instances_animator_looping_frames")
            layout.prop(context.scene, "instances_animator_speed")
            layout.prop(context.scene, "instances_animator_distortion")
            layout.prop(context.scene, "instances_animator_distortion_scale")
            layout.prop(context.scene, "instances_animator_x_offset")
            layout.prop(context.scene, "instances_animator_y_offset")
            layout.prop(context.scene, "instances_animator_z_offset")

# =================================================================================
# ОПЕРАТОРЫ (КНОПКИ)
# =================================================================================

class InstancesAnimatorOperator(bpy.types.Operator):
    bl_idname = "node.instances_animator"
    bl_label = "Apply Instances Animator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        def instances_animator_node_group():
            # =================================================================================
            # НАЧАЛО БЛОКА НОДОВ ИЗ ВАШЕГО ФАЙЛА __init__.py (work.py) - НЕ ТРОГАТЬ!
            # =================================================================================
            instances_animator = bpy.data.node_groups.new(type='GeometryNodeTree', name="Instances animator")

            instances_animator.color_tag = 'NONE'
            instances_animator.description = ""
            instances_animator.is_modifier = True

            # instances_animator interface
            # Socket Geometry
            geometry_socket = instances_animator.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
            geometry_socket.attribute_domain = 'POINT'

            # Socket Geometry
            geometry_socket_1 = instances_animator.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
            geometry_socket_1.attribute_domain = 'POINT'

            # Panel Main parameters
            main_parameters_panel = instances_animator.interface.new_panel("Main parameters")
            # Socket Show main mesh
            show_main_mesh_socket = instances_animator.interface.new_socket(name="Show main mesh", in_out='INPUT', socket_type='NodeSocketBool', parent=main_parameters_panel)
            show_main_mesh_socket.default_value = False
            show_main_mesh_socket.attribute_domain = 'POINT'

            # Socket Subdivide mesh
            subdivide_mesh_socket = instances_animator.interface.new_socket(name="Subdivide mesh", in_out='INPUT', socket_type='NodeSocketInt', parent=main_parameters_panel)
            subdivide_mesh_socket.default_value = 0
            subdivide_mesh_socket.min_value = 0
            subdivide_mesh_socket.max_value = 1000
            subdivide_mesh_socket.subtype = 'NONE'
            subdivide_mesh_socket.attribute_domain = 'POINT'

            # Socket Collection for instances
            collection_for_instances_socket = instances_animator.interface.new_socket(name="Collection for instances", in_out='INPUT', socket_type='NodeSocketCollection', parent=main_parameters_panel)
            collection_for_instances_socket.attribute_domain = 'POINT'

            # Socket Set Material
            set_material_socket = instances_animator.interface.new_socket(name="Set Material", in_out='INPUT', socket_type='NodeSocketBool', parent=main_parameters_panel)
            set_material_socket.default_value = False
            set_material_socket.attribute_domain = 'POINT'

            # Socket Material
            material_socket = instances_animator.interface.new_socket(name="Material", in_out='INPUT', socket_type='NodeSocketMaterial', parent=main_parameters_panel)
            material_socket.attribute_domain = 'POINT'

            # Panel Instance parameters
            instance_parameters_panel = instances_animator.interface.new_panel("Instance parameters")
            # Socket Random instances
            random_instances_socket = instances_animator.interface.new_socket(name="Random instances", in_out='INPUT', socket_type='NodeSocketBool', parent=instance_parameters_panel)
            random_instances_socket.default_value = False
            random_instances_socket.attribute_domain = 'POINT'

            # Socket Random density
            random_density_socket = instances_animator.interface.new_socket(name="Random density", in_out='INPUT', socket_type='NodeSocketFloat', parent=instance_parameters_panel)
            random_density_socket.default_value = 200.0
            random_density_socket.min_value = 0.0
            random_density_socket.max_value = 3.4028234663852886e+38
            random_density_socket.subtype = 'NONE'
            random_density_socket.attribute_domain = 'POINT'

            # Socket Random seed
            random_seed_socket = instances_animator.interface.new_socket(name="Random seed", in_out='INPUT', socket_type='NodeSocketInt', parent=instance_parameters_panel)
            random_seed_socket.default_value = 0
            random_seed_socket.min_value = -2147483648
            random_seed_socket.max_value = 2147483647
            random_seed_socket.subtype = 'NONE'
            random_seed_socket.attribute_domain = 'POINT'

            # Socket X rotation
            x_rotation_socket = instances_animator.interface.new_socket(name="X rotation", in_out='INPUT', socket_type='NodeSocketFloat', parent=instance_parameters_panel)
            x_rotation_socket.default_value = 0.0
            x_rotation_socket.min_value = -10000.0
            x_rotation_socket.max_value = 10000.0
            x_rotation_socket.subtype = 'NONE'
            x_rotation_socket.attribute_domain = 'POINT'

            # Socket Y rotation
            y_rotation_socket = instances_animator.interface.new_socket(name="Y rotation", in_out='INPUT', socket_type='NodeSocketFloat', parent=instance_parameters_panel)
            y_rotation_socket.default_value = 0.0
            y_rotation_socket.min_value = -10000.0
            y_rotation_socket.max_value = 10000.0
            y_rotation_socket.subtype = 'NONE'
            y_rotation_socket.attribute_domain = 'POINT'

            # Socket Z rotation
            z_rotation_socket = instances_animator.interface.new_socket(name="Z rotation", in_out='INPUT', socket_type='NodeSocketFloat', parent=instance_parameters_panel)
            z_rotation_socket.default_value = 0.0
            z_rotation_socket.min_value = -10000.0
            z_rotation_socket.max_value = 10000.0
            z_rotation_socket.subtype = 'NONE'
            z_rotation_socket.attribute_domain = 'POINT'

            # Socket Random rotation
            random_rotation_socket = instances_animator.interface.new_socket(name="Random rotation", in_out='INPUT', socket_type='NodeSocketBool', parent=instance_parameters_panel)
            random_rotation_socket.default_value = False
            random_rotation_socket.attribute_domain = 'POINT'

            # Socket Value of random
            value_of_random_socket = instances_animator.interface.new_socket(name="Value of random", in_out='INPUT', socket_type='NodeSocketFloat', parent=instance_parameters_panel)
            value_of_random_socket.default_value = 1.0
            value_of_random_socket.min_value = -3.4028234663852886e+38
            value_of_random_socket.max_value = 3.4028234663852886e+38
            value_of_random_socket.subtype = 'NONE'
            value_of_random_socket.attribute_domain = 'POINT'

            # Socket Seed rr
            seed_rr_socket = instances_animator.interface.new_socket(name="Seed rr", in_out='INPUT', socket_type='NodeSocketInt', parent=instance_parameters_panel)
            seed_rr_socket.default_value = 0
            seed_rr_socket.min_value = -10000
            seed_rr_socket.max_value = 10000
            seed_rr_socket.subtype = 'NONE'
            seed_rr_socket.attribute_domain = 'POINT'

            # Socket Scale instance
            scale_instance_socket = instances_animator.interface.new_socket(name="Scale instance", in_out='INPUT', socket_type='NodeSocketFloat', parent=instance_parameters_panel)
            scale_instance_socket.default_value = 1.0
            scale_instance_socket.min_value = -10000.0
            scale_instance_socket.max_value = 10000.0
            scale_instance_socket.subtype = 'NONE'
            scale_instance_socket.attribute_domain = 'POINT'

            # Socket Random scale
            random_scale_socket = instances_animator.interface.new_socket(name="Random scale", in_out='INPUT', socket_type='NodeSocketBool', parent=instance_parameters_panel)
            random_scale_socket.default_value = False
            random_scale_socket.attribute_domain = 'POINT'

            # Socket Min scale
            min_scale_socket = instances_animator.interface.new_socket(name="Min scale", in_out='INPUT', socket_type='NodeSocketFloat', parent=instance_parameters_panel)
            min_scale_socket.default_value = 1.0
            min_scale_socket.min_value = -3.4028234663852886e+38
            min_scale_socket.max_value = 3.4028234663852886e+38
            min_scale_socket.subtype = 'NONE'
            min_scale_socket.attribute_domain = 'POINT'

            # Socket Max scale
            max_scale_socket = instances_animator.interface.new_socket(name="Max scale", in_out='INPUT', socket_type='NodeSocketFloat', parent=instance_parameters_panel)
            max_scale_socket.default_value = 3.0
            max_scale_socket.min_value = -3.4028234663852886e+38
            max_scale_socket.max_value = 3.4028234663852886e+38
            max_scale_socket.subtype = 'NONE'
            max_scale_socket.attribute_domain = 'POINT'

            # Socket Seed rs
            seed_rs_socket = instances_animator.interface.new_socket(name="Seed rs", in_out='INPUT', socket_type='NodeSocketInt', parent=instance_parameters_panel)
            seed_rs_socket.default_value = 0
            seed_rs_socket.min_value = -10000
            seed_rs_socket.max_value = 10000
            seed_rs_socket.subtype = 'NONE'
            seed_rs_socket.attribute_domain = 'POINT'

            # Panel Animation parameters
            animation_parameters_panel = instances_animator.interface.new_panel("Animation parameters")
            # Socket Looping frames
            looping_frames_socket = instances_animator.interface.new_socket(name="Looping frames", in_out='INPUT', socket_type='NodeSocketFloat', parent=animation_parameters_panel)
            looping_frames_socket.default_value = 70.0
            looping_frames_socket.min_value = -3.4028234663852886e+38
            looping_frames_socket.max_value = 3.4028234663852886e+38
            looping_frames_socket.subtype = 'NONE'
            looping_frames_socket.attribute_domain = 'POINT'

            # Socket Speed
            speed_socket = instances_animator.interface.new_socket(name="Speed", in_out='INPUT', socket_type='NodeSocketFloat', parent=animation_parameters_panel)
            speed_socket.default_value = 1.0
            speed_socket.min_value = -10000.0
            speed_socket.max_value = 10000.0
            speed_socket.subtype = 'NONE'
            speed_socket.attribute_domain = 'POINT'

            # Socket Distortion
            distortion_socket = instances_animator.interface.new_socket(name="Distortion", in_out='INPUT', socket_type='NodeSocketFloat', parent=animation_parameters_panel)
            distortion_socket.default_value = 0.0
            distortion_socket.min_value = -1000.0
            distortion_socket.max_value = 1000.0
            distortion_socket.subtype = 'NONE'
            distortion_socket.attribute_domain = 'POINT'

            # Socket Distortion Scale
            distortion_scale_socket = instances_animator.interface.new_socket(name="Distortion Scale", in_out='INPUT', socket_type='NodeSocketFloat', parent=animation_parameters_panel)
            distortion_scale_socket.default_value = 5.0
            distortion_scale_socket.min_value = -1000.0
            distortion_scale_socket.max_value = 1000.0
            distortion_scale_socket.subtype = 'NONE'
            distortion_scale_socket.attribute_domain = 'POINT'

            # Socket X offset
            x_offset_socket = instances_animator.interface.new_socket(name="X offset", in_out='INPUT', socket_type='NodeSocketFloat', parent=animation_parameters_panel)
            x_offset_socket.default_value = 0.0
            x_offset_socket.min_value = -10000.0
            x_offset_socket.max_value = 10000.0
            x_offset_socket.subtype = 'NONE'
            x_offset_socket.attribute_domain = 'POINT'

            # Socket Y offset
            y_offset_socket = instances_animator.interface.new_socket(name="Y offset", in_out='INPUT', socket_type='NodeSocketFloat', parent=animation_parameters_panel)
            y_offset_socket.default_value = 0.0
            y_offset_socket.min_value = -10000.0
            y_offset_socket.max_value = 10000.0
            y_offset_socket.subtype = 'NONE'
            y_offset_socket.attribute_domain = 'POINT'

            # Socket Z offset
            z_offset_socket = instances_animator.interface.new_socket(name="Z offset", in_out='INPUT', socket_type='NodeSocketFloat', parent=animation_parameters_panel)
            z_offset_socket.default_value = 0.0
            z_offset_socket.min_value = -10000.0
            z_offset_socket.max_value = 10000.0
            z_offset_socket.subtype = 'NONE'
            z_offset_socket.attribute_domain = 'POINT'

            # Initialize instances_animator nodes
            # node Group Input
            group_input = instances_animator.nodes.new("NodeGroupInput")
            group_input.name = "Group Input"
            group_input.outputs[1].hide = True
            group_input.outputs[2].hide = True
            group_input.outputs[3].hide = True
            group_input.outputs[4].hide = True
            group_input.outputs[5].hide = True
            group_input.outputs[6].hide = True
            group_input.outputs[7].hide = True
            group_input.outputs[8].hide = True
            group_input.outputs[9].hide = True
            group_input.outputs[10].hide = True
            group_input.outputs[11].hide = True
            group_input.outputs[12].hide = True
            group_input.outputs[13].hide = True
            group_input.outputs[14].hide = True
            group_input.outputs[15].hide = True
            group_input.outputs[16].hide = True
            group_input.outputs[17].hide = True
            group_input.outputs[18].hide = True
            group_input.outputs[19].hide = True
            group_input.outputs[20].hide = True
            group_input.outputs[21].hide = True
            group_input.outputs[22].hide = True
            group_input.outputs[23].hide = True
            group_input.outputs[24].hide = True
            group_input.outputs[25].hide = True
            group_input.outputs[26].hide = True
            group_input.outputs[27].hide = True

            # node Group Output
            group_output = instances_animator.nodes.new("NodeGroupOutput")
            group_output.name = "Group Output"
            group_output.is_active_output = True

            # node Instance on Points
            instance_on_points = instances_animator.nodes.new("GeometryNodeInstanceOnPoints")
            instance_on_points.name = "Instance on Points"
            # Selection
            instance_on_points.inputs[1].default_value = True
            # Pick Instance
            instance_on_points.inputs[3].default_value = True
            # Instance Index
            instance_on_points.inputs[4].default_value = 0

            # node Noise Texture
            noise_texture = instances_animator.nodes.new("ShaderNodeTexNoise")
            noise_texture.name = "Noise Texture"
            noise_texture.noise_dimensions = '4D'
            noise_texture.noise_type = 'FBM'
            noise_texture.normalize = True
            # Vector
            noise_texture.inputs[0].default_value = (0.0, 0.0, 0.0)
            # Detail
            noise_texture.inputs[3].default_value = 0.0
            # Roughness
            noise_texture.inputs[4].default_value = 0.0
            # Lacunarity
            noise_texture.inputs[5].default_value = 0.0
            # Offset
            noise_texture.inputs[6].default_value = 0.0
            # Gain
            noise_texture.inputs[7].default_value = 1.0

            # node Vector Math
            vector_math = instances_animator.nodes.new("ShaderNodeVectorMath")
            vector_math.name = "Vector Math"
            vector_math.operation = 'MULTIPLY'
            # Vector_002
            vector_math.inputs[2].default_value = (0.0, 0.0, 0.0)
            # Scale
            vector_math.inputs[3].default_value = 1.0

            # node Combine XYZ
            combine_xyz = instances_animator.nodes.new("ShaderNodeCombineXYZ")
            combine_xyz.name = "Combine XYZ"

            # node Set Material
            set_material = instances_animator.nodes.new("GeometryNodeSetMaterial")
            set_material.name = "Set Material"

            # node Noise Texture.001
            noise_texture_001 = instances_animator.nodes.new("ShaderNodeTexNoise")
            noise_texture_001.name = "Noise Texture.001"
            noise_texture_001.noise_dimensions = '4D'
            noise_texture_001.noise_type = 'FBM'
            noise_texture_001.normalize = True
            # Vector
            noise_texture_001.inputs[0].default_value = (0.0, 0.0, 0.0)
            # Detail
            noise_texture_001.inputs[3].default_value = 0.0
            # Roughness
            noise_texture_001.inputs[4].default_value = 0.0
            # Lacunarity
            noise_texture_001.inputs[5].default_value = 0.0
            # Offset
            noise_texture_001.inputs[6].default_value = 0.0
            # Gain
            noise_texture_001.inputs[7].default_value = 1.0

            # node Mix
            mix = instances_animator.nodes.new("ShaderNodeMix")
            mix.name = "Mix"
            mix.blend_type = 'MIX'
            mix.clamp_factor = True
            mix.clamp_result = False
            mix.data_type = 'RGBA'
            mix.factor_mode = 'UNIFORM'
            # Factor_Vector
            mix.inputs[1].default_value = (0.5, 0.5, 0.5)
            # A_Float
            mix.inputs[2].default_value = 0.0
            # B_Float
            mix.inputs[3].default_value = 0.0
            # A_Vector
            mix.inputs[4].default_value = (0.0, 0.0, 0.0)
            # B_Vector
            mix.inputs[5].default_value = (0.0, 0.0, 0.0)
            # A_Rotation
            mix.inputs[8].default_value = (0.0, 0.0, 0.0)
            # B_Rotation
            mix.inputs[9].default_value = (0.0, 0.0, 0.0)

            # node Value.001
            value_001 = instances_animator.nodes.new("ShaderNodeValue")
            value_001.label = "Noise Speed"
            value_001.name = "Value.001"

            value_001.outputs[0].default_value = 0.0
            # node Math.002
            math_002 = instances_animator.nodes.new("ShaderNodeMath")
            math_002.name = "Math.002"
            math_002.operation = 'SUBTRACT'
            math_002.use_clamp = False
            # Value_002
            math_002.inputs[2].default_value = 0.5

            # node Math.003
            math_003 = instances_animator.nodes.new("ShaderNodeMath")
            math_003.name = "Math.003"
            math_003.operation = 'MULTIPLY'
            math_003.use_clamp = False
            # Value_002
            math_003.inputs[2].default_value = 0.5

            # node Math.004
            math_004 = instances_animator.nodes.new("ShaderNodeMath")
            math_004.name = "Math.004"
            math_004.operation = 'MULTIPLY'
            math_004.use_clamp = False
            # Value_002
            math_004.inputs[2].default_value = 0.5

            # node Math.005
            math_005 = instances_animator.nodes.new("ShaderNodeMath")
            math_005.name = "Math.005"
            math_005.operation = 'DIVIDE'
            math_005.use_clamp = False
            # Value_002
            math_005.inputs[2].default_value = 0.5

            # node Math.001
            math_001 = instances_animator.nodes.new("ShaderNodeMath")
            math_001.name = "Math.001"
            math_001.operation = 'FLOORED_MODULO'
            math_001.use_clamp = False
            # Value_002
            math_001.inputs[2].default_value = 0.5

            # node Scene Time
            scene_time = instances_animator.nodes.new("GeometryNodeInputSceneTime")
            scene_time.name = "Scene Time"

            # node Reroute
            reroute = instances_animator.nodes.new("NodeReroute")
            reroute.name = "Reroute"
            # node Math.006
            math_006 = instances_animator.nodes.new("ShaderNodeMath")
            math_006.name = "Math.006"
            math_006.operation = 'DIVIDE'
            math_006.use_clamp = False
            # Value_001
            math_006.inputs[1].default_value = 300.0
            # Value_002
            math_006.inputs[2].default_value = 0.5

            # node Set Position.001
            set_position_001 = instances_animator.nodes.new("GeometryNodeSetPosition")
            set_position_001.name = "Set Position.001"
            # Selection
            set_position_001.inputs[1].default_value = True
            # Position
            set_position_001.inputs[2].default_value = (0.0, 0.0, 0.0)

            # node Set Position.002
            set_position_002 = instances_animator.nodes.new("GeometryNodeSetPosition")
            set_position_002.name = "Set Position.002"
            # Selection
            set_position_002.inputs[1].default_value = True
            # Position
            set_position_002.inputs[2].default_value = (0.0, 0.0, 0.0)

            # node Group Input.001
            group_input_001 = instances_animator.nodes.new("NodeGroupInput")
            group_input_001.name = "Group Input.001"
            group_input_001.outputs[0].hide = True
            group_input_001.outputs[1].hide = True
            group_input_001.outputs[2].hide = True
            group_input_001.outputs[3].hide = True
            group_input_001.outputs[4].hide = True
            group_input_001.outputs[5].hide = True
            group_input_001.outputs[6].hide = True
            group_input_001.outputs[7].hide = True
            group_input_001.outputs[8].hide = True
            group_input_001.outputs[9].hide = True
            group_input_001.outputs[10].hide = True
            group_input_001.outputs[11].hide = True
            group_input_001.outputs[12].hide = True
            group_input_001.outputs[13].hide = True
            group_input_001.outputs[14].hide = True
            group_input_001.outputs[15].hide = True
            group_input_001.outputs[16].hide = True
            group_input_001.outputs[17].hide = True
            group_input_001.outputs[18].hide = True
            group_input_001.outputs[19].hide = True
            group_input_001.outputs[20].hide = True
            group_input_001.outputs[21].hide = True
            group_input_001.outputs[22].hide = True
            group_input_001.outputs[23].hide = True
            group_input_001.outputs[24].hide = True
            group_input_001.outputs[25].hide = True
            group_input_001.outputs[26].hide = True
            group_input_001.outputs[27].hide = True

            # node Group Input.002
            group_input_002 = instances_animator.nodes.new("NodeGroupInput")
            group_input_002.name = "Group Input.002"
            group_input_002.hide = True
            group_input_002.outputs[0].hide = True
            group_input_002.outputs[1].hide = True
            group_input_002.outputs[2].hide = True
            group_input_002.outputs[3].hide = True
            group_input_002.outputs[4].hide = True
            group_input_002.outputs[5].hide = True
            group_input_002.outputs[6].hide = True
            group_input_002.outputs[7].hide = True
            group_input_002.outputs[8].hide = True
            group_input_002.outputs[9].hide = True
            group_input_002.outputs[10].hide = True
            group_input_002.outputs[11].hide = True
            group_input_002.outputs[12].hide = True
            group_input_002.outputs[13].hide = True
            group_input_002.outputs[14].hide = True
            group_input_002.outputs[15].hide = True
            group_input_002.outputs[16].hide = True
            group_input_002.outputs[17].hide = True
            group_input_002.outputs[18].hide = True
            group_input_002.outputs[19].hide = True
            group_input_002.outputs[20].hide = True
            group_input_002.outputs[21].hide = True
            group_input_002.outputs[22].hide = True
            group_input_002.outputs[23].hide = True
            group_input_002.outputs[27].hide = True

            # node Vector Math.001
            vector_math_001 = instances_animator.nodes.new("ShaderNodeVectorMath")
            vector_math_001.name = "Vector Math.001"
            vector_math_001.operation = 'DIVIDE'
            # Vector_001
            vector_math_001.inputs[1].default_value = (-2.0, -2.0, -2.0)
            # Vector_002
            vector_math_001.inputs[2].default_value = (0.0, 0.0, 0.0)
            # Scale
            vector_math_001.inputs[3].default_value = 1.0

            # node Combine XYZ.001
            combine_xyz_001 = instances_animator.nodes.new("ShaderNodeCombineXYZ")
            combine_xyz_001.name = "Combine XYZ.001"

            # node Math.009
            math_009 = instances_animator.nodes.new("ShaderNodeMath")
            math_009.name = "Math.009"
            math_009.operation = 'ADD'
            math_009.use_clamp = False
            # Value_002
            math_009.inputs[2].default_value = 0.5

            # node Group Input.004
            group_input_004 = instances_animator.nodes.new("NodeGroupInput")
            group_input_004.name = "Group Input.004"
            group_input_004.outputs[0].hide = True
            group_input_004.outputs[1].hide = True
            group_input_004.outputs[2].hide = True
            group_input_004.outputs[3].hide = True
            group_input_004.outputs[4].hide = True
            group_input_004.outputs[5].hide = True
            group_input_004.outputs[6].hide = True
            group_input_004.outputs[7].hide = True
            group_input_004.outputs[8].hide = True
            group_input_004.outputs[9].hide = True
            group_input_004.outputs[10].hide = True
            group_input_004.outputs[11].hide = True
            group_input_004.outputs[12].hide = True
            group_input_004.outputs[13].hide = True
            group_input_004.outputs[14].hide = True
            group_input_004.outputs[15].hide = True
            group_input_004.outputs[16].hide = True
            group_input_004.outputs[17].hide = True
            group_input_004.outputs[18].hide = True
            group_input_004.outputs[19].hide = True
            group_input_004.outputs[21].hide = True
            group_input_004.outputs[22].hide = True
            group_input_004.outputs[23].hide = True
            group_input_004.outputs[24].hide = True
            group_input_004.outputs[25].hide = True
            group_input_004.outputs[26].hide = True
            group_input_004.outputs[27].hide = True

            # node Group Input.005
            group_input_005 = instances_animator.nodes.new("NodeGroupInput")
            group_input_005.name = "Group Input.005"
            group_input_005.outputs[0].hide = True
            group_input_005.outputs[1].hide = True
            group_input_005.outputs[2].hide = True
            group_input_005.outputs[3].hide = True
            group_input_005.outputs[4].hide = True
            group_input_005.outputs[5].hide = True
            group_input_005.outputs[6].hide = True
            group_input_005.outputs[7].hide = True
            group_input_005.outputs[8].hide = True
            group_input_005.outputs[9].hide = True
            group_input_005.outputs[10].hide = True
            group_input_005.outputs[11].hide = True
            group_input_005.outputs[12].hide = True
            group_input_005.outputs[13].hide = True
            group_input_005.outputs[14].hide = True
            group_input_005.outputs[15].hide = True
            group_input_005.outputs[16].hide = True
            group_input_005.outputs[17].hide = True
            group_input_005.outputs[18].hide = True
            group_input_005.outputs[19].hide = True
            group_input_005.outputs[20].hide = True
            group_input_005.outputs[21].hide = True
            group_input_005.outputs[24].hide = True
            group_input_005.outputs[25].hide = True
            group_input_005.outputs[26].hide = True
            group_input_005.outputs[27].hide = True

            # node Reroute.001
            reroute_001 = instances_animator.nodes.new("NodeReroute")
            reroute_001.name = "Reroute.001"
            # node Group Input.006
            group_input_006 = instances_animator.nodes.new("NodeGroupInput")
            group_input_006.name = "Group Input.006"
            group_input_006.outputs[0].hide = True
            group_input_006.outputs[1].hide = True
            group_input_006.outputs[2].hide = True
            group_input_006.outputs[3].hide = True
            group_input_006.outputs[4].hide = True
            group_input_006.outputs[5].hide = True
            group_input_006.outputs[6].hide = True
            group_input_006.outputs[7].hide = True
            group_input_006.outputs[8].hide = True
            group_input_006.outputs[9].hide = True
            group_input_006.outputs[10].hide = True
            group_input_006.outputs[11].hide = True
            group_input_006.outputs[12].hide = True
            group_input_006.outputs[13].hide = True
            group_input_006.outputs[14].hide = True
            group_input_006.outputs[15].hide = True
            group_input_006.outputs[16].hide = True
            group_input_006.outputs[17].hide = True
            group_input_006.outputs[18].hide = True
            group_input_006.outputs[19].hide = True
            group_input_006.outputs[20].hide = True
            group_input_006.outputs[22].hide = True
            group_input_006.outputs[23].hide = True
            group_input_006.outputs[24].hide = True
            group_input_006.outputs[25].hide = True
            group_input_006.outputs[26].hide = True
            group_input_006.outputs[27].hide = True

            # node Combine XYZ.002
            combine_xyz_002 = instances_animator.nodes.new("ShaderNodeCombineXYZ")
            combine_xyz_002.name = "Combine XYZ.002"

            # node Group Input.007
            group_input_007 = instances_animator.nodes.new("NodeGroupInput")
            group_input_007.name = "Group Input.007"
            group_input_007.outputs[0].hide = True
            group_input_007.outputs[1].hide = True
            group_input_007.outputs[2].hide = True
            group_input_007.outputs[3].hide = True
            group_input_007.outputs[4].hide = True
            group_input_007.outputs[5].hide = True
            group_input_007.outputs[6].hide = True
            group_input_007.outputs[7].hide = True
            group_input_007.outputs[8].hide = True
            group_input_007.outputs[15].hide = True
            group_input_007.outputs[16].hide = True
            group_input_007.outputs[17].hide = True
            group_input_007.outputs[18].hide = True
            group_input_007.outputs[19].hide = True
            group_input_007.outputs[20].hide = True
            group_input_007.outputs[21].hide = True
            group_input_007.outputs[22].hide = True
            group_input_007.outputs[23].hide = True
            group_input_007.outputs[24].hide = True
            group_input_007.outputs[25].hide = True
            group_input_007.outputs[26].hide = True
            group_input_007.outputs[27].hide = True

            # node Group Input.008
            group_input_008 = instances_animator.nodes.new("NodeGroupInput")
            group_input_008.name = "Group Input.008"
            group_input_008.outputs[0].hide = True
            group_input_008.outputs[1].hide = True
            group_input_008.outputs[2].hide = True
            group_input_008.outputs[3].hide = True
            group_input_008.outputs[6].hide = True
            group_input_008.outputs[7].hide = True
            group_input_008.outputs[8].hide = True
            group_input_008.outputs[9].hide = True
            group_input_008.outputs[10].hide = True
            group_input_008.outputs[11].hide = True
            group_input_008.outputs[12].hide = True
            group_input_008.outputs[13].hide = True
            group_input_008.outputs[14].hide = True
            group_input_008.outputs[15].hide = True
            group_input_008.outputs[16].hide = True
            group_input_008.outputs[17].hide = True
            group_input_008.outputs[18].hide = True
            group_input_008.outputs[19].hide = True
            group_input_008.outputs[20].hide = True
            group_input_008.outputs[21].hide = True
            group_input_008.outputs[22].hide = True
            group_input_008.outputs[23].hide = True
            group_input_008.outputs[24].hide = True
            group_input_008.outputs[25].hide = True
            group_input_008.outputs[26].hide = True
            group_input_008.outputs[27].hide = True

            # node Switch
            switch = instances_animator.nodes.new("GeometryNodeSwitch")
            switch.name = "Switch"
            switch.input_type = 'INT'
            # False
            switch.inputs[1].default_value = 0
            # True
            switch.inputs[2].default_value = 1

            # node Group Input.010
            group_input_010 = instances_animator.nodes.new("NodeGroupInput")
            group_input_010.name = "Group Input.010"
            group_input_010.outputs[0].hide = True
            group_input_010.outputs[1].hide = True
            group_input_010.outputs[2].hide = True
            group_input_010.outputs[4].hide = True
            group_input_010.outputs[5].hide = True
            group_input_010.outputs[6].hide = True
            group_input_010.outputs[7].hide = True
            group_input_010.outputs[8].hide = True
            group_input_010.outputs[9].hide = True
            group_input_010.outputs[10].hide = True
            group_input_010.outputs[11].hide = True
            group_input_010.outputs[12].hide = True
            group_input_010.outputs[13].hide = True
            group_input_010.outputs[14].hide = True
            group_input_010.outputs[20].hide = True
            group_input_010.outputs[21].hide = True
            group_input_010.outputs[22].hide = True
            group_input_010.outputs[23].hide = True
            group_input_010.outputs[24].hide = True
            group_input_010.outputs[25].hide = True
            group_input_010.outputs[26].hide = True
            group_input_010.outputs[27].hide = True

            # node Collection Info
            collection_info = instances_animator.nodes.new("GeometryNodeCollectionInfo")
            collection_info.name = "Collection Info"
            collection_info.transform_space = 'RELATIVE'
            # Separate Children
            collection_info.inputs[1].default_value = True
            # Reset Children
            collection_info.inputs[2].default_value = True

            # node Distribute Points on Faces
            distribute_points_on_faces = instances_animator.nodes.new("GeometryNodeDistributePointsOnFaces")
            distribute_points_on_faces.name = "Distribute Points on Faces"
            distribute_points_on_faces.distribute_method = 'RANDOM'
            distribute_points_on_faces.use_legacy_normal = False
            # Selection
            distribute_points_on_faces.inputs[1].default_value = True
            # Distance Min
            distribute_points_on_faces.inputs[2].default_value = 0.0
            # Density Max
            distribute_points_on_faces.inputs[3].default_value = 500.0
            # Density Factor
            distribute_points_on_faces.inputs[5].default_value = 1.0

            # node Switch.001
            switch_001 = instances_animator.nodes.new("GeometryNodeSwitch")
            switch_001.name = "Switch.001"
            switch_001.input_type = 'GEOMETRY'

            # node Group Input.009
            group_input_009 = instances_animator.nodes.new("NodeGroupInput")
            group_input_009.name = "Group Input.009"
            group_input_009.outputs[0].hide = True
            group_input_009.outputs[1].hide = True
            group_input_009.outputs[2].hide = True
            group_input_009.outputs[3].hide = True
            group_input_009.outputs[4].hide = True
            group_input_009.outputs[5].hide = True
            group_input_009.outputs[9].hide = True
            group_input_009.outputs[10].hide = True
            group_input_009.outputs[11].hide = True
            group_input_009.outputs[12].hide = True
            group_input_009.outputs[13].hide = True
            group_input_009.outputs[14].hide = True
            group_input_009.outputs[15].hide = True
            group_input_009.outputs[16].hide = True
            group_input_009.outputs[17].hide = True
            group_input_009.outputs[18].hide = True
            group_input_009.outputs[19].hide = True
            group_input_009.outputs[20].hide = True
            group_input_009.outputs[21].hide = True
            group_input_009.outputs[22].hide = True
            group_input_009.outputs[23].hide = True
            group_input_009.outputs[24].hide = True
            group_input_009.outputs[25].hide = True
            group_input_009.outputs[26].hide = True
            group_input_009.outputs[27].hide = True

            # node Switch.002
            switch_002 = instances_animator.nodes.new("GeometryNodeSwitch")
            switch_002.name = "Switch.002"
            switch_002.input_type = 'GEOMETRY'

            # node Join Geometry
            join_geometry = instances_animator.nodes.new("GeometryNodeJoinGeometry")
            join_geometry.name = "Join Geometry"

            # node Group Input.011
            group_input_011 = instances_animator.nodes.new("NodeGroupInput")
            group_input_011.name = "Group Input.011"
            group_input_011.outputs[0].hide = True
            group_input_011.outputs[2].hide = True
            group_input_011.outputs[3].hide = True
            group_input_011.outputs[4].hide = True
            group_input_011.outputs[5].hide = True
            group_input_011.outputs[6].hide = True
            group_input_011.outputs[7].hide = True
            group_input_011.outputs[8].hide = True
            group_input_011.outputs[9].hide = True
            group_input_011.outputs[10].hide = True
            group_input_011.outputs[11].hide = True
            group_input_011.outputs[12].hide = True
            group_input_011.outputs[13].hide = True
            group_input_011.outputs[14].hide = True
            group_input_011.outputs[15].hide = True
            group_input_011.outputs[16].hide = True
            group_input_011.outputs[17].hide = True
            group_input_011.outputs[18].hide = True
            group_input_011.outputs[19].hide = True
            group_input_011.outputs[20].hide = True
            group_input_011.outputs[21].hide = True
            group_input_011.outputs[22].hide = True
            group_input_011.outputs[23].hide = True
            group_input_011.outputs[24].hide = True
            group_input_011.outputs[25].hide = True
            group_input_011.outputs[26].hide = True
            group_input_011.outputs[27].hide = True

            # node Math
            math = instances_animator.nodes.new("ShaderNodeMath")
            math.name = "Math"
            math.operation = 'DIVIDE'
            math.use_clamp = False
            # Value_001
            math.inputs[1].default_value = 50.0
            # Value_002
            math.inputs[2].default_value = 0.5

            # node Group Input.012
            group_input_012 = instances_animator.nodes.new("NodeGroupInput")
            group_input_012.name = "Group Input.012"
            group_input_012.outputs[0].hide = True
            group_input_012.outputs[1].hide = True
            group_input_012.outputs[3].hide = True
            group_input_012.outputs[4].hide = True
            group_input_012.outputs[5].hide = True
            group_input_012.outputs[6].hide = True
            group_input_012.outputs[7].hide = True
            group_input_012.outputs[8].hide = True
            group_input_012.outputs[9].hide = True
            group_input_012.outputs[10].hide = True
            group_input_012.outputs[11].hide = True
            group_input_012.outputs[12].hide = True
            group_input_012.outputs[13].hide = True
            group_input_012.outputs[14].hide = True
            group_input_012.outputs[15].hide = True
            group_input_012.outputs[16].hide = True
            group_input_012.outputs[17].hide = True
            group_input_012.outputs[18].hide = True
            group_input_012.outputs[19].hide = True
            group_input_012.outputs[20].hide = True
            group_input_012.outputs[21].hide = True
            group_input_012.outputs[22].hide = True
            group_input_012.outputs[23].hide = True
            group_input_012.outputs[24].hide = True
            group_input_012.outputs[25].hide = True
            group_input_012.outputs[26].hide = True
            group_input_012.outputs[27].hide = True

            # node Subdivide Mesh.001
            subdivide_mesh_001 = instances_animator.nodes.new("GeometryNodeSubdivideMesh")
            subdivide_mesh_001.name = "Subdivide Mesh.001"

            # node Subdivide Mesh.002
            subdivide_mesh_002 = instances_animator.nodes.new("GeometryNodeSubdivideMesh")
            subdivide_mesh_002.name = "Subdivide Mesh.002"

            # node Reroute.002
            reroute_002 = instances_animator.nodes.new("NodeReroute")
            reroute_002.name = "Reroute.002"
            # node Math.007
            math_007 = instances_animator.nodes.new("ShaderNodeMath")
            math_007.name = "Math.007"
            math_007.operation = 'ADD'
            math_007.use_clamp = False
            # Value
            math_007.inputs[0].default_value = 0.0
            # Value_002
            math_007.inputs[2].default_value = 0.5

            # node Switch.003
            switch_003 = instances_animator.nodes.new("GeometryNodeSwitch")
            switch_003.name = "Switch.003"
            switch_003.input_type = 'VECTOR'

            # node Random Value
            random_value = instances_animator.nodes.new("FunctionNodeRandomValue")
            random_value.name = "Random Value"
            random_value.data_type = 'FLOAT'
            # Min
            random_value.inputs[0].default_value = (0.0, 0.0, 0.0)
            # Max
            random_value.inputs[1].default_value = (1.0, 1.0, 1.0)
            # Min_001
            random_value.inputs[2].default_value = 0.0
            # Min_002
            random_value.inputs[4].default_value = 0
            # Max_002
            random_value.inputs[5].default_value = 100
            # Probability
            random_value.inputs[6].default_value = 0.5
            # ID
            random_value.inputs[7].default_value = 0

            # node Switch.004
            switch_004 = instances_animator.nodes.new("GeometryNodeSwitch")
            switch_004.name = "Switch.004"
            switch_004.input_type = 'FLOAT'

            # node Random Value.001
            random_value_001 = instances_animator.nodes.new("FunctionNodeRandomValue")
            random_value_001.name = "Random Value.001"
            random_value_001.data_type = 'FLOAT'
            # Min
            random_value_001.inputs[0].default_value = (0.0, 0.0, 0.0)
            # Max
            random_value_001.inputs[1].default_value = (1.0, 1.0, 1.0)
            # Min_002
            random_value_001.inputs[4].default_value = 0
            # Max_002
            random_value_001.inputs[5].default_value = 100
            # Probability
            random_value_001.inputs[6].default_value = 0.5
            # ID
            random_value_001.inputs[7].default_value = 0

            # Set locations
            group_input.location = (737.158447265625, 975.9734497070312)
            group_output.location = (2775.431884765625, 536.7282104492188)
            instance_on_points.location = (2140.03564453125, 584.9578247070312)
            noise_texture.location = (1512.1279296875, -126.09011840820312)
            vector_math.location = (627.8524169921875, -39.4674072265625)
            combine_xyz.location = (628.17578125, -181.42279052734375)
            set_material.location = (2358.157470703125, 507.3840637207031)
            noise_texture_001.location = (1714.3759765625, -297.6951904296875)
            mix.location = (1713.364013671875, -53.17462158203125)
            value_001.location = (1188.6619873046875, -581.9361572265625)
            math_002.location = (1353.63818359375, -653.3568115234375)
            math_003.location = (1349.398193359375, -298.76220703125)
            math_004.location = (1518.832275390625, -601.046142578125)
            math_005.location = (1348.1082763671875, -126.5341796875)
            math_001.location = (1348.5064697265625, -475.1617431640625)
            scene_time.location = (1183.24853515625, -476.2677001953125)
            reroute.location = (1575.5831298828125, -801.612548828125)
            math_006.location = (1177.288818359375, -127.4896240234375)
            set_position_001.location = (761.943359375, 409.26129150390625)
            set_position_002.location = (1083.2415771484375, 618.52197265625)
            group_input_001.location = (1715.8260498046875, 79.82447814941406)
            group_input_002.location = (1351.7064208984375, 115.45679473876953)
            vector_math_001.location = (1517.9266357421875, 78.20391845703125)
            combine_xyz_001.location = (1355.0458984375, 77.23382568359375)
            math_009.location = (1182.07666015625, -300.4725341796875)
            group_input_004.location = (1352.6873779296875, -849.9087524414062)
            group_input_005.location = (1514.3489990234375, -474.54766845703125)
            reroute_001.location = (1547.8720703125, -803.2291259765625)
            group_input_006.location = (1186.365966796875, -681.4178466796875)
            combine_xyz_002.location = (1799.8433837890625, 295.9389953613281)
            group_input_007.location = (2034.59716796875, 143.02468872070312)
            group_input_008.location = (2424.551025390625, 175.95387268066406)
            switch.location = (2425.141357421875, 338.56982421875)
            group_input_010.location = (1309.4898681640625, 778.2595825195312)
            collection_info.location = (1643.188720703125, 747.9642944335938)
            distribute_points_on_faces.location = (559.153564453125, 409.3873291015625)
            switch_001.location = (763.548583984375, 568.1928100585938)
            group_input_009.location = (326.39593505859375, 427.85791015625)
            switch_002.location = (2607.998779296875, 691.9143676757812)
            join_geometry.location = (2612.307373046875, 536.6454467773438)
            group_input_011.location = (2614.052001953125, 756.07080078125)
            math.location = (1919.4310302734375, 486.71282958984375)
            group_input_012.location = (732.9610595703125, 742.258544921875)
            subdivide_mesh_001.location = (912.66455078125, 892.8464965820312)
            subdivide_mesh_002.location = (921.305908203125, 1001.2003173828125)
            reroute_002.location = (879.3603515625, 949.0638427734375)
            math_007.location = (733.066650390625, 903.22607421875)
            switch_003.location = (2220.1572265625, 296.34765625)
            random_value.location = (2023.7037353515625, 330.48260498046875)
            switch_004.location = (1753.8929443359375, 465.9742431640625)
            random_value_001.location = (1547.8548583984375, 382.9947509765625)

            # Set dimensions
            group_input.width, group_input.height = 140.0, 100.0
            group_output.width, group_output.height = 140.0, 100.0
            instance_on_points.width, instance_on_points.height = 140.0, 100.0
            noise_texture.width, noise_texture.height = 140.0, 100.0
            vector_math.width, vector_math.height = 140.0, 100.0
            combine_xyz.width, combine_xyz.height = 140.0, 100.0
            set_material.width, set_material.height = 140.0, 100.0
            noise_texture_001.width, noise_texture_001.height = 140.0, 100.0
            mix.width, mix.height = 140.0, 100.0
            value_001.width, value_001.height = 140.0, 100.0
            math_002.width, math_002.height = 140.0, 100.0
            math_003.width, math_003.height = 140.0, 100.0
            math_004.width, math_004.height = 140.0, 100.0
            math_005.width, math_005.height = 140.0, 100.0
            math_001.width, math_001.height = 140.0, 100.0
            scene_time.width, scene_time.height = 140.0, 100.0
            reroute.width, reroute.height = 16.0, 100.0
            math_006.width, math_006.height = 140.0, 100.0
            set_position_001.width, set_position_001.height = 140.0, 100.0
            set_position_002.width, set_position_002.height = 140.0, 100.0
            group_input_001.width, group_input_001.height = 140.0, 100.0
            group_input_002.width, group_input_002.height = 140.0, 100.0
            vector_math_001.width, vector_math_001.height = 140.0, 100.0
            combine_xyz_001.width, combine_xyz_001.height = 140.0, 100.0
            math_009.width, math_009.height = 140.0, 100.0
            group_input_004.width, group_input_004.height = 140.0, 100.0
            group_input_005.width, group_input_005.height = 140.0, 100.0
            reroute_001.width, reroute_001.height = 16.0, 100.0
            group_input_006.width, group_input_006.height = 140.0, 100.0
            combine_xyz_002.width, combine_xyz_002.height = 140.0, 100.0
            group_input_007.width, group_input_007.height = 140.0, 100.0
            group_input_008.width, group_input_008.height = 140.0, 100.0
            switch.width, switch.height = 140.0, 100.0
            group_input_010.width, group_input_010.height = 140.0, 100.0
            collection_info.width, collection_info.height = 140.0, 100.0
            distribute_points_on_faces.width, distribute_points_on_faces.height = 170.0, 100.0
            switch_001.width, switch_001.height = 140.0, 100.0
            group_input_009.width, group_input_009.height = 140.0, 100.0
            switch_002.width, switch_002.height = 140.0, 100.0
            join_geometry.width, join_geometry.height = 140.0, 100.0
            group_input_011.width, group_input_011.height = 140.0, 100.0
            math.width, math.height = 140.0, 100.0
            group_input_012.width, group_input_012.height = 140.0, 100.0
            subdivide_mesh_001.width, subdivide_mesh_001.height = 140.0, 100.0
            subdivide_mesh_002.width, subdivide_mesh_002.height = 140.0, 100.0
            reroute_002.width, reroute_002.height = 16.0, 100.0
            math_007.width, math_007.height = 140.0, 100.0
            switch_003.width, switch_003.height = 140.0, 100.0
            random_value.width, random_value.height = 140.0, 100.0
            switch_004.width, switch_004.height = 140.0, 100.0
            random_value_001.width, random_value_001.height = 140.0, 100.0

            # Initialize instances_animator links
            # join_geometry.Geometry -> group_output.Geometry
            instances_animator.links.new(join_geometry.outputs[0], group_output.inputs[0])
            # set_position_001.Geometry -> instance_on_points.Points
            instances_animator.links.new(set_position_001.outputs[0], instance_on_points.inputs[0])
            # instance_on_points.Instances -> set_material.Geometry
            instances_animator.links.new(instance_on_points.outputs[0], set_material.inputs[0])
            # noise_texture.Fac -> mix.A
            instances_animator.links.new(noise_texture.outputs[0], mix.inputs[6])
            # noise_texture_001.Fac -> mix.B
            instances_animator.links.new(noise_texture_001.outputs[0], mix.inputs[7])
            # reroute_001.Output -> math_002.Value
            instances_animator.links.new(reroute_001.outputs[0], math_002.inputs[1])
            # math_003.Value -> noise_texture.W
            instances_animator.links.new(math_003.outputs[0], noise_texture.inputs[1])
            # reroute.Output -> math_003.Value
            instances_animator.links.new(reroute.outputs[0], math_003.inputs[1])
            # math_002.Value -> math_004.Value
            instances_animator.links.new(math_002.outputs[0], math_004.inputs[0])
            # reroute.Output -> math_004.Value
            instances_animator.links.new(reroute.outputs[0], math_004.inputs[1])
            # math_004.Value -> noise_texture_001.W
            instances_animator.links.new(math_004.outputs[0], noise_texture_001.inputs[1])
            # reroute_001.Output -> math_005.Value
            instances_animator.links.new(reroute_001.outputs[0], math_005.inputs[1])
            # math_005.Value -> mix.Factor
            instances_animator.links.new(math_005.outputs[0], mix.inputs[0])
            # reroute_001.Output -> math_001.Value
            instances_animator.links.new(reroute_001.outputs[0], math_001.inputs[1])
            # math_001.Value -> math_003.Value
            instances_animator.links.new(math_001.outputs[0], math_003.inputs[0])
            # math_001.Value -> math_002.Value
            instances_animator.links.new(math_001.outputs[0], math_002.inputs[0])
            # math_001.Value -> math_005.Value
            instances_animator.links.new(math_001.outputs[0], math_005.inputs[0])
            # scene_time.Frame -> math_001.Value
            instances_animator.links.new(scene_time.outputs[1], math_001.inputs[0])
            # math_006.Value -> reroute.Input
            instances_animator.links.new(math_006.outputs[0], reroute.inputs[0])
            # math_009.Value -> math_006.Value
            instances_animator.links.new(math_009.outputs[0], math_006.inputs[0])
            # mix.Result -> vector_math.Vector
            instances_animator.links.new(mix.outputs[2], vector_math.inputs[0])
            # combine_xyz.Vector -> vector_math.Vector
            instances_animator.links.new(combine_xyz.outputs[0], vector_math.inputs[1])
            # switch_001.Output -> set_position_001.Geometry
            instances_animator.links.new(switch_001.outputs[0], set_position_001.inputs[0])
            # vector_math.Vector -> set_position_001.Offset
            instances_animator.links.new(vector_math.outputs[0], set_position_001.inputs[3])
            # group_input_001.X offset -> combine_xyz.X
            instances_animator.links.new(group_input_001.outputs[24], combine_xyz.inputs[0])
            # group_input_001.Z offset -> combine_xyz.Z
            instances_animator.links.new(group_input_001.outputs[26], combine_xyz.inputs[2])
            # group_input_001.Y offset -> combine_xyz.Y
            instances_animator.links.new(group_input_001.outputs[25], combine_xyz.inputs[1])
            # vector_math_001.Vector -> set_position_002.Offset
            instances_animator.links.new(vector_math_001.outputs[0], set_position_002.inputs[3])
            # combine_xyz_001.Vector -> vector_math_001.Vector
            instances_animator.links.new(combine_xyz_001.outputs[0], vector_math_001.inputs[0])
            # group_input_002.Z offset -> combine_xyz_001.Z
            instances_animator.links.new(group_input_002.outputs[26], combine_xyz_001.inputs[2])
            # group_input_002.X offset -> combine_xyz_001.X
            instances_animator.links.new(group_input_002.outputs[24], combine_xyz_001.inputs[0])
            # group_input_002.Y offset -> combine_xyz_001.Y
            instances_animator.links.new(group_input_002.outputs[25], combine_xyz_001.inputs[1])
            # subdivide_mesh_001.Mesh -> set_position_002.Geometry
            instances_animator.links.new(subdivide_mesh_001.outputs[0], set_position_002.inputs[0])
            # value_001.Value -> math_009.Value
            instances_animator.links.new(value_001.outputs[0], math_009.inputs[0])
            # group_input_005.Distortion Scale -> noise_texture.Scale
            instances_animator.links.new(group_input_005.outputs[23], noise_texture.inputs[2])
            # group_input_005.Distortion Scale -> noise_texture_001.Scale
            instances_animator.links.new(group_input_005.outputs[23], noise_texture_001.inputs[2])
            # group_input_005.Distortion -> noise_texture.Distortion
            instances_animator.links.new(group_input_005.outputs[22], noise_texture.inputs[8])
            # group_input_005.Distortion -> noise_texture_001.Distortion
            instances_animator.links.new(group_input_005.outputs[22], noise_texture_001.inputs[8])
            # group_input_006.Speed -> math_009.Value
            instances_animator.links.new(group_input_006.outputs[21], math_009.inputs[1])
            # group_input_007.X rotation -> combine_xyz_002.X
            instances_animator.links.new(group_input_007.outputs[9], combine_xyz_002.inputs[0])
            # group_input_007.Y rotation -> combine_xyz_002.Y
            instances_animator.links.new(group_input_007.outputs[10], combine_xyz_002.inputs[1])
            # group_input_007.Z rotation -> combine_xyz_002.Z
            instances_animator.links.new(group_input_007.outputs[11], combine_xyz_002.inputs[2])
            # group_input_004.Looping frames -> reroute_001.Input
            instances_animator.links.new(group_input_004.outputs[20], reroute_001.inputs[0])
            # switch.Output -> set_material.Selection
            instances_animator.links.new(switch.outputs[0], set_material.inputs[1])
            # group_input_008.Set Material -> switch.Switch
            instances_animator.links.new(group_input_008.outputs[4], switch.inputs[0])
            # group_input_008.Material -> set_material.Material
            instances_animator.links.new(group_input_008.outputs[5], set_material.inputs[2])
            # math.Value -> instance_on_points.Scale
            instances_animator.links.new(math.outputs[0], instance_on_points.inputs[6])
            # collection_info.Instances -> instance_on_points.Instance
            instances_animator.links.new(collection_info.outputs[0], instance_on_points.inputs[2])
            # set_position_002.Geometry -> distribute_points_on_faces.Mesh
            instances_animator.links.new(set_position_002.outputs[0], distribute_points_on_faces.inputs[0])
            # group_input_009.Random instances -> switch_001.Switch
            instances_animator.links.new(group_input_009.outputs[6], switch_001.inputs[0])
            # group_input_009.Random density -> distribute_points_on_faces.Density
            instances_animator.links.new(group_input_009.outputs[7], distribute_points_on_faces.inputs[4])
            # group_input_009.Random seed -> distribute_points_on_faces.Seed
            instances_animator.links.new(group_input_009.outputs[8], distribute_points_on_faces.inputs[6])
            # set_material.Geometry -> join_geometry.Geometry
            instances_animator.links.new(set_material.outputs[0], join_geometry.inputs[0])
            # subdivide_mesh_002.Mesh -> switch_002.True
            instances_animator.links.new(subdivide_mesh_002.outputs[0], switch_002.inputs[2])
            # group_input_011.Show main mesh -> switch_002.Switch
            instances_animator.links.new(group_input_011.outputs[1], switch_002.inputs[0])
            # group_input_010.Collection for instances -> collection_info.Collection
            instances_animator.links.new(group_input_010.outputs[3], collection_info.inputs[0])
            # set_position_002.Geometry -> switch_001.False
            instances_animator.links.new(set_position_002.outputs[0], switch_001.inputs[1])
            # distribute_points_on_faces.Points -> switch_001.True
            instances_animator.links.new(distribute_points_on_faces.outputs[0], switch_001.inputs[2])
            # switch_004.Output -> math.Value
            instances_animator.links.new(switch_004.outputs[0], math.inputs[0])
            # reroute_002.Output -> subdivide_mesh_001.Mesh
            instances_animator.links.new(reroute_002.outputs[0], subdivide_mesh_001.inputs[0])
            # reroute_002.Output -> subdivide_mesh_002.Mesh
            instances_animator.links.new(reroute_002.outputs[0], subdivide_mesh_002.inputs[0])
            # group_input.Geometry -> reroute_002.Input
            instances_animator.links.new(group_input.outputs[0], reroute_002.inputs[0])
            # math_007.Value -> subdivide_mesh_002.Level
            instances_animator.links.new(math_007.outputs[0], subdivide_mesh_002.inputs[1])
            # math_007.Value -> subdivide_mesh_001.Level
            instances_animator.links.new(math_007.outputs[0], subdivide_mesh_001.inputs[1])
            # group_input_012.Subdivide mesh -> math_007.Value
            instances_animator.links.new(group_input_012.outputs[2], math_007.inputs[1])
            # switch_003.Output -> instance_on_points.Rotation
            instances_animator.links.new(switch_003.outputs[0], instance_on_points.inputs[5])
            # group_input_007.Random rotation -> switch_003.Switch
            instances_animator.links.new(group_input_007.outputs[12], switch_003.inputs[0])
            # group_input_007.Value of random -> random_value.Max
            instances_animator.links.new(group_input_007.outputs[13], random_value.inputs[3])
            # random_value.Value -> switch_003.True
            instances_animator.links.new(random_value.outputs[1], switch_003.inputs[2])
            # combine_xyz_002.Vector -> switch_003.False
            instances_animator.links.new(combine_xyz_002.outputs[0], switch_003.inputs[1])
            # random_value_001.Value -> switch_004.True
            instances_animator.links.new(random_value_001.outputs[1], switch_004.inputs[2])
            # group_input_010.Scale instance -> switch_004.False
            instances_animator.links.new(group_input_010.outputs[15], switch_004.inputs[1])
            # group_input_010.Random scale -> switch_004.Switch
            instances_animator.links.new(group_input_010.outputs[16], switch_004.inputs[0])
            # group_input_010.Min scale -> random_value_001.Min
            instances_animator.links.new(group_input_010.outputs[17], random_value_001.inputs[2])
            # group_input_010.Max scale -> random_value_001.Max
            instances_animator.links.new(group_input_010.outputs[18], random_value_001.inputs[3])
            # group_input_010.Seed rs -> random_value_001.Seed
            instances_animator.links.new(group_input_010.outputs[19], random_value_001.inputs[8])
            # group_input_007.Seed rr -> random_value.Seed
            instances_animator.links.new(group_input_007.outputs[14], random_value.inputs[8])
            # switch_002.Output -> join_geometry.Geometry
            instances_animator.links.new(switch_002.outputs[0], join_geometry.inputs[0])
            
            # =================================================================================
            # КОНЕЦ БЛОКА НОДОВ
            # =================================================================================
            return instances_animator
        
        if not context.object:
            self.report({"WARNING"}, "No active object selected")
            return {"CANCELLED"}

        obj = context.object

        if "Instances animator" in obj.modifiers:
            self.report({"INFO"}, "Instances Animator is already applied.")
            return {"CANCELLED"}

        # Ищем группу нодов, если нет - создаем
        node_group = bpy.data.node_groups.get("Instances animator")
        if not node_group:
            node_group = instances_animator_node_group()

        mod = obj.modifiers.new(name="Instances animator", type="NODES")
        mod.node_group = node_group

        # Сразу после создания синхронизируем все параметры
        update_all_animator_properties(context)

        return {"FINISHED"}


class DeleteInstancesAnimatorOperator(bpy.types.Operator):
    bl_idname = "node.delete_instances_animator"
    bl_label = "Delete Instances Animator"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if not context.object:
            self.report({"WARNING"}, "No active object selected")
            return {"CANCELLED"}

        obj = context.object

        modifier_to_remove = obj.modifiers.get("Instances animator")
        if modifier_to_remove:
            # Запоминаем имя группы нодов ПЕРЕД удалением модификатора
            node_group_name = modifier_to_remove.node_group.name
            obj.modifiers.remove(modifier_to_remove)

            # Ищем группу нодов по имени
            node_group = bpy.data.node_groups.get(node_group_name)
            
            # Если группа существует и у нее больше нет пользователей, удаляем ее
            if node_group and node_group.users == 0:
                bpy.data.node_groups.remove(node_group)

        else:
            self.report({"INFO"}, "Instances Animator modifier not found.")

        return {"FINISHED"}


# =================================================================================
# ЛОГИКА СВЯЗИ UI И МОДИФИКАТОРА
# =================================================================================

def update_all_animator_properties(context):
    """Синхронизирует все проперти сцены с модификатором на активном объекте."""
    obj = context.object
    if not obj:
        return

    mod = obj.modifiers.get("Instances animator")
    if not mod or not mod.node_group:
        return

    # Правильный способ итерации по сокетам интерфейса
    for item in mod.node_group.interface.items_tree:
        # Убеждаемся, что это сокет, а не панель
        if hasattr(item, "in_out") and item.in_out == "INPUT":
            # Формируем имя проперти из имени сокета
            prop_name = "instances_animator_" + item.name.lower().replace(" ", "_")
            
            if hasattr(context.scene, prop_name):
                value = getattr(context.scene, prop_name)
                try:
                    # Устанавливаем значение в модификаторе по уникальному идентификатору сокета
                    mod[item.identifier] = value
                except Exception as e:
                    print(f"Error updating property {prop_name} on modifier: {e}")

    # Принудительно обновляем вьюпорт
    if obj:
        obj.update_tag()

def update_single_animator_property(self, context):
    """Эта функция-заглушка вызывается каждым свойством и запускает основную функцию обновления."""
    update_all_animator_properties(context)


# =================================================================================
# РЕГИСТРАЦИЯ КЛАССОВ И СВОЙСТВ
# =================================================================================

def register():
    bpy.utils.register_class(InstancesAnimatorPanel)
    bpy.utils.register_class(InstancesAnimatorOperator)
    bpy.utils.register_class(DeleteInstancesAnimatorOperator)

    properties = [
        ("instances_animator_show_main_mesh", bpy.props.BoolProperty(name="Show Main Mesh", default=False, update=update_single_animator_property)),
        ("instances_animator_subdivide_mesh", bpy.props.IntProperty(name="Subdivide Mesh", default=0, min=0, max=1000, update=update_single_animator_property)),
        ("instances_animator_collection_for_instances", bpy.props.PointerProperty(type=bpy.types.Collection, name="Collection for Instances", update=update_single_animator_property)),
        ("instances_animator_set_material", bpy.props.BoolProperty(name="Set Material", default=False, update=update_single_animator_property)),
        ("instances_animator_material", bpy.props.PointerProperty(type=bpy.types.Material, name="Material", update=update_single_animator_property)),
        ("instances_animator_random_instances", bpy.props.BoolProperty(name="Random Instances", default=False, update=update_single_animator_property)),
        ("instances_animator_random_density", bpy.props.FloatProperty(name="Random Density", default=200.0, min=0.0, update=update_single_animator_property)),
        ("instances_animator_random_seed", bpy.props.IntProperty(name="Random Seed", default=0, update=update_single_animator_property)),
        ("instances_animator_x_rotation", bpy.props.FloatProperty(name="X Rotation", default=0.0, update=update_single_animator_property)),
        ("instances_animator_y_rotation", bpy.props.FloatProperty(name="Y Rotation", default=0.0, update=update_single_animator_property)),
        ("instances_animator_z_rotation", bpy.props.FloatProperty(name="Z Rotation", default=0.0, update=update_single_animator_property)),
        ("instances_animator_random_rotation", bpy.props.BoolProperty(name="Random Rotation", default=False, update=update_single_animator_property)),
        ("instances_animator_value_of_random", bpy.props.FloatProperty(name="Value of Random", default=1.0, update=update_single_animator_property)),
        ("instances_animator_seed_rr", bpy.props.IntProperty(name="Seed rr", default=0, update=update_single_animator_property)),
        ("instances_animator_scale_instance", bpy.props.FloatProperty(name="Scale Instance", default=1.0, update=update_single_animator_property)),
        ("instances_animator_random_scale", bpy.props.BoolProperty(name="Random Scale", default=False, update=update_single_animator_property)),
        ("instances_animator_min_scale", bpy.props.FloatProperty(name="Min Scale", default=1.0, update=update_single_animator_property)),
        ("instances_animator_max_scale", bpy.props.FloatProperty(name="Max Scale", default=3.0, update=update_single_animator_property)),
        ("instances_animator_seed_rs", bpy.props.IntProperty(name="Seed rs", default=0, update=update_single_animator_property)),
        ("instances_animator_looping_frames", bpy.props.FloatProperty(name="Looping Frames", default=70.0, update=update_single_animator_property)),
        ("instances_animator_speed", bpy.props.FloatProperty(name="Speed", default=1.0, update=update_single_animator_property)),
        ("instances_animator_distortion", bpy.props.FloatProperty(name="Distortion", default=0.0, update=update_single_animator_property)),
        ("instances_animator_distortion_scale", bpy.props.FloatProperty(name="Distortion Scale", default=5.0, update=update_single_animator_property)),
        ("instances_animator_x_offset", bpy.props.FloatProperty(name="X Offset", default=0.0, update=update_single_animator_property)),
        ("instances_animator_y_offset", bpy.props.FloatProperty(name="Y Offset", default=0.0, update=update_single_animator_property)),
        ("instances_animator_z_offset", bpy.props.FloatProperty(name="Z Offset", default=0.0, update=update_single_animator_property)),
    ]
    for prop_name, prop_value in properties:
        setattr(bpy.types.Scene, prop_name, prop_value)


def unregister():
    bpy.utils.unregister_class(InstancesAnimatorPanel)
    bpy.utils.unregister_class(InstancesAnimatorOperator)
    bpy.utils.unregister_class(DeleteInstancesAnimatorOperator)

    properties_to_delete = [
        "instances_animator_show_main_mesh",
        "instances_animator_subdivide_mesh",
        "instances_animator_collection_for_instances",
        "instances_animator_set_material",
        "instances_animator_material",
        "instances_animator_random_instances",
        "instances_animator_random_density",
        "instances_animator_random_seed",
        "instances_animator_x_rotation",
        "instances_animator_y_rotation",
        "instances_animator_z_rotation",
        "instances_animator_random_rotation",
        "instances_animator_value_of_random",
        "instances_animator_seed_rr",
        "instances_animator_scale_instance",
        "instances_animator_random_scale",
        "instances_animator_min_scale",
        "instances_animator_max_scale",
        "instances_animator_seed_rs",
        "instances_animator_looping_frames",
        "instances_animator_speed",
        "instances_animator_distortion",
        "instances_animator_distortion_scale",
        "instances_animator_x_offset",
        "instances_animator_y_offset",
        "instances_animator_z_offset",
    ]
    for prop in properties_to_delete:
        if hasattr(bpy.types.Scene, prop):
            delattr(bpy.types.Scene, prop)


if __name__ == "__main__":
    register()
