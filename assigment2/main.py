import pandas as pd
import tkinter as tk
import math

################ CURRENT DATA SET#################### , change it here to data1 or data2 :) ##
data = data2

data1 = pd.read_csv("data1.csv", header=None)
data1.columns = ["x", "y", "category"]
print(data1.head())

data2 = pd.read_csv("data2.csv", header=None)
data2.columns = ["x", "y", "category"]
print(data2.head())

root = tk.Tk()
root.title("Data Viewer")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

points= []
grid_items = []
selected_index = None # which point selected for moving

def draw_point(x, y, cat):
    r = 4 
    if cat == 0:
        item = canvas.create_rectangle(x-r, y-r, x+r, y+r, fill="red", outline="")
    elif cat == 1:
        item = canvas.create_oval(x-r, y-r, x+r, y+r, fill="black", outline="")
    else:
        item = canvas.create_polygon(x, y-r, x-r, y+r, x+r, y+r, fill="blue", outline="")
    return item

def find_clicked_point(mx, my):
    best = None
    best_dist = 10
    for i, p in enumerate(points):
        d = math.hypot(p["sx"] - mx, p["sy"] - my) # screen x and screen y
                                                   
        if d < best_dist:
            best = i
            best_dist = d
    return best

def reset_view():
    global grid_items 
    for p in points:
        canvas.itemconfig(p["item"], fill=p["base_fill"], outline="", width=1)
    
    for gid in grid_items:
        canvas.delete(gid)
    grid_items = []

## application of new views
def apply_quadrant_view(origin_idx):
    global grid_items

    origin = points[origin_idx]
    x0, y0 = origin["x"], origin["y"]
    sx0, sy0 = origin["sx"], origin["sy"]

    # draw new axes through selected point (new orgn)
    grid_items.extend([canvas.create_line(sx0, margin, sx0, h - margin), 
                       canvas.create_line(margin, sy0, w - margin, sy0)])
    
    # colour p different based on quadrant or center
    for i,p in enumerate(points): 
        if i == origin_idx:
            canvas.itemconfig(p["item"], fill=p["base_fill"], outline="purple", width=5)
            continue

        dx = p["x"] - x0 
        dy = p["y"] - y0
        if dx == 0 or dy == 0:
            color = "black"
        elif dx > 0 and dy > 0:
            color = "grey"
        elif dx < 0 and dy > 0:
            color = "green"
        elif dx < 0 and dy < 0:
            color = "yellow"
        else:
            color = "lightgreen"

        canvas.itemconfig(p["item"], fill=color)

def apply_euclidean_view(origin_idx):
    origin = points[origin_idx]
    x0, y0 = origin["x"], origin["y"] 

    canvas.itemconfig(origin["item"], outline="purple", width=5)

    dists = []
    # find all euclidean distances to other ps
    for i, p in enumerate(points):
        if i == origin_idx:
            continue #otherwise included in the five
        d = math.hypot(p["x"] - x0, p["y"] - y0)
        dists.append((d, i))

    dists.sort(key=lambda t: t[0])
    nearest = dists[:5]

    for d, i in nearest:
        canvas.itemconfig(points[i]["item"], outline="orange", width=5)

## click and unclick events tat trigger new views
def on_left_click(event):
    global selected_index
    
    idx = find_clicked_point(event.x, event.y)
    if idx is  None:
        return 
    
    if selected_index == idx:
        selected_index = None
        reset_view()
    
    else: 
        selected_index = idx
        apply_quadrant_view(idx)

def on_right_click(event):
    global selected_index
    
    idx = find_clicked_point(event.x, event.y)
    if idx is  None:
        return 
    
    if selected_index == idx:
        selected_index = None
        reset_view()
    
    else: 
        selected_index = idx
        apply_euclidean_view(idx)

def map_x(x):
    return margin + (x - xmin) / (xmax - xmin) * range_x

def map_y(y):
    return h - margin - (y - ymin) / (ymax - ymin) * range_y

# misc defs 
margin = 50 # margins for content
h,w = 600,800 # h and w of entire GUI
xmin, xmax = data["x"].min(), data["x"].max()
ymin, ymax = data["y"].min(), data["y"].max()

#axises
canvas.create_line(margin,margin, margin, h-margin)
canvas.create_line(margin, h-margin, w-margin, h-margin)

range_x, range_y = w-2*margin, h-2*margin # width and height of drawing area

## TICKS
for i in range(6):
    # ticks on x axis
    Xcurrtick = margin + i * range_x / ticks
    val = xmin + i * (xmax - xmin) / ticks
    canvas.create_line(Xcurrtick, h - margin, Xcurrtick, h - margin + 5)
    canvas.create_text(Xcurrtick, h - margin + 20, text=f"{val:.1f}")

    # ticks on y
    Ycurrtick = h - margin - i * range_y / ticks
    val = ymin + i * (ymax - ymin) / ticks
    canvas.create_line(margin - 5, Ycurrtick, margin, Ycurrtick)
    canvas.create_text(margin - 30, Ycurrtick, text=f"{val:.1f}")

## points list structure
categories = data["category"].unique()
BASE_FILLS = {0: "red", 1: "black", 2: "blue"} # too use during reset
for col, row in data.iterrows():
    sx = map_x(row.x)
    sy = map_y(row.y)
    cat_index = (categories == row.category).nonzero()[0][0]

    item_id = draw_point(sx, sy, cat_index)

    points.append({
        "x": row.x,
        "y": row.y,
        "sx": sx,
        "sy": sy,
        "item": item_id,
        "base_fill": BASE_FILLS.get(cat_index, "black")  #for resetting
    })
    
## LEGEND
txt ="--------------\n"
shapes = ["square", "circle", "triangle", "star"]
for i in range(categories.size):
    txt += categories[i] + ": " + shapes[i] + "\n"
txt+="------------"
canvas.create_text(w-30, 40,text=txt)

## second part
canvas.bind("<Button-1>", on_left_click)
canvas.bind("<Button-3>", on_right_click)

root.mainloop()
