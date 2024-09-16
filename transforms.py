
def transform(self, x, y, dimension="3D"):
    if dimension.strip().lower() == "3d":
        return self.transform_perspective(x, y)
    else:
        return self.transform_2D(x, y)

def transform_2D(self, x, y):
    return int(x), int(y)

def transform_perspective(self, x, y):
    new_y = ( y *self.PERSPECTIVE_POINT["y"] ) /self.height
    if new_y > self.PERSPECTIVE_POINT["y"]:
        new_y = self.PERSPECTIVE_POINT["y"]
    dx = x - self.PERSPECTIVE_POINT["x"]
    dy = self.PERSPECTIVE_POINT["y"] - new_y
    factor_y = dy / self.PERSPECTIVE_POINT["y"]
    factor_y = pow(factor_y, 4)
    offset_x = dx * factor_y
    new_x = self.PERSPECTIVE_POINT["x"] + offset_x
    lin_y = self.PERSPECTIVE_POINT["y"] - factor_y * self.PERSPECTIVE_POINT["y"]
    return int(new_x), int(lin_y)