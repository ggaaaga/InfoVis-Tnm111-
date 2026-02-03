import pandas as pd
import tkinter as tk

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

def draw_point(x, y, cat):
    r = 4
    if cat == 0:
        canvas.create_rectangle(x-r, y-r, x+r, y+r, fill="red")
    elif cat == 1:
        canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")
    else:
        canvas.create_polygon(x, y-r, x-r, y+r, x+r, y+r, fill="blue")

def map_x(x):
    return margin + (x - xmin) / (xmax - xmin) * range_x

def map_y(y):
    return h - margin - (y - ymin) / (ymax - ymin) * range_y

## CURRENT DATA SET ##
data = data2

margin = 50 # margins for content
h,w = 600,800 # h and w of entire GUI
xmin, xmax = data["x"].min(), data["x"].max()
ymin, ymax = data["y"].min(), data["y"].max()

#axises
canvas.create_line(margin,margin, margin, h-margin)
canvas.create_line(margin, h-margin, w-margin, h-margin)

range_x, range_y = w-2*margin, h-2*margin # width and height of drawing area

## TICKS
ticks = 5
for i in range(ticks + 1):
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

categories = data["category"].unique()

## LEGEND
txt =""
shapes = ["square", "circle", "triangle", "star"]
for i in range(categories.size):
    txt += categories[i] + ": " + shapes[i] + "\n"

canvas.create_text(w-50, 50,text=txt)

for col, row in data.iterrows():
    # last param is to find the unique category
    draw_point(map_x(row.x), map_y(row.y), (categories == row.category).nonzero()[0][0])


root.mainloop()
