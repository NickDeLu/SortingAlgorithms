import pygame
import pygame_textinput as ti
import random
import time
import sys

pygame.init();
#Colors
COLUMNS = (171,222,231);
BACKGROUND = (100,170,200);
FONT = (40,40,40);
SWAP = (47,149,176);
SORTED = (45,124,85);5
RED = (255,0,0);

#Screen
screenX = 500;
screenY = 400;
screenSize = (screenX,screenY+110);
DisplayScreen = pygame.display.set_mode(screenSize,0);
pygame.display.set_caption("BubbleSort");
DisplayScreen.fill(BACKGROUND);

#text pygame_textinput
xInput = ti.TextInput(max_string_length=4);
xInput.set_text_color(FONT);
xEvent = True;

yInput = ti.TextInput(max_string_length=4);
yInput.set_text_color(FONT);
yEvent = False;

#speedSliders
speedSlider = pygame.Rect(210,screenY+10,30,20);
colSlider = pygame.Rect(250,screenY+20,30,20);
borderSlider = pygame.Rect(290,screenY+10,30,20);

#Clock
clock = pygame.time.Clock()

#Data
borderWidth = 1;
columnWidth = 50;
scl = int(screenX/columnWidth);
data = [];
rects = [];
global speed;
speed = 0;
sorted = False;

bubbleBox = pygame.Rect(420,screenY+10,20,20);
quickBox = pygame.Rect(420,screenY+50,20,20);

#font
fontValue = pygame.font.SysFont("Courier",int((columnWidth-borderWidth)/2),True);
fontTitles = pygame.font.SysFont("Courier",20,True);
fontLables = pygame.font.SysFont("Courier",11,True);

#populate the array
def populate():
    global sorted;
    sorted = False;
    data.clear();
    for i in range(scl):
        data.append(random.randint (0,screenY));


#draw data to screen
def generate():
    xPos = 0;
    rects.clear();
    for d in data:
        pygame.draw.rect(DisplayScreen, BACKGROUND, (xPos,screenY,columnWidth,-screenY),0);
        rects.append(pygame.draw.rect(DisplayScreen, COLUMNS, (xPos,screenY,columnWidth,-d),0));
        pygame.draw.rect(DisplayScreen, BACKGROUND, (xPos,screenY,borderWidth,-screenY),0);
        value = fontValue.render(str(d),True,FONT);
        DisplayScreen.blit(value,(xPos + ((columnWidth - value.get_width()) /2) + (borderWidth/2),screenY - value.get_height()));
        xPos += (screenX/scl);
        if speed > 0:
            time.sleep(speed);
            pygame.display.update();

#update columns of data
def updateColumns(Color, array, index):
    pygame.draw.rect(DisplayScreen, BACKGROUND, (rects[index].left,screenY,rects[index].w,-screenY),0); #clear column on screen
    pygame.draw.rect(DisplayScreen, Color, (rects[index].left,screenY,rects[index].w,-array[index]),0); #redraw at new position
    pygame.draw.rect(DisplayScreen, BACKGROUND, (rects[index].left,screenY,borderWidth,-screenY),0); #border of column
    value = fontValue.render(str(array[index]),True,FONT);
    DisplayScreen.blit(value,(rects[index].left + ((columnWidth - value.get_width()) /2) + (borderWidth/2), screenY - value.get_height())); #display new value
    if speed > 0:
        pygame.display.update();

def sort():
    global data;
    global sorted;
    if sorted == False:
        if checked == "bubbleBox":
            bubbleSort();
        else:
            data = quickSort(data);
        sorted = True;

#BubbleSort
def bubbleSort():
    global sorted;
    sorted = True;
    for i in range(len(data)-1,0,-1):
        for j in range(i):
            if data[j] > data[j+1]:
                updateColumns(SWAP,data,j);
                updateColumns(SWAP,data,j+1);
                time.sleep(speed);
                temp = data[j];
                data[j] = data[j+1]
                data[j+1] = temp;
            updateColumns(SWAP,data,j);
            updateColumns(SWAP,data,j+1);
            time.sleep(speed);
            updateColumns(COLUMNS,data,j);
            updateColumns(COLUMNS,data,j+1);
            if j+1 == i:
                updateColumns(SORTED,data,i);
            if i == 1:
                updateColumns(SORTED,data,0);

