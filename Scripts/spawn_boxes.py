import unreal
from .utils import spawn_obj
from .get_area_obj_list import get_area_obj_list, Box


def spawn_boxes(box_objs, area, origin_x, origin_y, origin_z):

    box_obj_list = []
    for box_obj in box_objs:
        box_obj_list.append(Box(
            box_obj['static_mesh_obj'],
            box_obj['asset_name'],
            box_obj['length'],
            box_obj['width'],
            box_obj['height'],
            is_rotated=False
        ))

    area_obj_list = get_area_obj_list(
        area,
        box_obj_list,
        is_with_margin=True,

        origin_x=origin_x,
        origin_y=origin_y,
        origin_z=origin_z,
    )

    for each in area_obj_list:
        spawn_obj(each.box_obj.static_mesh_obj,
                  unreal.Vector(each.x1, each.y1, each.z1),
                  unreal.Rotator(0, 0, 0))
