from graphics2 import *
from button import Button
    
MAX_COLOR_NUM = 255   
MAX_SIZE = 1000  
VERTICAL_RATIO = 69 / 55
ABBREV_LIST = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
               'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MH', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT','NE',
               'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD',
               'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'USA']
YEAR_LIST  = ['1960', '1964', '1968', '1972', '1976', '1980', '1984', '1988', '1992', '1996', '2000', '2004', '2008', '2012', '2016']

def get_response(window, region_box, year_box, button):
    """
    Waits for the user to click the button, then retrieves and validates input for region and year.

    Params:
    window (GraphWin): The graphical window to interact with.
    region_box (Entry): The entry box for the region input.
    year_box (Entry): The entry box for the year input.
    button (Button): The button to confirm the input.

    Returns:
    tuple: A tuple containing the validated region name and year.
    """
    
    click = window.getMouse()
    while not button.isClicked(click):
        click = window.getMouse()
    
    region_name = region_box.getText().upper()
    year = year_box.getText()
    
    error_text = None
    while region_name not in ABBREV_LIST or year not in YEAR_LIST:
  
        button.setLabel("Try again")
        button.activate()
        
        if region_name not in ABBREV_LIST and year not in YEAR_LIST:
            error_text = Text(Point(250, 450), "Invalid state abbrevation and year.Try again")
            
        elif region_name not in ABBREV_LIST:
            error_text = Text(Point(250, 450), "Invalid state abbrevation.Try again")
        
        elif year not in YEAR_LIST:
            error_text = Text(Point(250, 450), "Invalid year.Try again")
        
        error_text.setFill("red")
        error_text.draw(window)
        
        click = window.getMouse()
        while not button.isClicked(click):
            click = window.getMouse()
        
        region_name = region_box.getText().upper()
        year = year_box.getText()
        
        if error_text:
            error_text.undraw()
    
    return region_name, year
            
def get_map_choice(window, file):
    """
    Prompts the user to choose between red-blue or purple map types and generates the appropriate color dictionary.

    Params:
    window (GraphWin): The graphical window to interact with.
    file (file): File object containing election data.

    Returns:
    dict: A dictionary mapping subregions to colors based on the chosen map type.
    """
    
    direction = Text(Point(250,100), f"Choose the map type you want displayed")
    direction.draw(window)                 
          
    red_blue_map_button = Button(Point(150,150), 100, 25, "red_blue_map")
    red_blue_map_button.draw(window)
    red_blue_map_button.activate()
    
    purple_map_button = Button(Point(350,150), 100, 25, "purple_map")    
    purple_map_button.draw(window)
    purple_map_button.activate()
    
    click = window.getMouse()
    while (not red_blue_map_button.isClicked(click)) and (not purple_map_button.isClicked(click)):
        click = window.getMouse()
    
    if red_blue_map_button.isClicked(click):
        return make_red_blue_subregion_to_color_dict(file)
    
    else:
        return make_purple_subregion_to_color_dict(file)

def adjust_window(width, height):
    
    '''
    Adjusts the window dimensions based on the map's width and height.

    Params:
    width (float): The width of the map.
    height (float): The height of the map.

    Returns:
    tuple: A tuple containing adjusted window width and height.
    '''
    
    if width > height:
        new_width = MAX_SIZE
        new_height = int((height / width) * MAX_SIZE)
    
    elif height > width:
        new_width = int((width / height) * MAX_SIZE * VERTICAL_RATIO)
        new_height = MAX_SIZE
    
    else:
        new_width = MAX_SIZE
        new_height = MAX_SIZE
    
    return new_width, new_height

def make_red_blue_subregion_to_color_dict(fin_elect):
    
    '''
    Creates and returns a subregion_to_color_dictionary mapping the subregion
    name to red or blue insubregion_to_color_dictating whether republicans or
    democrates had more votes in that subregion

    Params:
    fin_elect (file): file object connected to the data file with voting data

    Returns:
    a subregion_to_color_dictionary matching a subregion to either red (republican) or blue (democrats)
    '''
    subregion_to_color_dict = {}
    
    fin_elect.readline()# we are not using this line 
    
    for line in fin_elect:
        line_data = line.split(',')
        sub_region = line_data[0].strip()
        republicans_vote = int(line_data[1])
        democrats_vote = int(line_data[2])
        
        if republicans_vote > democrats_vote:
            color = "red"
        
        else:
            color = "blue"
   
        subregion_to_color_dict[sub_region] = color 
        
    return subregion_to_color_dict