def quickSort(array):
    global sorted;
    sorted = True;
    length = len(array);
    if length <= 1:
        return array;
    else:
        pivot = array.pop();
    greaterThan = []
    lessThan = []
    for value in array:
        if value > pivot:
            greaterThan.append(value);
        else:
            lessThan.append(value);
    lessThan = quickSort(lessThan);
    greaterThan = quickSort(greaterThan);
    temp = lessThan + [pivot] + greaterThan;
    if speed > 0:
        for i in range(len(temp)):
            updateColumns(SWAP,temp,len(lessThan));
            time.sleep(speed);
            if temp[i] > pivot:
                updateColumns(SORTED,temp,i);
            else:
                updateColumns(RED,temp,i);
            time.sleep(speed);
    pygame.draw.rect(DisplayScreen, BACKGROUND, (screenX,screenY,-screenX,-screenY),0);
    if len(temp)-1 == len(data):
        for i in range(len(temp)):
            updateColumns(SORTED,temp,i)
    return temp;

#update the screen size
def updateScreenSize():
    global screenX;
    global screenY;
    global scl;
    global screenSize;
    global DisplayScreen;
    global speedSlider;
    global colSlider;
    global borderSlider;
    global bubbleBox;
    global quickBox;
    if len(xInput.get_text()) > 0:
        screenX = int(xInput.get_text());
        scl = int(screenX/columnWidth);
    if len(yInput.get_text()) > 0:
        oldY = screenY;
        screenY = int(yInput.get_text());
        speedSlider = pygame.Rect(210,speedSlider.y-(oldY-screenY),30,20);
        colSlider = pygame.Rect(250,colSlider.y-(oldY-screenY),30,20);
        borderSlider = pygame.Rect(290,borderSlider.y-(oldY-screenY),30,20);
        bubbleBox = pygame.Rect(420,bubbleBox.y-(oldY-screenY),20,20);
        quickBox = pygame.Rect(420,quickBox.y-(oldY-screenY),20,20);
    if ((len(xInput.get_text()) > 0) | ((len(yInput.get_text()))) > 0):
        screenSize = (screenX,screenY+110);
        DisplayScreen= pygame.display.set_mode(screenSize,0);
        xInput.clear_text();
        yInput.clear_text();
        xInput.update(events);
        yInput.update(events);
        DisplayScreen.fill(BACKGROUND);
        pygame.display.update();
        return True;
    else:
        pygame.draw.rect(DisplayScreen, BACKGROUND, (screenX,screenY,-screenX,-screenY),0);
        return False;

#run
def run():

    if updateScreenSize() == False:
        populate();
        generate();


class Button():
    def __init__(self, txt, location, action, bg=SWAP, fg=FONT, hover=COLUMNS, size=(80, 30), font_name="Arial", font_size=16):
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.size = size
        self.hover = hover

        self.font = self.font = pygame.font.SysFont(font_name, font_size,True)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)

        self.call_back_ = action

    def draw(self):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        DisplayScreen.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = self.hover  # mouseover color

    def call_back(self):
        self.call_back_()

def mousebuttondown():
    pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(pos):
            button.call_back()

def update_xEvent():
    global xEvent;
    global yEvent;
    xEvent = True;
    yEvent = False;

def update_yEvent():
    global xEvent;
    global yEvent;
    yEvent = True;
    xEvent = False;

def updateSlider(slider):
    if slider is speedSlider:
        title = fontLables.render(str(round(speed,2)),True,FONT);
    elif slider is colSlider:
        title = fontLables.render(str(round(scl)),True,FONT);
    elif slider is borderSlider:
        title = fontLables.render(str(round(borderWidth)),True,FONT);
    pygame.draw.rect(DisplayScreen, SWAP, (slider.x+10,screenY+10,10,80));
    pygame.draw.rect(DisplayScreen, COLUMNS, slider);
    DisplayScreen.blit(title,(slider.x,slider.y));

def updateCheckBox():
    global checked;
    if checked == "bubbleBox":
        pygame.draw.rect(DisplayScreen,COLUMNS,bubbleBox);
        pygame.draw.rect(DisplayScreen,SWAP,quickBox);
    else:
        pygame.draw.rect(DisplayScreen,SWAP,bubbleBox);
        pygame.draw.rect(DisplayScreen,COLUMNS,quickBox);

