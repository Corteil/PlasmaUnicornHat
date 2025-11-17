import math

def hsv_to_rgb(h, s, v):
    """Convert HSV color space to RGB color space
    
    @param h: Hue
    @param s: Saturation
    @param v: Value
    return (r, g, b)  
    """
   
    hi = math.floor(h / 60.0) % 6
    f =  (h / 60.0) - math.floor(h / 60.0)
    p = v * (1.0 - s)
    q = v * (1.0 - (f*s))
    t = v * (1.0 - ((1.0 - f) * s))
    output = {
        0: [v, t, p],
        1: [q, v, p],
        2: [p, v, t],
        3: [p, q, v],
        4: [t, p, v],
        5: [v, p, q],
    }[hi]
    output[0] = int(output[0] * 255)
    output[1] = int(output[1] * 255)
    output[2] = int(output[2] * 255)
    return output

"""
r, b, g = hsv_to_rgb(27, 0.813, 0.902)

print(f"red: {r} blue: {b} green: {g}")
"""