def make_purple_subregion_to_color_dict(fin_elect):
           
    '''
    Creates and returns a subregion_to_color_dictionary mapping the subregion
    name to a color representing the proportion of republican
    (red) votes, democratic (blue) votes, and independent
    (green) votes for a particular presidential election.

    Params:
    fin_elect (file): file object connected to the data file with voting data

    Returns:
    a dict matching a subregion to a shade of purple
    '''
    subregion_to_color_dict = {}
    first_line = fin_elect.readline()
    
    for line in fin_elect:
        line_data = line.split(',')
        sub_region = line_data[0].strip()
        republicans_vote = int(line_data[1])
        democrats_vote = int(line_data[2])
        other_vote = int(line_data[3])
        
        red = int(republicans_vote / (republicans_vote + democrats_vote + other_vote) * MAX_COLOR_NUM)
        green = int(other_vote / (republicans_vote + democrats_vote + other_vote) * MAX_COLOR_NUM)
        blue = int(democrats_vote / (republicans_vote + democrats_vote + other_vote) * MAX_COLOR_NUM)
        
        color = color_rgb(red, green, blue)
   
        subregion_to_color_dict[sub_region] = color 
    
    return subregion_to_color_dict

def make_map(file,window,subregion_to_color_dict):
    '''
    Draws subregions on the map and fills them with appropriate colors.

    Params:
    file (file): The file object containing map data.
    window (GraphWin): The graphical window to draw on.
    subregion_to_color_dict (subregion_to_color_dict): A dict mapping subregions to colors.
    '''
    num_region = int(file.readline())
    
    for count in range(num_region):
        
        file.readline()        
        sub_region = file.readline().strip()
        region = file.readline()
        num_sub_region = int(file.readline())
        
        vertex_list = []
        
        for num in range(num_sub_region):
            
            line = file.readline()
            line_list = line.split()
            x_coordinate = line_list[0]
            y_coordinate = line_list[-1]
            
            vertex_list.append(Point(x_coordinate, y_coordinate))
        
        polygon = Polygon(vertex_list)
        polygon.draw(window)
        
        if sub_region in subregion_to_color_dict:
            color = subregion_to_color_dict[sub_region]
        else:
            color ='black'
        
        polygon.setFill(color)

def display_window(file,name,year):
    
    '''
    Creates a graphical window based on the map size.

    Params:
    file (file): The file object containing map data.
    name (str): The name of the region.
    year (str): The election year.

    Returns:
    Graphwin: A GraphWin object representing the graphical window.  
    '''
    line1 = file.readline()
    line2 = file.readline()
    
    min_x = float(line1.split()[0])
    min_y = float(line1.split()[-1])
    max_x = float(line2.split()[0])
    max_y = float(line2.split()[-1])
    
    width = max_x - min_x
    height = max_y - min_y
    
    window_width, window_height = adjust_window(width, height)
    
    window = GraphWin(f"{name} {year}", window_width, window_height)
    window.setBackground("black")
    window.setCoords(min_x, min_y, max_x, max_y)
    
    return window
       
def selection_window():
    
    '''
    Creates a graphical window based on the map size.

    Returns:
    tuple: Containg a window and strings that came from user input
    '''
    
    window = GraphWin("Purple map", 500, 500)
    window.setBackground('white')
    
    region_name_box = Entry(Point(150,150), 5)
    year_box = Entry(Point(350,150), 5)
    region_name_box.draw(window)
    year_box.draw(window)
    region_name_box.setTextColor("white")
    year_box.setTextColor("white")
    
    direction = Text(Point(150,125), "Enter 'USA' or a state postal code")
    direction_year = Text(Point(350, 125), "Enter election year(1960 - 2016)")
    direction_year.draw(window)
    direction.draw(window)
    
    button = Button(Point(460,25), 70, 30,"Continue","grey")
    button.draw(window)
    button.activate()
    button.setLabelColor("white")
    
    region_name, year = get_response(window, region_name_box, year_box, button)
    
    region_name_box.undraw()
    year_box.undraw()
    direction.undraw()
    direction_year.undraw()
    button.setLabel("Continue")
    button.setLabelColor("white")
    
    return region_name, year, window

def main():
    
    region, year, window = selection_window()
    
    file_name = f"purple/{region}.txt"   
    election_file_name = f"purple/{region}{year}.txt"
    
    fin = open(file_name, 'r')
    fin_elect = open(election_file_name, "r")
    
    subregion_to_color_dict = get_map_choice(window, fin_elect)
    window.close()
    win = display_window(fin,region,year)
    make_map(fin,win, subregion_to_color_dict)
    
    fin.close()
    fin_elect.close()
    
main()