def sliderUpdateValue(slider, min, max):
    increment = (slider.y-screenY)-10
    value = (max-min)/60*increment + min;
    global speed;
    global columnWidth;
    global scl;
    global borderWidth;
    global fontValue
    if slider is speedSlider:
        speed = value;
        print(speed);
    elif slider is colSlider:
        columnWidth = value;
        print(speed);
        scl = int(screenX/columnWidth);
    elif slider is borderSlider:
        borderWidth = value;
    fontValue = pygame.font.SysFont("Courier",int((columnWidth-borderWidth)/2),True);

done = False;
selected = None;
checked = "bubbleBox";
while not done:
    pygame.draw.rect(DisplayScreen, BACKGROUND, (210,screenY+10,screenX,100));
    speedTitle = fontLables.render("Speed",True,FONT);
    colTitle = fontLables.render("Column",True,FONT);
    borderTitle = fontLables.render("Border",True,FONT);
    bubbleSortTitle = fontLables.render("Bubble Sort",True,FONT);
    quickSortTitle = fontLables.render("Quick Sort",True,FONT);
    DisplayScreen.blit(speedTitle,(speedSlider.x-6,screenY+90));
    DisplayScreen.blit(colTitle,(colSlider.x-3,screenY+90));
    DisplayScreen.blit(borderTitle,(borderSlider.x+6,screenY+90));
    DisplayScreen.blit(bubbleSortTitle,(340,screenY+10));
    DisplayScreen.blit(quickSortTitle,(340,screenY+50));
    updateSlider(speedSlider);
    updateSlider(colSlider);
    updateSlider(borderSlider);

    button_01 = Button("Generate", (50, screenY + 20), run)
    button_02 = Button("Sort",(150, screenY + 20), sort);
    button_03 = Button("", (50,screenY+85), update_xEvent);
    button_04 = Button("", (150,screenY+85), update_yEvent);
    buttons = [button_01,button_02,button_03, button_04];
    events = pygame.event.get()

    if xEvent == True:
        xInput.update(events);
    elif yEvent == True:
        yInput.update(events);

    for button in buttons:
        button.draw()

    screenSizeTitle = fontTitles.render("screenX,screenY",True,FONT);
    coordinates = fontTitles.render("(      ,      )",True,FONT);
    pygame.draw.rect(DisplayScreen, SWAP, (10,screenY+55,screenSizeTitle.get_width(),50));
    DisplayScreen.blit(xInput.get_surface(),(30,screenY+75));
    DisplayScreen.blit(yInput.get_surface(),(120,screenY+75));
    DisplayScreen.blit(screenSizeTitle,(10,screenY+55));
    DisplayScreen.blit(coordinates,(10,screenY+75));
    updateCheckBox();
    for event in events:
        if event.type == pygame.QUIT:
            done = True;
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                done = True;
            elif event.key == pygame.K_TAB:

                if xEvent == True:
                    update_yEvent()
                elif yEvent == True:
                    update_xEvent()
            elif event.key == pygame.K_RETURN:
                run();

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttondown()
            if speedSlider.collidepoint(event.pos):
                selected = "speed";
            if colSlider.collidepoint(event.pos):
                selected = "col";
            if borderSlider.collidepoint(event.pos):
                selected = "border";
            if bubbleBox.collidepoint(event.pos):
                checked = "bubbleBox";
            if quickBox.collidepoint(event.pos):
                checked = "quickBox";
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selected = None;
        elif event.type == pygame.MOUSEMOTION:

            if selected is not None: # selected can be `0` so `is not None` is required
                # move object
                boundary = range(screenY+10,screenY+71);
                if event.pos[1] in boundary:
                    if selected == "speed":
                        speedSlider.y = event.pos[1];
                        sliderUpdateValue(speedSlider,0,0.1);
                        updateSlider(speedSlider);
                    elif selected == "col":
                        colSlider.y = event.pos[1];
                        sliderUpdateValue(colSlider,borderWidth+2,screenX/2);
                        sliderUpdateValue(borderSlider,1,columnWidth-1);
                        updateSlider(colSlider);
                    elif selected == "border":
                        borderSlider.y = event.pos[1];
                        sliderUpdateValue(colSlider,borderWidth+2,screenX/2);
                        sliderUpdateValue(borderSlider,1,columnWidth-1);
                        updateSlider(borderSlider);

    pygame.display.update();
    pygame.display.flip()
    clock.tick(30);
