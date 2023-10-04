from numba import cuda
import numpy as np
from math import sin, cos, sqrt, copysign
from soft_nudge.cuda_utils import lerp, general_sine_wave


@cuda.jit(device=True, cache=True)
def fsx(x, y, period, amplitude, w, h, t):
    return amplitude * abs(h / 2) * (sin(x / (w / 2 / period) + t) * sin(t)) + x + h / 2


@cuda.jit(device=True, cache=True)
def fsy(x, y, period, amplitude, w, h, t):
    return amplitude * abs(w / 2) * (sin(y / (h / 2 / period) + t) * sin(t)) + y + w / 2


@cuda.jit(device=True, cache=True)
def fx(x, y, period, amplitude, w, h, t):
    return min(
        abs(fsx(x, y, period, amplitude, w, -h, t) - (x + y)),
        abs(fsx(x, y, period, amplitude, w, h, t) - (x + y)),
    )


@cuda.jit(device=True, cache=True)
def fy(x, y, period, amplitude, w, h, t):
    return min(
        abs(fsy(x, y, period, amplitude, -w, h, t) - (x + y)),
        abs(fsy(x, y, period, amplitude, w, h, t) - (x + y)),
    )


@cuda.jit(device=True, cache=True)
def border_effect_f(x, y, period, amplitude, w, h, t):
    if (
        fsy(x, y, period, amplitude, -w, h, t) - y < x
        and fsy(x, y, period, amplitude, w, h, t) - y > x
        and fsx(x, y, period, amplitude, w, -h, t) - x < y
        and fsx(x, y, period, amplitude, w, h, t) - x > y
    ):
        return fx(x, y, period, amplitude, w, h, t) * fy(
            x, y, period, amplitude, w, h, t
        )
    return 0.0


@cuda.jit(device=True, cache=True)
def slope(x, s):
    return min(2 ** (5 * ((x / s) ** 3)), 1)


@cuda.jit(cache=True)
def render_graphics_cuda(
    image,
    w,
    h,
    rgba,
    period,
    amplitude,
    undulation_frequency,
    duration,
    trend_split,
    flat_time_pct,
    t,
    pop_in_outside,
    pop_in_inside,
    limit_rect_x1,
    limit_rect_y1,
    limit_rect_x2,
    limit_rect_y2,
):
    height = image.shape[0]
    width = image.shape[1]

    startX = cuda.blockDim.x * cuda.blockIdx.x + cuda.threadIdx.x  # type: ignore
    startY = cuda.blockDim.y * cuda.blockIdx.y + cuda.threadIdx.y  # type: ignore
    gridX = cuda.gridDim.x * cuda.blockDim.x  # type: ignore
    gridY = cuda.gridDim.y * cuda.blockDim.y  # type: ignore

    tseconds = t / 1_000_000_000
    undulation_time = tseconds * 2 * np.pi * undulation_frequency
    xt = tseconds
    duration_a = duration * trend_split
    duration_ms = (duration - duration_a) * flat_time_pct
    duration_b = duration - duration_a - duration_ms

    # progress formula: https://www.desmos.com/calculator/orf5s78po2
    fa = slope(xt - duration_a, duration_a)
    fb = -slope(xt - duration, duration_b) + 1
    xfade = -slope(xt - duration, duration_b + duration_ms) + 1

    progress = lerp(fb, fa, xfade)

    pcx = w / 2
    pcy = h / 2

    # limit rect debug code
    # progress = 1
    # undulation_time = (np.pi/2)/(2*np.pi*undulation_frequency)

    for x in range(startX, width, gridX):
        for y in range(startY, height, gridY):
            px = x
            py = y

            if x == 0 and y == 0 and tseconds >= duration:
                # Trigger kill with this color: 101 110 100 are the codes for e n d in ascii: http://sticksandstones.kstrom.com/appen.html
                image[y, x, 0] = 101
                image[y, x, 1] = 110
                image[y, x, 2] = 100
                image[y, x, 3] = 255
                continue

            if (px > limit_rect_x1 and px < limit_rect_x2) and (
                py > limit_rect_y1 and py < limit_rect_y2
            ):
                # limit rect debug code
                # image[y, x, 0] = 255
                # image[y, x, 1] = 0
                # image[y, x, 2] = 0
                # image[y, x, 3] = 20
                continue

            pixel_r = 0
            pixel_g = 0
            pixel_b = 0
            pixel_a = 0

            a = border_effect_f(
                (px - pcx),
                (py - pcy),
                period,
                amplitude,
                w * lerp(pop_in_outside, pop_in_inside, progress),
                h * lerp(pop_in_outside, pop_in_inside, progress),
                undulation_time,
            )
            if a < 50:
                pixel_r = rgba[0]
                pixel_g = rgba[1]
                pixel_b = rgba[2]
                pixel_a = rgba[3]

            image[y, x, 0] = pixel_r
            image[y, x, 1] = pixel_g
            image[y, x, 2] = pixel_b
            image[y, x, 3] = pixel_a


def render_frame(
    w,
    h,
    rgba,
    period,
    amplitude,
    undulation_frequency,
    duration,
    trend_split,
    flat_time_pct,
    t,
    pop_in_outside,
    pop_in_inside,
    limit_rect_x1,
    limit_rect_y1,
    limit_rect_x2,
    limit_rect_y2,
):
    cimage = np.zeros((h, w, 4), dtype=np.uint8)
    blockdim = (32, 8)
    griddim = (32, 16)

    d_image = cuda.to_device(cimage)
    render_graphics_cuda[blockdim, griddim](
        d_image,
        w,
        h,
        rgba,
        period,
        amplitude,
        undulation_frequency,
        duration,
        trend_split,
        flat_time_pct,
        t,
        pop_in_outside,
        pop_in_inside,
        limit_rect_x1,
        limit_rect_y1,
        limit_rect_x2,
        limit_rect_y2,
    )
    d_image.copy_to_host(cimage)
    return cimage.astype(np.uint8)


def get_bmp_data(
    w,
    h,
    rgba,
    period,
    amplitude,
    undulation_frequency,
    duration,
    trend_split,
    flat_time_pct,
    t,
    pop_in_outside,
    pop_in_inside,
    limit_rect_x1,
    limit_rect_y1,
    limit_rect_x2,
    limit_rect_y2,
):
    frame = render_frame(
        w,
        h,
        rgba,
        period,
        amplitude,
        undulation_frequency,
        duration,
        trend_split,
        flat_time_pct,
        t,
        pop_in_outside,
        pop_in_inside,
        limit_rect_x1,
        limit_rect_y1,
        limit_rect_x2,
        limit_rect_y2,
    )

    cdata = frame[:, :, 0:3]
    adata = frame[:, :, 3]
    return cdata, adata
