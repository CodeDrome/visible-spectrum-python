from PIL import Image, ImageDraw, ImageFont


def generate_data():

    """
    Creates a list of dictionaries
    containing data on the visible
    portion of the electromagnetic
    spectrum.
    """

    data = []

    c = 3 * 10**8  # speed of light in m/s
    h = 6.62607015 * 10**-34  # Planck's constant in Js

    for nm in range(380, 781):

        item = {}

        item["nm"] = nm
        item["Hz"] = (c / (nm * 10**-9))
        item["THz"] = int(item["Hz"] * 10**-12)
        item["rgb"] = _wavelength_to_rgb(nm)
        item["J"] = h * item["Hz"]
        item["E"] = item["J"] * 10**19

        data.append(item)

    return data


def print_data(data):

    """
    Prints the data structure returned by
    generate_data in a table format.
    """

    width = 37
    pow_minus19 = chr(8315) + chr(185) + chr(8313)

    print("-" * width)
    print(f"|{chr(955)}(nm)|f(THz)|E(J)      |R  |G  |B  |")
    print("-" * width)

    for item in data:

        print(f"|{item['nm']:>5.0f}|", end="")
        print(f"{item['THz']:>6.0f}|", end="")
        print(f"{item['E']:>4.2f}x10{pow_minus19}|", end="")
        print(f"{item['rgb'][0]:>3.0f}|", end="")
        print(f"{item['rgb'][1]:>3.0f}|", end="")
        print(f"{item['rgb'][2]:>3.0f}|")

    print("-" * width)


def plot_wavelength_frequency(data, filename):

    """
    Plots the data structure from generate_data
    with wavelength on the x-axis and frequency
    on the y-axis using an approximation
    of the actual colours.
    """

    border_width = 70
    width_scaling = 2
    height_scaling = 0.5
    image_width = int(401 * width_scaling) + (border_width * 2)
    image_height = int(800 * height_scaling) + (border_width * 2)
    column_width = width_scaling
    column_bottom = image_height - border_width
    x = border_width

    image = Image.new("RGB", (image_width, image_height), (32, 32, 32))

    image = _draw_labels(image, "Visible Spectrum", "Wavelength (nm)", "Frequency (THz)")
    _draw_x_axes(image, border_width, 380, 780, 50)
    _draw_y_axes(image, border_width, 0, 800, 50)

    draw = ImageDraw.Draw(image)

    for item in data:

        column_top = column_bottom - (item["THz"] * height_scaling)

        draw.rectangle(xy=[x, column_bottom, x - column_width, column_top],
                       fill=item["rgb"])

        x += column_width

    try:
        image.save(filename, "PNG")
    except IOError as e:
        print(e)


def plot_frequency_wavelength(data, filename):

    """
    Plots the data structure from generate_data
    with frequency on the x-axis and wavelength
    on the y-axis using an approximation
    of the actual colours.
    """

    border_width = 70
    width_scaling = 2
    height_scaling = 0.5
    image_width = int(401 * width_scaling) + (border_width * 2)
    image_height = int(800 * height_scaling) + (border_width * 2)
    column_width = width_scaling
    column_bottom = image_height - border_width
    x = image_width - border_width

    image = Image.new("RGB", (image_width, image_height), (32, 32, 32))

    image = _draw_labels(image, "Visible Spectrum", "Frequency (THz)", "Wavelength (nm)")
    _draw_x_axes(image, border_width, 384, 789, 50)
    _draw_y_axes(image, border_width, 0, 800, 50)

    draw = ImageDraw.Draw(image)

    for item in data:

        column_top = column_bottom - (item["nm"] * height_scaling)

        draw.rectangle(xy=[x, column_bottom, x - column_width, column_top],
                       fill=item["rgb"])

        x -= column_width

    try:
        image.save(filename, "PNG")
    except IOError as e:
        print(e)


def _draw_labels(image, heading_text, x_axis_text, y_axis_text):

    heading_font = ImageFont.truetype('Pillow/Tests/fonts/FreeSans.ttf', 32)
    axis_font = ImageFont.truetype('Pillow/Tests/fonts/FreeSans.ttf', 16)

    draw = ImageDraw.Draw(image)

    heading_text_size = draw.textsize(text=heading_text, font=heading_font)
    draw.text(xy=((image.width / 2)-(heading_text_size[0] / 2), 8),
              text=heading_text,
              align="center",
              font=heading_font,
              fill=(255, 255, 255))

    x_axis_text_size = draw.textsize(text=x_axis_text, font=axis_font)
    draw.text(xy=((image.width / 2) - (x_axis_text_size[0] / 2), image.height - 24),
              text=x_axis_text,
              font=axis_font,
              fill=(255, 255, 255))

    image = image.rotate(270, expand=1)
    draw = ImageDraw.Draw(image)
    y_axis_text_size = draw.textsize(text=y_axis_text, font=axis_font)
    draw.text(xy=((image.width / 2)-(y_axis_text_size[0] / 2), 8),
              text=y_axis_text,
              font=axis_font,
              fill=(255, 255, 255))
    image = image.rotate(90, expand=1)

    return image


