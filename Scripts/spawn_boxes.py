import unreal
from .utils import spawn_obj
from .get_area_obj_list import get_area_obj_list, Box


def spawn_boxes(box_obj_list, area, origin_x, origin_y, origin_z):
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