def _draw_y_axes(image, border_width, y_axis_start, y_axis_end, y_axis_interval):

    y_axis_indices_x_left = border_width - 8
    y_axis_indices_x_right = border_width
    y = image.height - border_width
    y_distance = ((image.height - (border_width * 2)) / (y_axis_end - y_axis_start)) * y_axis_interval
    index_font = ImageFont.truetype('Pillow/Tests/fonts/FreeSans.ttf', 12)

    draw = ImageDraw.Draw(image)

    for v in range(y_axis_start, y_axis_end + 1, y_axis_interval):
        draw.line(xy=[y_axis_indices_x_left, y, y_axis_indices_x_right, y],
                  fill=(255, 255, 255),
                  width=1)
        v_str = str(v)
        v_str_size = draw.textsize(text=v_str, font=index_font)
        draw.text(xy=[y_axis_indices_x_left - 2 - (v_str_size[0]), y - (v_str_size[1] / 2)],
                  text=v_str,
                  font=index_font,
                  fill=(255, 255, 255))
        y -= y_distance


def _draw_x_axes(image, border_width, x_axis_start, x_axis_end, x_axis_interval):

    x_axis_indices_y_top = image.height - border_width
    x_axis_indices_y_bottom = x_axis_indices_y_top + 8
    x = border_width
    x_distance = ((image.width - (border_width * 2)) / (x_axis_end - x_axis_start)) * x_axis_interval
    index_font = ImageFont.truetype('Pillow/Tests/fonts/FreeSans.ttf', 12)

    draw = ImageDraw.Draw(image)

    for v in range(x_axis_start, x_axis_end + 1, x_axis_interval):
        draw.line(xy=[x, x_axis_indices_y_bottom, x, x_axis_indices_y_top],
                  fill=(255, 255, 255),
                  width=1)
        v_str = str(v)
        v_str_size = draw.textsize(text=v_str, font=index_font)
        draw.text(xy=[x - (v_str_size[0] / 2), x_axis_indices_y_bottom + 2],
                  text=v_str,
                  font=index_font,
                  fill=(255, 255, 255))
        x += x_distance


def _wavelength_to_rgb(nm):

    gamma = 0.8
    max_intensity = 255
    factor = 0

    rgb = {"R": 0, "G": 0, "B": 0}

    if 380 <= nm <= 439:
        rgb["R"] = -(nm - 440) / (440 - 380)
        rgb["G"] = 0.0
        rgb["B"] = 1.0
    elif 440 <= nm <= 489:
        rgb["R"] = 0.0
        rgb["G"] = (nm - 440) / (490 - 440)
        rgb["B"] = 1.0
    elif 490 <= nm <= 509:
        rgb["R"] = 0.0
        rgb["G"] = 1.0
        rgb["B"] = -(nm - 510) / (510 - 490)
    elif 510 <= nm <= 579:
        rgb["R"] = (nm - 510) / (580 - 510)
        rgb["G"] = 1.0
        rgb["B"] = 0.0
    elif 580 <= nm <= 644:
        rgb["R"] = 1.0
        rgb["G"] = -(nm - 645) / (645 - 580)
        rgb["B"] = 0.0
    elif 645 <= nm <= 780:
        rgb["R"] = 1.0
        rgb["G"] = 0.0
        rgb["B"] = 0.0

    if 380 <= nm <= 419:
        factor = 0.3 + 0.7 * (nm - 380) / (420 - 380)
    elif 420 <= nm <= 700:
        factor = 1.0
    elif 701 <= nm <= 780:
        factor = 0.3 + 0.7 * (780 - nm) / (780 - 700)

    if rgb["R"] > 0:
        rgb["R"] = int(max_intensity * ((rgb["R"] * factor) ** gamma))
    else:
        rgb["R"] = 0

    if rgb["G"] > 0:
        rgb["G"] = int(max_intensity * ((rgb["G"] * factor) ** gamma))
    else:
        rgb["G"] = 0

    if rgb["B"] > 0:
        rgb["B"] = int(max_intensity * ((rgb["B"] * factor) ** gamma))
    else:
        rgb["B"] = 0

    return (rgb["R"], rgb["G"], rgb["B"])
